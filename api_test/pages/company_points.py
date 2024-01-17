import requests
from config import *
from api_test.models.company_points_models import *


def create_company_point(headers: dict, data: CompanyPointCreate):
    """
    Создать правило самовывоза
    :param headers: токен
    :param data: тело запроса
    """

    response = requests.post(
        f"{STAND_URL}/api/courier_services/company_points",
        headers=headers,
        data=data.model_dump_json(),
    )
    return response


def get_company_point(headers: dict, point_id: int):
    """
    Получить правило самовывоза по его id
    :param headers: токен
    :param point_id: id правила
    """

    response = requests.get(
        f"{STAND_URL}/api/courier_services/company_points/{point_id}", headers=headers)
    return response


def change_company_point(headers: dict, point_id: int, data: CompanyPointCreate):
    """
    Изменить правило самовывоза
    :param headers: токен
    :param point_id: id правила
    :param data: тело запроса
    """

    response = requests.put(
        f"{STAND_URL}/api/courier_services/company_points/{point_id}",
        headers=headers,
        data=data.model_dump_json(),
    )
    return response


def delete_company_point(headers: dict, point_id: int):
    """
    Удалить правило самовывоза
    :param headers: токен
    :param point_id: id правила
    """

    response = requests.delete(
        f"{STAND_URL}/api/courier_services/company_points/{point_id}", headers=headers)
    return response


def get_company_points_by_param(headers: dict, params: dict = None):
    """
    Получить все правила самовывоза, отфильтрованные по квери-параметру
    :param headers: токен
    :param params: service_id / restaurant_id / search
    """

    response = requests.get(
        f"{STAND_URL}/api/courier_services/company_points/",
        headers=headers,
        params=params
    )
    return response

