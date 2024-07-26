from typing import Dict
import time
from datetime import timedelta, datetime, timezone
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt
from config import get_jwt_config

jwt_config = get_jwt_config()


def create_access_token(user_id: str) -> str:
    access_token_expires = timedelta(minutes=jwt_config['jwt_expiration'])
    if access_token_expires:
        expire = datetime.now(timezone.utc) + access_token_expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {
        "user_id": user_id,
        "expires": expire.timestamp()
    }
    token = jwt.encode(payload, jwt_config['jwt_secret'], algorithm=jwt_config['jwt_algorithm'])

    return token


def decode_jwt(token: str) -> dict:
    # try:
    # print(token)
    decoded_token = jwt.decode(token, jwt_config['jwt_secret'], algorithms=[jwt_config['jwt_algorithm']])
    return decoded_token if decoded_token["expires"] >= datetime.now(timezone.utc).timestamp() else None


    # except:
    #     return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid
