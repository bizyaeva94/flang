from pydantic import Field, ConfigDict
from typing import List, Optional
from .base_models import CustomBaseModel


class PointTypePay(CustomBaseModel):
    """Способы оплаты для правила самовывоза"""

    cash: bool
    card: bool
    account: bool
    site: bool


class PointRule(CustomBaseModel):
    """Правило самовывоза"""

    minimal_sum: str | int
    name: str
    price: int
    payment_methods: PointTypePay


class PointCity(CustomBaseModel):
    """Город"""

    id: int
    name: str


class PointRegion(CustomBaseModel):
    """Регион"""

    id: int
    name: str


class PointRestaurant(CustomBaseModel):
    """Склад"""

    id: int
    name: str


class PointService(CustomBaseModel):
    """Служба доставки"""

    id: int
    name: str


class PointZone(CustomBaseModel):
    """Зоны склада"""

    id: int
    name: str


class CompanyPointCreate(CustomBaseModel):
    """Создание правила для самовывоза"""

    cities: Optional[List[str]] = None
    default_point: Optional[bool] = None
    regions: Optional[List[str]] = None
    restaurants: Optional[List[str]] = None
    rules: Optional[List[PointRule]] = None
    services: Optional[List[str]] = None
    zones: Optional[List[str]] = None


class CompanyPointGet(CompanyPointCreate):
    """Ответ при запросе правила самовывоза по id, поля добавляются к тем, что отправились при создании"""

    cities: Optional[List[PointCity]] = None
    regions: Optional[List[PointRegion]] = None
    restaurants: Optional[List[PointRestaurant]] = None
    services: Optional[List[PointService]] = None
    zones: Optional[List[PointZone]] = None
    id: int
    company_id: str
