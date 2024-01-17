import requests
from config import *


def get_regions(headers: dict, params: dict = None):
    response = requests.get(
        f"{STAND_URL}/api/regions/",
        headers=headers,
        params=params
    )
    return response
