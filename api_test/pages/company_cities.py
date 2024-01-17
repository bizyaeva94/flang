import requests
from config import *


def get_cities(headers: dict, params: dict = None):
    response = requests.get(
        f"{STAND_URL}/api/company_cities/",
        headers=headers,
        params=params
    )
    return response
