import requests
from config import *


def get_countries(headers: dict):
    response = requests.get(
        f"{STAND_URL}/api/countries/",
        headers=headers,
    )
    return response
