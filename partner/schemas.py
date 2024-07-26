from pydantic import BaseModel, RootModel
from typing import List, Optional


class Partner(BaseModel):
    id: int
    name: str
    phone: str
    is_active: int
    api_callback_url: str

    class Config:
        from_attributes = True
        # exaple result  to show in swagger
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "test",
                "phone": "test",
                "is_active": 1,
                "api_callback_url": "test",
                "api_key": "test",
            }}


class PartnerCreate(BaseModel):
    id: Optional[int] = None
    name: str
    phone: str
    is_active: int
    api_callback_url: str

    class Config:
        from_attributes = True
        # exaple result  to show in swagger
        json_schema_extra = {
            "example": {
                "name": "test",
                "phone": "test",
                "is_active": 1,
                "api_callback_url": "test",
            }}


class ListPartner(RootModel):
    root: List[Partner]

    class Config:
        from_attributes = True
        # exaple result  to show in swagger
        json_schema_extra = {
            "example": {
                "root": [
                    {
                        "id": 1,
                        "name": "test",
                        "phone": "test",
                        "is_active": 1,
                        "api_callback_url": "test",
                        "api_key": "test",
                    }
                ]
            }
        }


class PartnerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    api_callback_url: Optional[str] = None

    class Config:
        from_attributes = True
        # exaple result  to show in swagger
        json_schema_extra = {
            "example": {
                "name": "test",
                "phone": "test",
                "api_callback_url": "test",
            }}


class PartnerDelete(BaseModel):
    id: int

    class Config:
        from_attributes = True
        # exaple result  to show in swagger
        json_schema_extra = {
            "example": {
                "id": 1,
        }}


class ApiKey(BaseModel):
    id: int
    api_key: str
    is_active: int
