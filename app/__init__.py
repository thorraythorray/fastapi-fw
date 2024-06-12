from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from app.core.exception import register_exception_handlers
from app.config import ALLOW_ORIGINS, DATABASE_DB_URL


async def init_tortoise():
    await Tortoise.init(
        db_url=DATABASE_DB_URL,
        modules={'app_models': [
            'app.core.models',
        ]}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


async def create_fastapi_app():
    app = FastAPI()

    register_exception_handlers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.include_router(router, prefix="/api")

    return app
