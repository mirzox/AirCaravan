from typing import Dict
import datetime

import requests
from logging import getLogger

logger = getLogger(__name__)


def get_cbu_currency_rate() -> Dict[str, float]:
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    response = requests.get(f"https://cbu.uz/ru/arkhiv-kursov-valyut/json/all/{today}/")

    data = response.json()
    currencies = {}
    for currency in data:
        currencies[currency['Ccy']] = float(currency['Rate']) + 200
    currencies['BYR'] = currencies['BYN']
    return currencies


cbu_currencies = get_cbu_currency_rate()


async def change_price(price: int, currency: str) -> float:
    percent = 1.5

    cbu_currency = cbu_currencies[currency]
    new_price = (price * percent / 100 + price) * cbu_currency
    return new_price


async def pre_process_status(data: Dict) :
    data['data']['status']['minprice'] = await change_price(int(data['data']['status']['minprice']), "USD")
    data['data']['status']['maxprice'] = await change_price(int(data['data']['status']['maxprice']), "USD")
    return data


async def pre_process_result(data: Dict):
    try:
        data['data']['status']['minprice'] = await change_price(int(data['data']['status']['minprice']), "USD")
        data['data']['status']['maxprice'] = await change_price(int(data['data']['status']['maxprice']), "USD")

        for index in range(len(data['data']['result']['hotel'])):
            hotel = data['data']['result']['hotel'][index]
            data['data']['result']['hotel'][index]['price'] = await change_price(hotel['price'], hotel['currency'])
            data['data']['result']['hotel'][index]['currency'] = 'UZS'
            for tour_index in range(len(hotel['tours']['tour'])):
                tour = hotel['tours']['tour'][tour_index]
                data['data']['result']['hotel'][index]['tours']['tour'][tour_index]['price'] = await change_price(tour['price'],
                                                                                                            tour[
                                                                                                                'currency'])
                data['data']['result']['hotel'][index]['tours']['tour'][tour_index]['fuelcharge'] = await change_price(
                    tour['fuelcharge'], tour['currency'])
                data['data']['result']['hotel'][index]['tours']['tour'][tour_index]['priceue'] = await change_price(
                    tour['priceue'], tour['currency'])
                data['data']['result']['hotel'][index]['tours']['tour'][tour_index]['currency'] = 'UZS'
    except KeyError:
        logger.error("KeyError in pre_process_result")
    
    # for index in range(len(data['data']['result']['hotel'])):
    #     hotel = data['data']['result']['hotel'][index]
    #     for tour_index in range(len(hotel['tours']['tour'])):
    #         tour = hotel['tours']['tour'][tour_index]
    #         if tour['operatorcode'] in [25, 140, 93, 167] and hotel['countrycode'] == 4: # filter out FUN&SUN for Turkey
    #             del data['data']['result']['hotel'][index]['tours']['tour'][tour_index]

    return data


def send_request_to_callback(url: str, data: Dict):
    try:
        response = requests.post(url, json=data, timeout=30)
        logger.info(f"Callback response: {response.json()}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while sending request to callback: {e}")
        return None
    return response.json()
