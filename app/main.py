from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.exception import register_exception_handlers
from app.settings import ALLOW_CREDENTIALS, ALLOW_HEADERS, ALLOW_METHODS, ALLOW_ORIGINS, DATABASE_DB_URL, origins


def create_app():
    app = FastAPI()

    register_exception_handlers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOW_ORIGINS,
        allow_credentials=ALLOW_CREDENTIALS,
        allow_methods=ALLOW_METHODS,
        allow_headers=ALLOW_HEADERS,
    )


    async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
        await Tortoise.init(
            db_url=DATABASE_DB_URL,
            modules={'models': ['app.models']}
        )
        # Generate the schema
        await Tortoise.generate_schemas()

    @app.on_event("startup")
    async def startup_event():
        await init()


    # register router
    # app.include_router(router, prefix="/api")
