from tortoise import fields, Model


class BaseOrmModel(Model):
    create_tm = fields.DateTimeField(auto_now_add=True)
    update_tm = fields.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
