from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from app.core.config import TORTOISE_ORM
from app.core.error import handler_api_errors


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await RegisterTortoise(
        _app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=False
    ).init_orm()
    yield
    await Tortoise.close_connections()


def get_fastapi_app():
    application = FastAPI(lifespan=lifespan, openapi_version='3.1.0')
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # application.add_middleware(ResponseMiddleware)
    handler_api_errors(application)
    from app.api.auth.router import router as auth_router
    application.include_router(auth_router)
    return application


app = get_fastapi_app()
