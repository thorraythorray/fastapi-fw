from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from app.exception import register_exception_handlers
from app.settings import ALLOW_CREDENTIALS, ALLOW_HEADERS, ALLOW_METHODS, ALLOW_ORIGINS, DATABASE_DB_URL


async def init_tortoise():
    await Tortoise.init(
        db_url=DATABASE_DB_URL,
        modules={'models': ['app.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


async def init_fastapi_app():
    app = FastAPI()

    register_exception_handlers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOW_ORIGINS,
        allow_credentials=ALLOW_CREDENTIALS,
        allow_methods=ALLOW_METHODS,
        allow_headers=ALLOW_HEADERS,
    )

    # app.include_router(router, prefix="/api")
