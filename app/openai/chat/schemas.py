from typing import Dict, List, Optional, Union

from pydantic import BaseModel, confloat, conint

from .type import InputMessage, InputStreamOptions, InputTools, OutputChoices, OutputUsage


class OpenAIChatInputBody(BaseModel):
    messages: List[InputMessage]
    model: str
    frequency_penalty: Optional[confloat(gt=-2.0, lt=2.0)] = 0 # type: ignore # 控制模型生成文本的多样性和创新性,正相关
    logit_bias: Optional[Dict[str, int]] = None  # 影响模型在生成下一个词汇时的选择概率
    logprobs: Optional[bool] = False  # 返回每个输出令牌的日志概率，较高表明模型对该词的选择较为自信
    top_logprobs: Optional[conint(gt=0, lt=20)] = None  # type: ignore # logprobs must be set to true
    max_tokens: Optional[int] = None
    n: Optional[int] = 1  # 回复候选的数量
    presence_penalty: Optional[confloat(gt=-2.0, lt=2.0)] = 0  # type: ignore # 增加模型谈论新话题的可能性
    seed: Optional[int] = None
    stop: Union[str, List, None] = None
    stream: Optional[bool] = False
    stream_options: Optional[InputStreamOptions] = None
    # ether temperature or top_p
    temperature: Optional[confloat(gt=0, lt=2)] = 1  # type: ignore # 自由度
    top_p: Optional[float] = 1  # type: ignore # 自由度
    tools: Optional[List[InputTools]] = None
    tool_choice: Union[str, InputTools, None] = None
    parallel_tool_calls: Optional[bool] = True
    user: Optional[str] = None


class OpenAIChatOuputBody(BaseModel):
    id: str
    choices: List[OutputChoices]
    created: int
    service_tier: Optional[str] = None
    model: str
    system_fingerprint: str
    object: str
    usage: OutputUsage
