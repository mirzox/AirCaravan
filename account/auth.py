from fastapi import Depends, APIRouter, HTTPException, status, Form, Body
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Annotated
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError


from account.crud import get_user, get_user_with_password
from database import connect_db


from sqlalchemy.ext.asyncio import AsyncEngine

from auth_bearer import JWTBearer, create_access_token, decode_jwt
from account.schemas import Login, Token, TokenData, User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(db: AsyncEngine, username: str, password: str) -> bool | Login:
    user = await get_user_with_password(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(JWTBearer())], db: AsyncEngine = Depends(connect_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(**payload)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user._mapping


@router.post("/login/")
async def login(user: Login, db: AsyncEngine = Depends(connect_db)) -> Token:
    db_user = await authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(db_user.id)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me/", dependencies=[Depends(JWTBearer())])
async def me(user: Annotated[User, Depends(get_current_active_user)],  db: AsyncEngine = Depends(connect_db)) -> User:
    return user


# 
# @router.get("/test/", dependencies=[Depends(JWTBearer())])
# async def test_jwt():
#     return {"message": "Hello World"}


