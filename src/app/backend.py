from fastapi import FastAPI,HTTPException
import json,os
from typing import List
from pydantic import BaseModel
from agents import ReqAnalyst,SQLGenerator,SQLRevision
from langchain_core.messages import HumanMessage,AIMessage
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
        os.environ['LANGCHAIN_TRACING_V2']='false'
        messages = [HumanMessage(content=msg) for msg in request.messages]
        resp = ReqAnalyst.invoke(messages)
        logger.debug(f'{resp=}')
        messages.append(resp)
        logger.debug(f'{resp.content=}')
        steps = json.loads(resp.content)
        logger.debug(f'{steps=}')
        sql = SQLGenerator.invoke(steps)
        logger.debug(f'{sql=}')
        messages.append(AIMessage(content=sql))
        fixmsg = SQLRevision.invoke(messages)
        logger.debug(f'{fixmsg=}')
        return {"sql":fixmsg[-1].content}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


