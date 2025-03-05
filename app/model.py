from typing import Any, TypeVar

from pydantic import BaseModel
from tortoise import fields, Model
from tortoise.models import MODEL

T = TypeVar('T', bound=BaseModel)


class BaseTimestampORM(Model):
    create_tm = fields.DatetimeField(auto_now_add=True)
    update_tm = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

    async def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k) and v:
                setattr(self, k, v)
        await self.save()


class SuccessResponseModel(BaseModel):
    code: int = 0
    msg: str = 'ok'
    data: Any = None


class FailedResponseModel(BaseModel):
    code: int = -1
    msg: str = 'failed'
