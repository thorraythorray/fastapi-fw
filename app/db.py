from tortoise import Tortoise

from app.settings import settings


TORTOISE_ORM = {
    "connections": {"default": settings.mysql.default_dsn},
    "apps": {
        "aerich": {
            "models": ["aerich.models"],
            "default_connection": "default",  # 指定 Aerich 模型使用的默认连接
        },
        "admin": {
            "models": ["app.admin.models"],
            "default_connection": "default",
        },
    },
}


async def init_tortoise():
    await Tortoise.init(
        db_url=settings.mysql.default_dsn,
        modules={"admin": ["app.admin.models"]}
    )
    await Tortoise.generate_schemas()
