from typing import List, Optional, Union
from typing_extensions import Literal, TypedDict, Required


class MessageToolCallsFunciton(TypedDict, total=True):
    name: str
    arguments: str


class MessageToolCalls(TypedDict, total=True):
    id: str
    type: Literal["function"]
    function: MessageToolCallsFunciton


class SystemMessage(TypedDict, total=False):
    content: Required[str]
    role: Required[Literal["system"]]
    name: str


class UserMessage(TypedDict, total=False):
    content: Required[str]
    role: Required[Literal["user"]]
    name: str


class AssistantMessage(TypedDict, total=False):
    content: str
    role: Required[Literal["assistant"]]
    name: str
    tool_calls: Optional[List[MessageToolCalls]]


class ToolMessage(TypedDict, total=False):
    content: Required[str]
    role: Required[Literal["tool"]]
    tool_call_id: Required[str]


class FunctionMessage(TypedDict, total=False):
    content: str
    role: Required[Literal["function"]]
    name: Required[str]


class ToolsFunction(TypedDict, total=False):
    description: Required[str]
    name: Required[str]
    parameters: dict


InputMessage = Union[
    SystemMessage,
    UserMessage,
    AssistantMessage,
    ToolMessage,
    FunctionMessage,
]


class InputTools(TypedDict, total=True):
    type: Literal["function"]
    function: ToolsFunction


class InputStreamOptions(TypedDict, total=False):
    include_usage = Optional[bool]


class CommonOuptutLogprob(TypedDict, total=False):
    token: Required[str]
    logprob: Required[str]
    bytes: List


class ChoicesLogprobsContent(CommonOuptutLogprob):
    top_logprobs: Required[List[CommonOuptutLogprob]]


class ChoicesLogprobs(TypedDict, total=False):
    content: List[ChoicesLogprobsContent]


class ChoicesMessage(TypedDict, total=False):
    content: str
    tool_calls: Required[List[MessageToolCalls]]
    role: Required[str]


class OutputChoices(TypedDict, total=False):
    finish_reason: Required[str]
    index: Required[int]
    message: Required[ChoicesMessage]
    logprobs: ChoicesLogprobs


class OutputUsage(TypedDict, total=True):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
