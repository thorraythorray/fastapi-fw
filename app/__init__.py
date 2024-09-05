from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from app.errors import register_exception_handlers
from app.settings import settings
from app.utils.security import auth_manager

TORTOISE_ORM = {
    "connections": {"default": settings.mysql.default_dsn},
    "apps": {
        "aerich": {
            "models": ["aerich.models"],
            "default_connection": "default",  # 指定 Aerich 模型使用的默认连接
        },
        "auth": {
            "models": [
                "app.auth.models",
            ],
            "default_connection": "default",
        },
    },
}


def get_fastapi_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    async def init_tortoise():
        await Tortoise.init(
            config=TORTOISE_ORM,
        )
        # 每次重启都会创建不存在的表，不利于数据库迁移管理，暂时去掉
        # await Tortoise.generate_schemas()

    app.add_event_handler("startup", init_tortoise)

    auth_manager.handle_errors(app)
    register_exception_handlers(app)

    from app.auth.api import router as auth_router
    from app.openai.api import router as openai_router
    app.include_router(auth_router, prefix="/admin")
    app.include_router(openai_router, prefix="/chat")

    return app
