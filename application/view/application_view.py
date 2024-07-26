from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi import Request, HTTPException
from fastapi_pagination import Page, add_pagination, paginate

from database import connect_db
from application import models
from application import schemas
from partner.models import ApiKey, Partner
from auth_bearer import JWTBearer
from utils import send_request_to_callback
from fastapi import BackgroundTasks

router = APIRouter()


async def get_partner_id(request: Request, db: AsyncEngine = Depends(connect_db)):
    partner_id = await ApiKey.get_partner_by_api_key(db, request.headers.get("access-key"))
    if partner_id is None:
        raise HTTPException(status_code=403, detail="Forbidden")
    return partner_id


@router.get("/",dependencies=[Depends(JWTBearer())])
async def get_applications(db: AsyncEngine = Depends(connect_db)) -> Page[schemas.Application]:
    data = await models.Application.get_all_applications(db)
    return data


@router.get("/{application_id}", dependencies=[Depends(JWTBearer())])
async def get_application(application_id: int, db: AsyncEngine = Depends(connect_db)) -> schemas.RetrieveApplication:
    data = await models.Application.get_application_by_id(db, application_id)
    return data


@router.post("/")
async def create_application(application: schemas.CreateApplication, db: AsyncEngine = Depends(connect_db), partner_id: int = Depends(get_partner_id)):
    data = await models.Application.create_application(db, application, partner_id)
    return {"application_id": data.id}


@router.put("/{application_id}", dependencies=[Depends(JWTBearer())])
async def change_status(application_id: int, status: schemas.UpdateApplicationStatus, background_tasks: BackgroundTasks, db: AsyncEngine = Depends(connect_db)):
    data = await models.Application.update_application_status(db, application_id, status=status.status)
    partner = await Partner.get_partner_by_id(db, data.partner_id)
    response = {
        "application_id": data.id,
        "status": data.status,
    }
    background_tasks.add_task(send_request_to_callback, partner.api_callback_url, response)
    return {"application_id": data.id}


@router.delete("/{application_id}", dependencies=[Depends(JWTBearer())])
async def delete_application(application_id: int, db: AsyncEngine = Depends(connect_db)):
    data = await models.Application.delete_application(db, application_id)
    return {"application_id": data.id}