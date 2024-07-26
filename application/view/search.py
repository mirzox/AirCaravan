from fastapi import APIRouter, Depends, HTTPException
from application.params import SearchQuery, SearchStatus, ResultResponse, SearchCountinue, SearchStatusResponse
from sqlalchemy.ext.asyncio import AsyncEngine

import requests
from database import connect_db
from application import models
from config import get_tourvisor_credentials, get_departures

from application.view.application_view import get_partner_id
from utils import pre_process_status, pre_process_result

credentials = get_tourvisor_credentials()
router = APIRouter()


async def get_cbu_usd() -> float:
    response = requests.get("https://cbu.uz/ru/arkhiv-kursov-valyut/json/USD/")
    return float(response.json()[0]["Rate"]) + 200


async def change_price(price: int) -> float:
    percent = 1.5

    cbu_usd = await get_cbu_usd()
    new_price = (price * percent / 100 + price) * cbu_usd
    return new_price


@router.post("/search")
async def search_tours(query: SearchQuery, db: AsyncEngine = Depends(connect_db), partner_id: int = Depends(get_partner_id)):
    # print(await get_cbu_usd())
    base_url = "http://tourvisor.ru/xml/search.php"
    params = {
        "authlogin": credentials["login"],
        "authpass": credentials["password"],
        "format": "json",
        **query.model_dump(exclude_none=True)
    }

    response = requests.get(base_url, params=params)
    if response.json().get("error"):
        return response.json()
    print(response.json())
    await models.RequestId.create_request_id(db, response.json()['result'].get("requestid"), partner_id)

    return response.json()


@router.post("/continue")
async def countinue_search(query: SearchCountinue, partner_id: int = Depends(get_partner_id)):
    base_url = "http://tourvisor.ru/xml/search.php"
    params = {
        "authlogin": credentials["login"],
        "authpass": credentials["password"],
        "format": "json",
        **query.model_dump(exclude_none=True)
    }

    response = requests.get(base_url, params=params)
    return response.json()


@router.post("/status")
async def search_tours(query: SearchStatus, partner_id: int = Depends(get_partner_id)) -> SearchStatusResponse:
    base_url = "http://tourvisor.ru/xml/result.php"
    params = {
        "authlogin": credentials["login"],
        "authpass": credentials["password"],
        "format": "json",
        "type": "status",
        **query.model_dump(exclude_none=True)
    }

    response = requests.get(base_url, params=params)
    if response.json().get("error"):
        return response.json()
    data = response.json()
    data = await pre_process_status(data)
    return data


@router.post("/result")
async def search_result(query: ResultResponse, partner_id: int = Depends(get_partner_id)):
    base_url = "http://tourvisor.ru/xml/result.php"
    params = {
        "authlogin": credentials["login"],
        "authpass": credentials["password"],
        "format": "json",
        "type": "result",
        **query.model_dump(exclude_none=True)
    }

    response = requests.get(base_url, params=params)
    if response.json().get("error"):
        return response.json()
    data = response.json()
    data = await pre_process_result(data)
    return data


@router.get("/list")
async def search_result(type: str = "", partner_id: int = Depends(get_partner_id)):
    base_url = "http://tourvisor.ru/xml/list.php"
    params = {
        "authlogin": credentials["login"],
        "authpass": credentials["password"],
        "format": "json",
        "type": type,
    }

    response = requests.get(base_url, params=params)
    if response.json().get("error"):
        return response.json()
    data = response.json()
    if 'departures' in data.get('lists', {}).keys():
        departure = data['lists']['departures']["departure"]
        data['lists']['departures']["departure"] = [i for i in departure if i.get("name", '').lower() in get_departures()]
    return data

@router.get("/lists/id-by-country")
async def search_id_by_country(country: str, partner_id: int = Depends(get_partner_id)):
    base_url = "http://tourvisor.ru/xml/list.php"
    params = {
        "authlogin": credentials["login"],
        "authpass": credentials["password"],
        "format": "json",
        "type": 'country',
    }
    response = requests.get(base_url, params=params)
    if response.json().get("error"):
        return response.json()
    data = response.json()
    filtered_countries = list(filter(lambda x: country in x['name'], data['lists']['countries']['country']))
    if len(filtered_countries) == 0:
        raise HTTPException(status_code=400, detail=f'Country {country} not found')
    return {
        'id': filtered_countries[0]['id']
    }
