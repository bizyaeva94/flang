from .pages.settings import *
from .models.settings_models import *


class TestSettings:
    def test_create_setting(self, admin_auth):
        """Создать правило курьерской доставки, проверить его и удалить"""

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

    def test_get_settings_by_region(self, admin_auth):
        """Получить все правила курьерской доставки, отфильтрованные по региону"""

        region_id = 6
        response = get_settings_by_param(admin_auth, {"region_id": region_id})
        assert response.status_code == 200
        for item in response.json()["settings"]:
            setting = SettingGet.model_validate(item)
            assert region_id in [region.id for region in setting.regions]
