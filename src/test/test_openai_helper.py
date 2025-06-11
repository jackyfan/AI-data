from langchain_core.messages import HumanMessage, SystemMessage
from llm.openai_helper import create_llm
from utility.logger_helper import LoggerHelper

logger = LoggerHelper.get_logger(__name__)
def test_openai_helper():
    chat = create_llm()
    messages = [
        SystemMessage(content="You're a helpful assistant"),
        HumanMessage(content="What is the purpose of model regularization?"),
    ]
    response = chat.invoke(messages)
    logger.debug(f'response:{response}\n')

if __name__ == '__main__':
    test_openai_helper()

