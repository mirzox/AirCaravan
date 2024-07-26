from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    is_active: int
    user_type: str

    class Config:
        from_attributes = True
        # exaple result  to show in swagger
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "test",
                "full_name": "test",
                "email": "",
                "is_active": 1,
                "user_type": "admin",
        }}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None
    expires: float | None = None
