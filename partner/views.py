from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, Form, Body, APIRouter
from sqlalchemy.orm import Session
from middlewares import AuthMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi_pagination import Page, add_pagination, paginate


from database import connect_db

from partner import schemas
from partner import models as mdl
from auth_bearer import JWTBearer

partner_app = APIRouter()

# partner_app.add_middleware(AuthMiddleware)


@partner_app.get("/", dependencies=[Depends(JWTBearer())])
async def get_partners(db: AsyncEngine = Depends(connect_db)) -> Page[schemas.Partner]:
    data = await mdl.Partner.get_all_partners(db)
    return data


@partner_app.get("/{partner_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.Partner)
async def get_partner(partner_id: int, db: AsyncEngine = Depends(connect_db)):
    data = await mdl.Partner.get_partner_by_id(db, partner_id)
    return data


@partner_app.post("/", dependencies=[Depends(JWTBearer())], response_model=schemas.PartnerCreate)
async def create_partner(partner: schemas.PartnerCreate, db: AsyncEngine = Depends(connect_db)) -> schemas.Partner:
    data = await mdl.Partner.create_partner(db, partner)
    return data


@partner_app.put("/{partner_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.PartnerUpdate)
async def update_partner(partner_id: int, partner: schemas.PartnerUpdate, db: AsyncEngine = Depends(connect_db)):
    data = await mdl.Partner.update_partner(db, partner_id, partner)
    return data


@partner_app.patch("/{partner_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.PartnerUpdate)
async def update_partner_partial(partner_id: int, partner: schemas.PartnerUpdate, db: AsyncEngine = Depends(connect_db)):
    data = await mdl.Partner.update_partner(db, partner_id, partner)
    return data


@partner_app.delete("/{partner_id}", dependencies=[Depends(JWTBearer())])
async def delete_partner(partner_id: int, db: AsyncEngine = Depends(connect_db)):
    partner = await mdl.Partner.get_partner_by_id(db, partner_id)
    # print(partner)
    if not partner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partner not found")

    await mdl.Partner.delete_partner(db, partner_id)
    return {"message": "Partner deleted successfully"}


@partner_app.post("/{partner_id}/deactivate", dependencies=[Depends(JWTBearer())], response_model=schemas.Partner)
async def deactivate_partner(partner_id: int, db: AsyncEngine = Depends(connect_db)):
    data = await mdl.Partner.deactivate_partner(db, partner_id)
    return data


@partner_app.post("/{partner_id}/activate", dependencies=[Depends(JWTBearer())], response_model=schemas.Partner)
async def deactivate_partner(partner_id: int, db: AsyncEngine = Depends(connect_db)):
    data = await mdl.Partner.activate_partner(db, partner_id)
    return data


@partner_app.post('/{partner_id}/api_key', dependencies=[Depends(JWTBearer())], response_model=schemas.ApiKey)
async def create_api_key(partner_id: int, db: AsyncEngine = Depends(connect_db)):
    data = await mdl.ApiKey.create_api_key(db, partner_id)
    return data
