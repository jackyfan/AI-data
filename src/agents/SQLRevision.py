import json
from datetime import datetime
from langchain.schema import SystemMessage
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.output_parsers import JsonOutputParser

from llm.openai_helper import tool_chain
from utility.config import Config
from utility.logger_helper import LoggerHelper
from utility.unscape_helper import unescape_unicode
from dal.database import SQLiteDB
from models.table_meta import get_table_asserts

config = Config()
logger = LoggerHelper.get_logger(__name__)
db = SQLiteDB('example.sqlite3')


# 修正SQL
def correct_sql(sql, db_error, history, db, model_name):
    curate = datetime.now().strftime("%Y-%m-%d")

    system_prompt = f"""
        作为一名专业游戏数据分析师，你非常熟悉游戏行业并且擅长SQL代码开发。你将根据用户提供的SQL代码及数据库返回的错误信息，为用户写出正确的SQL代码。
        -当前日期是{curate}
        -特别注意，数据库的错误信息和用户信息中的内容可以提升编写SQL代码的成功率。
        -你仅能生成select查询语句。
    """

    user_prompt = f"""
        ##数据库错误信息
        {db_error}
        
        ##sql_input:
        {sql}
        特别注意，即将与程序对接，确保SQL代码简洁、准确。
        严格按照如下JSON格式输出：
        {{"reflect":(对SQL错误较为详细的反思)...,"sql":"..."}}
    """
    messages = [SystemMessage(system_prompt), *history, HumanMessage(user_prompt)]
    result = perform_correction(messages, db, model_name)
    return result


# 修正SQL
def invoke(message):
    try:
        logger.debug(f'{message=}')
        task = json.loads(message[-1].content)
        logger.debug(f'{task=}')
        retry_limit = int(config["LLM"].get("retry", 3))
        model_name = config["LLM"].get("model_name", "qwen-plus")
    except ValueError as e:
        logger.error(f'Error parsing retry limit:{e}')
        retry_limit = 3
    except Exception as e:
        logger.error(f'Exception during message parsing:{e}')
        return None
    logger.info(f'{retry_limit=}\n {task=}\n')
    eva_sql = task["sql"]
    history = []
    for attempt in range(retry_limit):
        logger.debug(f'第{attempt}次修正SQL:{eva_sql}')
        rst = db.explain(eva_sql)
        logger.info(f'SQL explain:{rst=}')
        if rst['code'] == 0:
            logger.info(f'SQL校验正确')
            break
        corrections = correct_sql(eva_sql, rst['msg'], history, db, model_name)
        logger.error(f'{corrections=}')
        history.extend(corrections)
        eva_sql = try_parse_new_sql(history)
        if eva_sql:
            task["sql"] = unescape_unicode(eva_sql)
            message.append(AIMessage(content=eva_sql, role="assistant"))
    return message


def perform_correction(message, db, model_name):
    result = []
    while True:
        logger.debug("Processing tool_call cycle...")
        rsp = tool_chain(model_name, message, [get_table_asserts])
        logger.debug(f'{rsp=}')
        message.append(rsp)
        result.append(rsp)
        for tool_call in rsp.tool_calls:
            selected_tool = get_table_asserts if tool_call["name"].lower() == "get_table_asserts" else None
            if selected_tool:
                logger.debug(f'{tool_call=}')
                tool_output = selected_tool(db, tool_call["args"]["table_name"])
                message.append(ToolMessage(json.dumps(tool_output, ensure_ascii=False), tool_call_id=tool_call["id"], role="tool"))
                result.append(message[-1])
        if isinstance(message[-1], ToolMessage):
            continue
        else:
            break
    return result


# 修正历史中提取和返回最新的SQL代码
def try_parse_new_sql(history):
    parser = JsonOutputParser()
    try:
        last_correction = history[-1].content
        sql_details = parser.parse(last_correction)
        return sql_details["sql"] if sql_details["sql"] else ""
    except Exception as e:
        logger.error(f'Failed to parsing new SQL:{e}')
        return ""
