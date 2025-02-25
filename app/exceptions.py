from typing import Union

from fastapi import HTTPException, FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


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


class DuplicatedError(HTTPException):
    def __init__(self, detail: str = 'Resource Conflict') -> None:
        status_code = status.HTTP_409_CONFLICT
        super().__init__(status_code, detail)

# 更改系统内置的异常处理，例如统一处理500的TemplateResponse
# app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)


# 自定义异常
class AppServiceError(Exception):
    def __init__(self, message: Union[str, None] = None) -> None:
        self.message = message or 'App Service Error'


# 处理自定义异常
def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppServiceError)
    def _(request: Request, exc: AppServiceError):
        return JSONResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=exc.message
        )
