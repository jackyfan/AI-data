from pydantic import BaseModel, Field
from dal.database import SQLiteDB
from utility.config import Config
from utility.logger_helper import LoggerHelper
from llm.openai_helper import json_chain
from datetime import datetime
from models.feature import get_feature_definition
from models.recommend import recommend_data_assets, recommend_data_asset

config = Config()
logger = LoggerHelper.get_logger(__name__)


class SQLResponse(BaseModel):
    """
    定义大模型返回的JSON格式
    """
    sql: str = Field(description="生成的SQL代码")


def get_query_specifications():
    sql = """
        -不要使用`with`语句定义仅包含日期或时间范围的临时表。应直接在每个查询的`where`子句中明确指定具体的日期或时间。
        -在处理日期增加或减少的需求时，必须使用date_add()函数。确保在SQL代码中正确使用date_add()函数来处理日期的增减，以保持数据处理的准确性和效率。
        -尽可能使用SQL代码简单易读。
        -如果'用户问题'中的时间没有提到具体的年份和月份，以'当前日期'的年份和月份为准。
        -'指标定义'中的变量需要替换成准确的时间。
        -必须严格遵循SQLite的语法规范。
        -不支持stack语法。
    """
    return sql


def sql_generate(task, dep_data):
    template = """
        作为一名专业游戏数据分析师，你非常熟悉游戏行业且擅长SQL代码开发。你需要理解"用户问题"，利用"指标定义"中提供的业务指标"计算SQL"和"库表定义"，结合"生成SQL注意事项"和"SQL语法编写要求"，按照以下"步骤"编写一个SQL。
        -当前日期是{currdate}
        ##用户问题
        {user_input}
        ##指标定义
        {feature_def}
        ##库表定义
        {table_assets}
        ##依赖资料
        {dep_data}
        ##SQL语法要求
        {query_specifications}
        严格按照如下JSON格式输出:
        {{'sql':'...'}}    
    """
    query_specifications = get_query_specifications()
    current_time = datetime.now()
    user_input = task.step

    feature_def = []
    for metric in task.step["metric"]:
        feature_def.append(get_feature_definition(metric))
    logger.debug(f'{feature_def=}')

    recommend_table = recommend_data_assets(user_input, topK=3)

    table_assets = []
    if recommend_table["code"] == 0:
        logger.debug(f'{recommend_table=}')
        # db = SQLiteDB('example.sqlite3')
        for table in recommend_table["data"]:
            table_assets.append(recommend_data_asset(table))

    prompt = template.format(user_input=user_input, query_specifications=
    query_specifications, currdate=current_time, dep_data=dep_data, table_assets=table_assets, feature_def=feature_def)
    model_name = config["LLM"].get("model_name", "qwen-plus")
    logger.debug(f"{prompt=}")
    response = json_chain(model_name, prompt, SQLResponse)
    return response
