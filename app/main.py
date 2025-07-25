from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from app.core.config import ResponseMiddleware
from app.core.config import TORTOISE_ORM
from app.core.config import auth_manager
from app.core.config import handler_api_errors

@asynccontextmanager
async def lifespan(app: FastAPI):
    await RegisterTortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=False
    ).init_orm()

    yield
    await Tortoise.close_connections()

def get_fastapi_app():
    app = FastAPI(lifespan=lifespan, openapi_version='3.1.0')

    # add middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ResponseMiddleware)

    # register exception
    auth_manager.handle_errors(app)

    # register routers
    from app.api.auth.router import router as auth_router
    app.include_router(auth_router)

    return app

app = get_fastapi_app() 