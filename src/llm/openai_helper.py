import os, json
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

from utility.logger_helper import LoggerHelper

api_key = os.getenv("OPENAI_API_KEY")
logger = LoggerHelper.get_logger(__name__)


def create_llm(model_name="gpt-3.5-turbo"):
    """
    创建并返回一个指定模型的实例
    :param model_name: 模型名称
    :return: 模型实例
    """
    return ChatOpenAI(api_key=api_key, model_name=model_name, temperature=0)


def create_json_llm(model_name="gpt-3.5-turbo"):
    """
    创建并返回一个指定模型的实例,并设置返回格式为JSON
    :param model_name: 模型名称
    :return: 模型实例
    """
    llm = create_llm(model_name)
    return llm.bind(response_format={"type": "json_object"})


def json_chain(model_name, prompt, cls):
    """
    使用指定模型生成JSON格式的响应
    :param model_name: 模型名称
    :param prompt: 提示模板
    :param cls:
    :return:
    """
    json_llm = create_json_llm(model_name)
    chain = json_llm | JsonOutputParser(pydantic_object=cls)
    logger.debug(f'json_chain:{prompt}\n')
    response_json = chain.invoke(prompt)
    return json.dumps(response_json, ensure_ascii=False)

def tool_chain(model_name, prompt,tools=[]):
    """
    使用指定模型和工具链生成响应信息
    :param model_name: 模型名称
    :param prompt: 提示模板
    :param tools: 工具链
    :return:
    """

    tool_llm = create_json_llm(model_name)
    tool_llm = tool_llm.bind_tools(tools)
    logger.debug(f'tool_chain:{prompt}\n')

    response_json = tool_llm.invoke(prompt)
    return response_json

