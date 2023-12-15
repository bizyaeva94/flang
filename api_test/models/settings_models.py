from pydantic import Field, ConfigDict
from typing import List, Optional
from .base_models import CustomBaseModel


class SettingInterval(CustomBaseModel):
    """Интервал для экспресс-доставки, доставки сегодня и доставки завтра"""

    from_: str = Field(alias="from")
    to: str
    model_config = ConfigDict(populate_by_name=True)


class SettingTypePay(CustomBaseModel):
    """Способы оплаты для курьерского правила"""

    cash: bool
    card: bool
    account: bool
    site: bool


class SettingWeekends(CustomBaseModel):
    """Интервалы доставки в субботу и воскресенье"""

    intervals: List[SettingInterval]
    working_saturday: bool
    working_sunday: bool


class SettingShortDays(CustomBaseModel):
    """Интервалы доставки в праздничные дни"""

    intervals: List[str]
    dates: List[str]


class SettingRule(CustomBaseModel):
    """Правило доставки"""

    minimal_sum: str | int
    name: str
    price: int
    payment_methods: SettingTypePay


class SettingExpress(CustomBaseModel):
    """Настройки экспресс-доставки"""

    price: int
    time_to: str
    intervals: Optional[SettingInterval] = None
    worktime: Optional[str] = None
    working_sunday: Optional[bool] = None


class SettingTodayInfo(CustomBaseModel):
    """Настройки доставки сегодня"""

    price: int
    time_to: str
    intervals: Optional[List[SettingInterval]] = None


class SettingRegion(CustomBaseModel):
    """Регион"""

    id: int
    name: str


class SettingCity(CustomBaseModel):
    """Город"""

    id: int
    name: str


class SettingRestaurant(CustomBaseModel):
    """Склад"""

    id: int
    name: str


class SettingZone(CustomBaseModel):
    """Зоны доставки"""

    id: int
    name: str


class SettingCreate(CustomBaseModel):
    """Создание правила курьерской доставки. Обязательное поле только service_id"""

    default_setting: Optional[bool] = None
    service_id: str
    cities: Optional[List[str]] = None
    regions: Optional[List[str]] = None
    restaurants: Optional[List[str]] = None
    zones: Optional[List[str]] = None
    type_pay: Optional[SettingTypePay] = None
    rules: Optional[List[SettingRule]] = None
    intervals: Optional[List[str]] = None
    weekends: Optional[SettingWeekends] = None
    holidays: Optional[List[str]] = None
    short_days: Optional[SettingShortDays] = None
    working_sunday: Optional[bool] = None
    express_today: Optional[bool] = None
    express: Optional[SettingExpress] = None
    today: Optional[bool] = None
    today_info: Optional[List[SettingTodayInfo]] = None
    tomorrow: Optional[bool] = None
    tomorrow_info: Optional[SettingTodayInfo] = None


class SettingGet(SettingCreate):
    """Ответ при запросе правила курьерской доставки по id, поля добавляются к тем, что отправились при создании"""

    company_id: str
    id: int
    cities: Optional[List[SettingCity]] = None
    regions: Optional[List[SettingRegion]] = None
    restaurants: Optional[List[SettingRestaurant]] = None
    zones: Optional[List[SettingZone]] = None

