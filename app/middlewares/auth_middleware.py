from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.requests import Request
from app.modules.auth.service import verify_access_token


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/auth"):
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token:
            return Response("Unauthorized", status_code=401)

        try:
            token = token.split(" ")[1] if " " in token else token
            user = verify_access_token(token)
            request.state.user = user
        except Exception as e:
            return Response(str(e), status_code=401)

        response = await call_next(request)
        return response
