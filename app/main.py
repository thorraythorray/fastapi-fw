from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from app.core.errors import register_exception_handlers
from settings.settings import settings


async def get_fastapi_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await Tortoise.init(
            db_url=settings.mysql.mysql_dsn,
            modules={'app_models': [
                'app.core.models',
            ]}
        )
        # Generate the schema
        await Tortoise.generate_schemas()


    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    # app.include_router(router, prefix="/api")

    return app


application = get_fastapi_app()
