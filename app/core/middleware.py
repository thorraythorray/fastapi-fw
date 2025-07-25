import json
import traceback

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.config import config
from app.core.config import FailedResponseModel, SuccessResponseModel


class ResponseMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        url_pattern = request.url.path
        if response.headers.get("Content-Type") == "application/json" and url_pattern.startswith('/api'):

            if (url_pattern == config.LOGIN_URL and config.settings.debug) or \
                url_pattern in config.SKIP_RESPONSE_FORMAT_URLS:
                return response

            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            body = json.loads(response_body.decode())
            try:
                if 200 <= response.status_code < 300:
                    resp_model = SuccessResponseModel(data=body)
                else:  # 非200
                    resp_model = FailedResponseModel(msg=str(body))
            except Exception:
                traceback.print_exc()
                resp_model = FailedResponseModel(msg=str(body))
            finally:
                new_response = Response(
                    content=json.dumps(resp_model.model_dump()),
                    status_code=response.status_code,
                    media_type='application/json',
                )
            return new_response

        return response
