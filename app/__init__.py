from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from app.exceptions import register_exception_handlers
from app.settings import TORTOISE_ORM, settings
from app.utils.security import auth_manager


def get_fastapi_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # init db
    async def init_tortoise():
        await Tortoise.init(
            config=TORTOISE_ORM,
        )
    app.add_event_handler("startup", init_tortoise)

    # register exception
    auth_manager.handle_errors(app)
    register_exception_handlers(app)

    # register routers
    from app.auth.api import router as auth_router
    app.include_router(auth_router, prefix="/admin")

    return app
