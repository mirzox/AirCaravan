from typing_extensions import List, TypedDict, NotRequired, Optional
from pydantic import BaseModel, Field
from datetime import datetime, date
from partner.schemas import Partner


class CreateClient(BaseModel):
    id: Optional[int] = None
    firstname: str
    lastname: str
    patronymic: str
    birthdate: date
    passport: str
    issued_by: str
    issued_date: date
    expired_date: date
    address: str
    gender: str
    pinfl: str

    class Config:
        from_attributes = True
        # exaple result  to show in swagger
        json_schema_extra = {
            "example": {
                "id": 1,
                "firstname": "test",
                "lastname": "test",
                "patronymic": "test",
                "birthdate": "2024-06-22",
                "passport": "test",
                "issued_by": "test",
                "issued_date": "2024-06-22",
                "expired_date": "2024-06-22",
                "address": "test",
                "gender": "male",
                "pinfl": "test",
            }
        }


class Application(BaseModel):
    id: int
    departure: str
    country: str
    datefrom: date
    dateto: date
    passengers: int
    hotel: str
    operatorcode: int | None
    operatorname: str | None
    tourid: str | None
    tour: str
    partner: Partner
    # clients: List[int]
    status: str

    class Config:
        from_attributes = True
        # exaple result  to show in swagger
        json_schema_extra = {
            "example": {
                "id": 1,
                "departure": "test",
                "country": "test",
                "datefrom": "2024-06-22",
                "dateto": "2024-06-22",
                "passengers": 1,
                "hotel": "test",
                "tour": "test",
                "partner_id": 1,
                "status": "test",
            }
        }


class RetrieveApplication(BaseModel):
    id: int
    departure: str
    country: str
    datefrom: date
    dateto: date
    passengers: int
    hotel: str
    tour: str
    operatorcode: int | None
    operatorname: str | None
    tourid: str | None
    partner: Partner
    clients: List[CreateClient]
    status: str

    class Config:
        from_attributes = True
        # exaple result  to show in swagger
        json_schema_extra = {
            "example": {
                "id": 1,
                "departure": "test",
                "country": "test",
                "datefrom": "2024-06-22",
                "dateto": "2024-06-22",
                "passengers": 1,
                "hotel": "test",
                "tour": "test",
                "partner_id": 1,
                "status": "test",
            }
        }


class UpdateApplicationStatus(BaseModel):
    status: str


class CreateApplication(BaseModel):
    id: Optional[int] = None
    departure: str
    country: str
    datefrom: date
    dateto: date
    passengers: int
    hotel: str
    tour: str
    operatorcode: int
    operatorname: str
    tourid: str
    clients: List[CreateClient]

    class Config:
        from_attributes = True
        # exaple result  to show in swagger
        json_schema_extra = {
            "example": {
                "id": 1,
                "departure": "test",
                "country": "test",
                "datefrom": "2024-06-22",
                "dateto": "2024-06-22",
                "passengers": 1,
                "hotel": "test",
                "tour": "test",
                "clients": [
                    {
                        "firstname": "test",
                        "lastname": "test",
                        "patronymic": "test",
                        "birthdate": "2024-06-22",
                        "passport": "test",
                        "issued_by": "test",
                        "issued_date": "2024-06-22",
                        "expired_date": "2024-06-22",
                        "address": "test",
                        "gender": "male",
                        "pinfl": "121212121"
                    }
                ]
            }
        }

