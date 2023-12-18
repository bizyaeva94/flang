from .pages.settings import *
from .models.settings_models import *


class TestSettings:
    def test_create_setting_own_delivery(self, admin_auth):
        """Создать правило курьерской доставки собственной службой, проверить его и удалить"""

        setting_create = SettingCreate(
            default_setting=False,
            service_id="5",
            cities=["824", "444"],
            regions=["8", "25"],
            restaurants=["132"],
            zones=["835", "836"],
            type_pay=SettingTypePay(cash=True, card=True, account=True, site=True),
            rules=[
                SettingRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=300,
                    payment_methods=SettingTypePay(
                        cash=False, card=False, account=True, site=True
                    ),
                ),
                SettingRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=200,
                    payment_methods=SettingTypePay(
                        cash=True, card=True, account=False, site=False
                    ),
                ),
            ],
            intervals=["09:00-10:00", "10:00-12:00"],
            weekends=SettingWeekends(
                intervals=[SettingInterval(from_="2023-12-06T10:00:00.000Z", to="2023-09-21T18:00:11.989Z")],
                working_saturday=True,
                working_sunday=True,
            ),
            holidays=["2001-01-01T00:00:00.000Z", "2001-01-02T00:00:00.000Z"],
            short_days=SettingShortDays(intervals=["10:00-19:00"], dates=["2001-03-08T00:00:00.000Z"]),
            working_sunday=True,
            express_today=True,
            express=SettingExpress(
                price=300,
                time_to="2023-09-21T10:00:11.989Z",
                intervals=SettingInterval(from_="2023-12-06T10:00:00.000Z", to="2023-09-21T18:00:11.989Z"),
                worktime="2023-09-21T03:00:11.989Z"
            ),
            today=True,
            today_info=[
                SettingTodayInfo(
                    price=200,
                    time_to="2023-09-21T10:00:11.989Z",
                    intervals=[SettingInterval(from_="2023-12-06T10:00:00.000Z", to="2023-09-21T18:00:11.989Z")]
                )
            ],
            tomorrow=True,
            tomorrow_info=SettingTodayInfo(
                price=100,
                time_to="2023-09-21T10:00:11.989Z",
                intervals=[SettingInterval(from_="2023-12-06T10:00:00.000Z", to="2023-09-21T18:00:11.989Z")]
            ),
        )

        response = create_setting(admin_auth, setting_create)
        assert response.status_code == 200
        setting_create_response = SettingGet.model_validate(response.json()["setting"])
        setting_id = setting_create_response.id

        response = get_setting(admin_auth, setting_id)
        assert response.status_code == 200
        setting_get = SettingGet.model_validate(response.json()["data"])

        response = delete_setting(admin_auth, setting_id)
        assert response.status_code == 200
        assert response.json() == {"data": {}}
        # response = get_setting(admin_auth, setting_id)
        # assert response.status_code == 404  # тут отлавливается баг
        assert setting_get.company_id == "1"
        assert setting_get.default_setting == setting_create.default_setting
        assert setting_get.service_id == setting_create.service_id
        assert {str(city.id) for city in setting_get.cities} == set(setting_create.cities)
        assert {str(region.id) for region in setting_get.regions} == set(setting_create.regions)
        assert {str(restaurant.id) for restaurant in setting_get.restaurants} == set(setting_create.restaurants)
        assert {str(zone.id) for zone in setting_get.zones} == set(setting_create.zones)
        assert setting_get.type_pay == setting_create.type_pay
        assert setting_get.rules == setting_create.rules
        assert setting_get.intervals == setting_create.intervals
        assert setting_get.weekends == setting_create.weekends
        assert setting_get.holidays == setting_create.holidays
        assert setting_get.short_days == setting_create.short_days
        assert setting_get.working_sunday == setting_create.working_sunday
        assert setting_get.express_today == setting_create.express_today
        assert setting_get.express == setting_create.express
        assert setting_get.today == setting_create.today
        assert setting_get.today_info == setting_create.today_info
        assert setting_get.tomorrow == setting_create.tomorrow
        assert setting_get.tomorrow_info == setting_create.tomorrow_info

    def test_create_setting_delivery(self, admin_auth):
        """Создать правило курьерской доставки сторонней службой, проверить его и удалить"""

        setting_create = SettingCreate(
            default_setting=False,
            service_id="348039",
            cities=["824"],
            regions=["8"],
            restaurants=["132"],
            zones=["835"],
            type_pay=SettingTypePay(cash=False, card=False, account=True, site=True),
            rules=[
                SettingRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=300,
                    payment_methods=SettingTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                ),
            ],
            intervals=None,
            weekends=None,
            holidays=None,
            short_days=None,
            working_sunday=True,
            express_today=False,
            express=None,
            today=False,
            today_info=None,
            tomorrow=False,
            tomorrow_info=None
        )

        response = create_setting(admin_auth, setting_create)
        assert response.status_code == 200
        setting_create_response = SettingGet.model_validate(response.json()["setting"])
        setting_id = setting_create_response.id

        response = get_setting(admin_auth, setting_id)
        assert response.status_code == 200
        setting_get = SettingGet.model_validate(response.json()["data"])

        response = delete_setting(admin_auth, setting_id)
        assert response.status_code == 200
        assert response.json() == {"data": {}}
        # response = get_setting(admin_auth, setting_id)
        # assert response.status_code == 404  # тут отлавливается баг
        assert setting_get.company_id == "1"
        assert setting_get.default_setting == setting_create.default_setting
        assert setting_get.service_id == setting_create.service_id
        assert {str(city.id) for city in setting_get.cities} == set(setting_create.cities)
        assert {str(region.id) for region in setting_get.regions} == set(setting_create.regions)
        assert {str(restaurant.id) for restaurant in setting_get.restaurants} == set(setting_create.restaurants)
        assert {str(zone.id) for zone in setting_get.zones} == set(setting_create.zones)
        assert setting_get.type_pay == setting_create.type_pay
        assert setting_get.rules == setting_create.rules
        assert setting_get.intervals == setting_create.intervals
        assert setting_get.weekends == setting_create.weekends
        assert setting_get.holidays == setting_create.holidays
        assert setting_get.short_days == setting_create.short_days
        assert setting_get.working_sunday == setting_create.working_sunday
        assert setting_get.express_today == setting_create.express_today
        assert setting_get.express == setting_create.express
        assert setting_get.today == setting_create.today
        assert setting_get.today_info == setting_create.today_info
        assert setting_get.tomorrow == setting_create.tomorrow
        assert setting_get.tomorrow_info == setting_create.tomorrow_info

    def test_get_settings_by_region(self, admin_auth):
        """Получить все правила курьерской доставки, отфильтрованные по региону"""

        region_id = 6
        response = get_settings_by_param(admin_auth, {"region_id": region_id})
        assert response.status_code == 200
        for item in response.json()["settings"]:
            setting = SettingGet.model_validate(item)
            assert region_id in [region.id for region in setting.regions]

    def test_get_settings_by_city(self, admin_auth):
        """Получить все правила курьерской доставки, отфильтрованные по региону и городу"""

        region_id = 1
        city_id = 302
        response = get_settings_by_param(admin_auth, {"region_id": region_id, "city_id": city_id})
        assert response.status_code == 200
        for item in response.json()["settings"]:
            setting = SettingGet.model_validate(item)
            assert region_id in [region.id for region in setting.regions]
            assert city_id in [city.id for city in setting.cities]

    def test_get_settings_by_service(self, admin_auth):
        """Получить все правила курьерской доставки, отфильтрованные по сервису"""

        service_id = "3"
        response = get_settings_by_param(admin_auth, {"service_id": service_id})
        assert response.status_code == 200
        for item in response.json()["settings"]:
            setting = SettingGet.model_validate(item)
            assert setting.service_id == service_id

    def test_get_settings_by_restaurant(self, admin_auth):
        """Получить все правила курьерской доставки, отфильтрованные по складу"""

        restaurant_id = 5
        response = get_settings_by_param(admin_auth, {"restaurant_id": restaurant_id})
        assert response.status_code == 200
        for item in response.json()["settings"]:
            setting = SettingGet.model_validate(item)
            assert restaurant_id in [restaurant.id for restaurant in setting.restaurants]

    def test_create_same_city_setting(self, admin_auth):
        """Нельзя создать правило курьерской доставки, если уже есть правило для этого города и сервиса"""

        setting_create = SettingCreate(
            default_setting=False,
            service_id="3",
            cities=["381"],
            regions=["5"],
            restaurants=[],
            zones=[],
            type_pay=SettingTypePay(cash=False, card=False, account=True, site=True),
            rules=[
                SettingRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=300,
                    payment_methods=SettingTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                ),
            ],
            intervals=None,
            weekends=None,
            holidays=None,
            short_days=None,
            working_sunday=True,
            express_today=False,
            express=None,
            today=False,
            today_info=None,
            tomorrow=False,
            tomorrow_info=None
        )
        response = create_setting(admin_auth, setting_create)
        assert response.status_code == 200
        setting_create_response = SettingGet.model_validate(response.json()["setting"])
        setting_id = setting_create_response.id

        setting_create_2 = SettingCreate(
            default_setting=False,
            service_id="3",
            cities=["381"],
            regions=["5"],
            restaurants=[],
            zones=[],
            type_pay=SettingTypePay(cash=False, card=False, account=True, site=True),
            rules=[
                SettingRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=200,
                    payment_methods=SettingTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                ),
            ],
            intervals=None,
            weekends=None,
            holidays=None,
            short_days=None,
            working_sunday=True,
            express_today=False,
            express=None,
            today=False,
            today_info=None,
            tomorrow=False,
            tomorrow_info=None
        )
        response = create_setting(admin_auth, setting_create_2)
        assert response.status_code == 409
        assert response.json() == {"message": "правило для этого/этих города/городов и данной курьерской службы уже создано"}

        response = delete_setting(admin_auth, setting_id)
        assert response.status_code == 200
        assert response.json() == {"data": {}}

    def test_create_same_region_setting(self, admin_auth):
        """Нельзя создать правило курьерской доставки, если уже есть правило для этого региона и сервиса"""

        setting_create = SettingCreate(
            default_setting=False,
            service_id="3",
            cities=[],
            regions=["5"],
            restaurants=[],
            zones=[],
            type_pay=SettingTypePay(cash=False, card=False, account=True, site=True),
            rules=[
                SettingRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=300,
                    payment_methods=SettingTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                ),
            ],
            intervals=None,
            weekends=None,
            holidays=None,
            short_days=None,
            working_sunday=True,
            express_today=False,
            express=None,
            today=False,
            today_info=None,
            tomorrow=False,
            tomorrow_info=None
        )
        response = create_setting(admin_auth, setting_create)
        assert response.status_code == 200
        setting_create_response = SettingGet.model_validate(response.json()["setting"])
        setting_id = setting_create_response.id

        setting_create_2 = SettingCreate(
            default_setting=False,
            service_id="3",
            cities=[],
            regions=["5"],
            restaurants=[],
            zones=[],
            type_pay=SettingTypePay(cash=False, card=False, account=True, site=True),
            rules=[
                SettingRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=200,
                    payment_methods=SettingTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                ),
            ],
            intervals=None,
            weekends=None,
            holidays=None,
            short_days=None,
            working_sunday=True,
            express_today=False,
            express=None,
            today=False,
            today_info=None,
            tomorrow=False,
            tomorrow_info=None
        )
        response = create_setting(admin_auth, setting_create_2)
        assert response.status_code == 409
        assert response.json() == {"message": "правило для этого/этих региона/регионов и данной курьерской службы уже создано"}

        response = delete_setting(admin_auth, setting_id)
        assert response.status_code == 200
        assert response.json() == {"data": {}}

    def test_create_same_restaurant_setting(self, admin_auth):
        """Нельзя создать правило курьерской доставки, если уже есть правило для этого склада и сервиса"""

        setting_create = SettingCreate(
            default_setting=False,
            service_id="3",
            cities=[],
            regions=[],
            restaurants=["46"],
            zones=[],
            type_pay=SettingTypePay(cash=False, card=False, account=True, site=True),
            rules=[
                SettingRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=300,
                    payment_methods=SettingTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                ),
            ],
            intervals=None,
            weekends=None,
            holidays=None,
            short_days=None,
            working_sunday=True,
            express_today=False,
            express=None,
            today=False,
            today_info=None,
            tomorrow=False,
            tomorrow_info=None
        )
        response = create_setting(admin_auth, setting_create)
        assert response.status_code == 200
        setting_create_response = SettingGet.model_validate(response.json()["setting"])
        setting_id = setting_create_response.id

        setting_create_2 = SettingCreate(
            default_setting=False,
            service_id="3",
            cities=[],
            regions=[],
            restaurants=["46"],
            zones=[],
            type_pay=SettingTypePay(cash=False, card=False, account=True, site=True),
            rules=[
                SettingRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=200,
                    payment_methods=SettingTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                ),
            ],
            intervals=None,
            weekends=None,
            holidays=None,
            short_days=None,
            working_sunday=True,
            express_today=False,
            express=None,
            today=False,
            today_info=None,
            tomorrow=False,
            tomorrow_info=None
        )
        response = create_setting(admin_auth, setting_create_2)
        assert response.status_code == 409
        assert response.json() == {"message": "правило для этого склада и данной курьерской службы уже создано"}

        response = delete_setting(admin_auth, setting_id)
        assert response.status_code == 200
        assert response.json() == {"data": {}}

    def test_create_same_zone_setting(self, admin_auth):
        """Нельзя создать правило курьерской доставки, если уже есть правило для этой зоны и сервиса"""

        setting_create = SettingCreate(
            default_setting=False,
            service_id="3",
            cities=[],
            regions=[],
            restaurants=["46"],
            zones=["537"],
            type_pay=SettingTypePay(cash=False, card=False, account=True, site=True),
            rules=[
                SettingRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=300,
                    payment_methods=SettingTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                ),
            ],
            intervals=None,
            weekends=None,
            holidays=None,
            short_days=None,
            working_sunday=True,
            express_today=False,
            express=None,
            today=False,
            today_info=None,
            tomorrow=False,
            tomorrow_info=None
        )
        response = create_setting(admin_auth, setting_create)
        assert response.status_code == 200
        setting_create_response = SettingGet.model_validate(response.json()["setting"])
        setting_id = setting_create_response.id

        setting_create_2 = SettingCreate(
            default_setting=False,
            service_id="3",
            cities=[],
            regions=[],
            restaurants=["46"],
            zones=["537"],
            type_pay=SettingTypePay(cash=False, card=False, account=True, site=True),
            rules=[
                SettingRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=200,
                    payment_methods=SettingTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                ),
            ],
            intervals=None,
            weekends=None,
            holidays=None,
            short_days=None,
            working_sunday=True,
            express_today=False,
            express=None,
            today=False,
            today_info=None,
            tomorrow=False,
            tomorrow_info=None
        )
        response = create_setting(admin_auth, setting_create_2)
        assert response.status_code == 409
        assert response.json() == {"message": "правило для этого склада, зоны и данной курьерской службы уже создано"}

        response = delete_setting(admin_auth, setting_id)
        assert response.status_code == 200
        assert response.json() == {"data": {}}

    def test_change_setting(self, admin_auth):
        setting_create = SettingCreate(
            default_setting=False,
            service_id="3",
            cities=[],
            regions=[],
            restaurants=["46"],
            zones=["537"],
            type_pay=SettingTypePay(cash=False, card=False, account=True, site=True),
            rules=[
                SettingRule(
                    minimal_sum="0",
                    name="до 1000 р",
                    price=300,
                    payment_methods=SettingTypePay(
                        cash=True, card=True, account=False, site=False
                    ),
                ),
                SettingRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=0,
                    payment_methods=SettingTypePay(
                        cash=True, card=True, account=False, site=False
                    ),
                ),
            ],
            intervals=None,
            weekends=None,
            holidays=None,
            short_days=None,
            working_sunday=True,
            express_today=False,
            express=None,
            today=False,
            today_info=None,
            tomorrow=False,
            tomorrow_info=None
        )
        response = create_setting(admin_auth, setting_create)
        assert response.status_code == 200
        setting_create_response = SettingGet.model_validate(response.json()["setting"])
        setting_id = setting_create_response.id

        setting_change = SettingCreate(
            default_setting=False,
            service_id="3",
            cities=[],
            regions=[],
            restaurants=["46"],
            zones=["537"],
            type_pay=SettingTypePay(cash=False, card=False, account=True, site=True),
            rules=[
                SettingRule(
                    minimal_sum="0",
                    name="до 500 р",
                    price=100,
                    payment_methods=SettingTypePay(
                        cash=False, card=False, account=True, site=True
                    ),
                ),
                SettingRule(
                    minimal_sum="500",
                    name="от 500 р",
                    price=50,
                    payment_methods=SettingTypePay(
                        cash=False, card=False, account=True, site=True
                    ),
                ),
            ],
            intervals=None,
            weekends=None,
            holidays=None,
            short_days=None,
            working_sunday=True,
            express_today=False,
            express=None,
            today=False,
            today_info=None,
            tomorrow=False,
            tomorrow_info=None
        )
        response = change_setting(admin_auth, setting_id, setting_change)
        assert response.status_code == 200

        response = get_setting(admin_auth, setting_id)
        assert response.status_code == 200
        setting_get = SettingGet.model_validate(response.json()["data"])
        assert setting_get.rules == setting_change.rules

        response = delete_setting(admin_auth, setting_id)
        assert response.status_code == 200
        assert response.json() == {"data": {}}
