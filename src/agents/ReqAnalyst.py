from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import AIMessage
from utility.config import Config
from utility.logger_helper import LoggerHelper
from langchain_core.pydantic_v1 import BaseModel, Field
from llm.openai_helper import json_chain

config = Config()
logger = LoggerHelper.get_logger(__name__)
"""
定义大模型返回的JSON格式
"""


class JsonResponse(BaseModel):
    serial_id: int = Field(description="数据包ID")
    id: str = Field(description="数据包")
    name: str = Field(description="数据包描述")
    input: str = Field(description="数据包输入")
    metric: list = Field(description="可量化的特性Metric")
    output: list = Field(description="输出字段数组")
    dependence: list = Field(description="依赖的包ID")


def invoke(user_input):
    # 设置系统提示词模板
    system_prompt = """
        你是一个专业的数据分析师，你的输出将提供给其他程序交互，请确保输出准确。
        #目标
        -"用户问题"应该先拆解成多个独立的"数据包"，再关联这些"数据包"，得到"结果"。
        -如果"数据包"的"dependence"是"无"，那么必须提取出"Metric"。
        -"Metric"是这个数据包的无时间范围特性metric的抽象描述，如注册人数、活跃人数等。
        -数据包中的"Metric"可以没有。
        #注意事项
        "拆解步骤"中一定只包含多个"数据包"和一个"结果"，不要存在多个"结果"。
        严格按照如下JSON格式输出:
        {{'step':[{{'serial_id':1,'id':'数据包n','name':'（数据包描述……）','input':'（输入数据包的详细执行描述……）','metric':['可量化的特性Metric'],'output':['输出字段'],'dependence':[serial_id])}},……]}}
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt,),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad")])
    logger.debug(f"{user_input=}")
    latest_message_content = user_input[-1].content

    model_name = config["ReqAnalyst"].get("model_name","gpt-3.5-turbo")
    response = json_chain(model_name=model_name, prompt=prompt.invoke(input={"messages": [latest_message_content], "agent_scratchpad": []}),cls=JsonResponse)
    logger.info(f'{response=}')

    return AIMessage(content=response)

