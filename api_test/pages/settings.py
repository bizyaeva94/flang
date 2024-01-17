import requests
from config import *
from api_test.models.settings_models import *


def create_setting(headers: dict, data: SettingCreate):
    """
    Создать правило курьерской доставки
    :param headers: токен
    :param data: тело запроса
    """

    response = requests.post(
        f"{STAND_URL}/api/courier_services/settings",
        headers=headers,
        data=data.model_dump_json(),
    )
    return response


def get_setting(headers: dict, setting_id: int):
    """
    Получить правило курьерской доставки по его id
    :param headers: токен
    :param setting_id: id правила
    """

    response = requests.get(
        f"{STAND_URL}/api/courier_services/settings/{setting_id}", headers=headers)
    return response


def change_setting(headers: dict, setting_id: int, data: SettingCreate):
    """
    Изменить правило курьерской доставки
    :param data: тело запроса
    :param headers: токен
    :param setting_id: id правила
    """

    response = requests.put(
        f"{STAND_URL}/api/courier_services/settings/{setting_id}",
        headers=headers,
        data=data.model_dump_json(),
    )
    return response


def delete_setting(headers: dict, setting_id: int):
    """
    Удалить правило курьерской доставки
    :param headers: токен
    :param setting_id: id правила
    """

    response = requests.delete(
        f"{STAND_URL}/api/courier_services/settings/{setting_id}", headers=headers)
    return response


def get_settings_by_param(headers: dict, params: dict = None):
    """
    Получить все правила курьерской доставки, отфильтрованные по квери-параметру
    :param headers: токен
    :param params: service_id / region_id / city_id / restaurant_id
    """

    response = requests.get(
        f"{STAND_URL}/api/courier_services/settings/",
        headers=headers,
        params=params
    )
    return response
