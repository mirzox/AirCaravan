from typing_extensions import List, TypedDict, NotRequired, Optional
from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    departure: str
    country: str
    datefrom: str
    dateto: str
    nightsfrom: str
    nightsto: str
    adults: str
    child: str
    childage1: Optional[str] = None
    childage2: Optional[str] = None
    childage3: Optional[str] = None
    stars: Optional[str] = None
    starsbetter: Optional[str] = None
    meal: Optional[str] = None
    mealbetter: Optional[str] = None
    rating: Optional[str] = None
    hotels: Optional[str] = None
    hoteltypes: Optional[str] = None
    pricetype: Optional[str] = None
    regions: Optional[str] = None
    subregions: Optional[str] = None
    operators: Optional[str] = None
    pricefrom: Optional[str] = None
    priceto: Optional[str] = None
    currency: Optional[str] = None
    hideregular: str
    services: Optional[str] = None

    class Config:
        json_schema_extra = {
            "title": "SearchQuery",
            "description": "Search query for tours",
            "exclude_none": True,
            "example": {
                "departure": "56",
                "country": "4",
                "datefrom": "03.07.2024",
                "dateto": "08.07.2024",
                "nightsfrom": "7",
                "nightsto": "14",
                "adults": "2",
                "child": "0",
                "hideregular": "1"
            }
        }


class SearchStatus(BaseModel):
    requestid: str
    # type: str = 'result'
    # page: Optional[str] = '1'
    # onpage: Optional[str] = '25'
    # nodescription: Optional[str] = '1'
    # operatorstatus: Optional[str] = '1'


class SearchStatusResponse(BaseModel):
    data: TypedDict('SearchStatusResponseData', {
        "status": TypedDict('SearchStatusResponseDataStatus', {
            "state": str,
            "progress": int,
            "requestid": int,
            "hotelsfound": int,
            "toursfound": int,
            "minprice": float | int,
            "maxprice": float | int ,
            "timepassed": int
        })
    })
    class Config:
        json_schema_extra = {
            "title": "SearchStatusResponse",
            "description": "Search status response",
            "example": {
             "data": {
                "status": {
                    "state": "finished",
                    "progress": 100,
                    "requestid": 7551155609,
                    "hotelsfound": 401,
                    "toursfound": 2174,
                    "minprice": 6101730,
                    "maxprice": 76886820,
                    "timepassed": 6
                    }
                }
            }
        }


class StatusResponse(BaseModel):
    state: str
    hotelsfound: str
    toursfound: str
    minprice: str
    progress: str
    timepassed: str
    operators: List[str]


class ResultResponse(BaseModel):
    requestid: str
    onpage: str = None
    page: str = None
    nodescription: str = None
    operatorstatus: str = None
    # hotelcode: str
    # price: str
    # countrycode: str
    # countryname: str
    # regioncode: str
    # regionname: str
    # subregioncode: str
    # hotelname: str
    # hotelstars: str
    # hotelrating: str = '0'
    # hoteldescription: Optional[str] = None
    # fulldesclink: str
    # reviewlink: str
    # picturelink: str
    # isphoto: str
    # iscoords: str
    # isdescription: str
    # isreviews: str
    # seadistance: str


class Hotel(BaseModel):
    operatorcode: str
    operatorname: str
    flydate: str
    nights: str
    price: str
    fuelcharge: str
    priceue: str
    placement: str
    adults: str
    child: str
    meal: str
    mealrussian: str
    room: str
    tourname: str
    tourlink: Optional[str] = None
    tourid: str
    currency: str
    regular: str
    promo: str
    onrequest: str
    flightstatus: str
    hotelstatus: str
    nightflights: str


class SearchCountinue(BaseModel):
    requestid: str
