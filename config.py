from typing import Dict, Any
import os
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, 'DevScale-AirCaravan', ".env"))


def get_config() -> Dict[str, Any]:
    return {
        'db_host': os.environ['DB_HOST'],
        'db_user': os.environ['DB_USER'],
        'db_password': os.environ['DB_PASSWORD'],
        'db_name': os.environ['DB_NAME'],
    }


def get_jwt_config() -> Dict[str, Any]:
    return {
        'jwt_secret': os.environ['JWT_SECRET'],
        'jwt_algorithm': os.environ['JWT_ALGORITHM'],
        'jwt_expiration': int(os.environ['JWT_EXPIRATION'])
    }


def get_origins() -> list:
    origins = os.environ['ORIGINS']
    return eval(origins)


def get_tourvisor_credentials() -> Dict[str, Any]:
    return {
        'login': os.environ['TOURVISOR_LOGIN'],
        'password': os.environ['TOURVISOR_PASSWORD']
    }


def get_departures() -> list:
    departures = os.environ['DEPARTURES']
    return eval(departures)