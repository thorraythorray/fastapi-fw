import traceback

from fastapi import HTTPException, FastAPI
from starlette import status
from starlette.responses import JSONResponse
from tortoise.exceptions import BaseORMException, DoesNotExist, IntegrityError

from app.core.pagination import FailedResponseModel


class RequestError(HTTPException):
    def __init__(self, detail: str = 'Bad request') -> None:
        status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(status_code, detail)


class ServerError(HTTPException):
    def __init__(self, detail: str = 'Internal Server Error') -> None:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(status_code, detail)


class NotFound(HTTPException):
    def __init__(self, detail: str = 'Not found') -> None:
        status_code = status.HTTP_404_NOT_FOUND
        super().__init__(status_code, detail)


class AuthError(HTTPException):
    def __init__(self, detail: str = 'No Authentication') -> None:
        status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(status_code, detail)


class AuthForbbiden(HTTPException):
    def __init__(self, detail: str = 'Auth Error') -> None:
        status_code = status.HTTP_403_FORBIDDEN
        super().__init__(status_code, detail)


class ConflictError(HTTPException):
    def __init__(self, detail: str = 'Resource Conflict') -> None:
        status_code = status.HTTP_409_CONFLICT
        super().__init__(status_code, detail)


class ResourceInUseError(HTTPException):
    def __init__(self, detail: str = '资源正在使用中') -> None:
        status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(status_code, detail)


def handler_api_errors(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_, exc: HTTPException):
        traceback.print_exc()
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )

    @app.exception_handler(BaseORMException)
    async def tortoise_exception_handler(_, exc: BaseORMException):
        traceback.print_exc()
        if exc == DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
        elif exc == IntegrityError:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        err_msg = exc.args[0] if exc.args else exc.args
        failed_model = FailedResponseModel(msg=err_msg)
        return JSONResponse(
            status_code=status_code,
            content=failed_model.model_dump()
        )
