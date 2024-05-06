from tortoise import fields

from app.base.models import BaseModel


class Role(BaseModel):
    name = fields.CharField(max_length=32)


class User(BaseModel):
    name = fields.CharField(max_length=64)
    email = fields.CharField(max_length=128, null=True)
    avatar = fields.CharField(max_length=255, null=True)
    phone = fields.CharField(max_length=16, null=True)
    is_active = fields.BooleanField(default=True)
    role = fields.ForeignKeyField(Role, related_name='users', on_delete=fields.RESTRICT, null=True)
