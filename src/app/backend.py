from fastapi import FastAPI, HTTPException
import json, os
from typing import List
from pydantic import BaseModel
from agents import ReqAnalyst, SQLGenerator, SQLRevision
from langchain_core.messages import HumanMessage, AIMessage
from utility.logger_helper import LoggerHelper
from utility.config import Config

config = Config
logger = LoggerHelper.get_logger(__name__)


class MessageRequest(BaseModel):
    messages: List[str]


app = FastAPI()


@app.post("/analyze-message/")
async def analyze_message(request: MessageRequest):
    try:
        # 关闭LangSmith追踪
        os.environ['LANGCHAIN_TRACING_V2'] = 'false'
        messages = [HumanMessage(content=msg) for msg in request.messages]
        response = ReqAnalyst.invoke(messages)
        logger.debug(f'1.分析需求：{response=}')
        messages.append(response)
        steps = json.loads(response.content)
        sql = SQLGenerator.invoke(steps)
        logger.debug(f'2.生成SQL：{sql=}')
        messages.append(AIMessage(content=sql))
        revisionMessage = SQLRevision.invoke(messages)
        logger.debug(f'3.修正SQL：{revisionMessage=}')
        return {"sql": revisionMessage[-1].content}
    except Exception as e:
        logger.error(f'Failed to analyze message:{e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
