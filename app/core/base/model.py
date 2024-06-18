from tortoise import fields, Model


class TimestampModel(Model):
    create_tm = fields.DatetimeField(auto_now_add=True)
    update_tm = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
