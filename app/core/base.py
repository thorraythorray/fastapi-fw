from pydantic import BaseModel, Field
from tortoise import fields, Model


class PaginationSchema(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1)


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
