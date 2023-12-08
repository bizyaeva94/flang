import time
from pydantic import Field
from typing import List, Optional
from random import choice

from .base_models import CustomBaseModel


class CourierHomeLocation(CustomBaseModel):
    """Адрес места финиша курьера, нужен в модели создания курьера"""

    address: Optional[str] = None
    lat: Optional[str] = None
    lon: Optional[str] = None


class CourierWarehouseReturnSchedule(CustomBaseModel):
    """Информация о перерывах курьера"""

    return_duration_s: Optional[int] = 1800
    from_time: Optional[str] = "2023-11-17T13:00:00.189Z"
    to_time: Optional[str] = "2023-11-17T14:00:00.422Z"


class CourierCreate(CustomBaseModel):
    """Все поля, которые могут участвовать при создании курьера. Где не указано Optional - это обязательные поля"""

    login: str = f"test{time.time()}".replace(".", "")  # генерируется уникальный логин
    password: str = "Pass1234"
    repeat_password: str = "Pass1234"
    phone: str = f"+79{choice([100000000, 999999999])}"  # генерируется уникальный телефон
    restaurant_id: str = "37"
    capacity: Optional[str] = None
    car: Optional[bool] = None
    email: Optional[str] = None
    external_id: Optional[str] = None
    first_name: Optional[str] = "Autotest"
    go_to_home: Optional[bool] = None
    go_to_sklad: Optional[bool] = None
    home: Optional[CourierHomeLocation] = None
    inn: Optional[str] = None
    interval_work: Optional[str] = None
    last_name: Optional[str] = ""
    lifting_capacity: Optional[str] = None
    localPasswordPay: Optional[str] = None
    login_pay: Optional[str] = None
    maximal_stops: Optional[str] = None
    middle_name: Optional[str] = ""
    zone_ids: Optional[List[int]] = None
    zone_names: Optional[List[str]] = None


class CourierChange(CourierCreate):
    """Поля, которые добавляются при редактировании курьера. Этих полей нет при создании"""

    blocked: Optional[bool] = None
    company_id: Optional[str] = None
    company_title: Optional[str] = None
    default: Optional[bool] = None
    device: Optional[str] = None
    firebaseIds: Optional[str] = None
    lastWorkDay: Optional[str] = None
    restaurant_address: Optional[str] = None
    restaurant_lat: Optional[str] = None
    restaurant_lon: Optional[str] = None
    restaurant_title: Optional[str] = None
    sklad: Optional[str] = None
    warehouse_return_schedule: Optional[CourierWarehouseReturnSchedule] = None


class CourierWorkday(CustomBaseModel):
    """Одна смена курьера (текущая или последняя)"""

    id: int
    from_: None | str = Field(alias="from")
    to: str | None
    courier_id: int
    plan_from: str | None
    plan_to: str | None


class CourierWorkdays(CustomBaseModel):
    """Все смены курьера (текущая и последняя)"""

    workday: CourierWorkday
    lastWorkDay: CourierWorkday

