from fastapi import APIRouter
from openai import AsyncOpenAI, OpenAI

from app.openai.chat.schemas import OpenAIChatInputBody, OpenAIChatOuputBody

router = APIRouter(tags=["OpenAI 兼容平台整合接口"])


@router.post("/completions")
async def get_response(chat_input: OpenAIChatInputBody):
    client = AsyncOpenAI(
        api_key='sk-d87783ce4cea4e8fa7f964af8768aef5', # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
    )
    completion = await client.chat.completions.create(**chat_input.model_dump(exclude_none=True))
    return completion
