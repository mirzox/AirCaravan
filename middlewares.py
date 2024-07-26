# at the import level
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta

from partner.models import ApiKey
from database import connect_db


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        access_key = request.headers.get("access-key")
        # print(request.url.path)
        # if request.url.path in ["/partner/docs", "/partner/openapi.json"]:
        #     response = await call_next(request)
        #     return response

        if not access_key:
            return JSONResponse(content={"error": "Access key required"}, status_code=400)

        api_key = await ApiKey.check_api_key(await connect_db(), access_key)
        print(api_key)
        if not api_key:
            return JSONResponse(content={"error": "Invalid access key"}, status_code=401)

        response = await call_next(request)
        return response
