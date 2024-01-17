import requests
from config import *
from api_test.models import *


def create_courier(headers: dict, first_name: str):
    """
    Создать курьера
    :param headers: токен
    :param first_name: имя курьера
    """
    response = requests.post(
        f"{STAND_URL}/api/couriers",
        headers=headers,
        data=CourierCreate(first_name=first_name).model_dump_json(),
    )
    return response


def get_couriers(headers: dict, params: dict = None):
    """
    Получить список курьеров
    :param headers: токен
    :param params: квери-параметры для фильтрации
    """
    response = requests.get(
        f"{STAND_URL}/api/couriers",
        headers=headers,
        params=params,
    )
    return response


def get_courier(headers: dict, courier_id: int):
    """
    Получить информацию по одному курьеру
    :param headers: токен
    :param courier_id: id курьера
    """
    response = requests.get(
        f"{STAND_URL}/api/couriers/{courier_id}",
        headers=headers,
    )
    return response


def change_courier(headers: dict, courier_id: int):
    """
    Поменять данные курьера
    :param headers: токен
    :param courier_id: id курьера
    """
    response = requests.put(
        f"{STAND_URL}/api/couriers/{courier_id}",
        headers=headers,
        data=CourierChange().model_dump_json(),
    )
    return response


def delete_courier(headers: dict, courier_id: int):
    """
    Удалить курьера
    :param headers: токен
    :param courier_id: id курьера
    """
    response = requests.delete(
        f"{STAND_URL}/api/couriers/{courier_id}",
        headers=headers,
    )
    return response


def update_warehouse_return_schedule(headers: dict, courier_id: int):
    """
    Обновить информацию о перерывах курьера
    :param headers: токен
    :param courier_id: id курьера
    """
    response = requests.patch(
        f"{STAND_URL}/api/couriers/{courier_id}",
        headers=headers,
        data=CourierWarehouseReturnSchedule.model_dump_json(),
    )
    return response


def open_workday(headers: dict, courier_id: int):
    """
    Открыть смену курьера
    :param headers: токен
    :param courier_id: id курьера
    """
    response = requests.post(
        f"{STAND_URL}/api/couriers/{courier_id}/workdays",
        headers=headers,
    )
    return response


def close_workday(headers: dict, courier_id: int):
    """
    Закрыть смену курьера
    :param headers: токен
    :param courier_id: id курьера
    """
    response = requests.put(
        f"{STAND_URL}/api/couriers/{courier_id}/workdays",
        headers=headers,
    )
    return response


def get_workdays(headers: dict, courier_id: int = None):
    """
    Получить информацию о сменах курьера
    :param headers: токен
    :param courier_id: id курьера передает только админ
    """
    params = {"courier_id": courier_id} if courier_id else None
    response = requests.get(
        f"{STAND_URL}/api/couriers/workdays",
        headers=headers,
        params=params,
    )
    return response
