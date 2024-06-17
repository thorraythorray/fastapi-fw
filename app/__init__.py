from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from app.errors import register_exception_handlers
from app.settings import TORTOISE_ORM, settings
from app.auth import security_auth


async def init_tortoise():
    await Tortoise.init(
        config=TORTOISE_ORM,
    )
    await Tortoise.generate_schemas()


def get_fastapi_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", init_tortoise)

    security_auth.handle_errors(app)

    register_exception_handlers(app)

    from app.admin.routers import router as admin_router
    app.include_router(admin_router, prefix="/admin")

    return app
