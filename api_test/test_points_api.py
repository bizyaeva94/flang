from .pages.points import *
from .models.points_models import *
import re


class TestPoints:
    def test_get_point(self, admin_auth):
        """Получить один ПВЗ"""

        point_id = 60727
        response = get_point(admin_auth, point_id)
        assert response.status_code == 200
        PointGet.model_validate(response.json()["point"])

    def test_get_all_points(self, admin_auth):
        """Получить все ПВЗ (по умолчанию метод возвращает только активные ПВЗ)"""

        response = get_points_by_param(admin_auth)
        assert response.status_code == 200
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert point.active is True
        pagination = PointsPagination.model_validate(response.json()["pagination"])
        assert pagination.limit == 20
        assert pagination.page == 1
        # тут нужно сделать запрос в базу, чтобы проверить count и total_pages

    def test_get_inactive_points(self, admin_auth):
        """Получить не активные ПВЗ"""

        response = get_points_by_param(admin_auth, {"active": "false"})
        assert response.status_code == 200
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert point.active is False
        pagination = PointsPagination.model_validate(response.json()["pagination"])
        assert pagination.limit == 20
        assert pagination.page == 1

    def test_get_points_by_service(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по сервису"""

        service_id = "3"
        response = get_points_by_param(admin_auth, {"service_id": service_id})
        assert response.status_code == 200
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert point.service_id == service_id

    def test_get_points_by_region(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по региону"""

        region_id = 4
        response = get_points_by_param(admin_auth, {"region_id": region_id})
        assert response.status_code == 200
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert point.region_id == region_id

    def test_get_points_by_city(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по городу"""

        city_id = 487
        response = get_points_by_param(admin_auth, {"city_id": city_id})
        assert response.status_code == 200
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert point.city_id == city_id

    def test_get_points_by_restaurant(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по складу"""

        restaurant_id = "5"
        response = get_points_by_param(admin_auth, {"restaurant_id": restaurant_id})
        assert response.status_code == 200
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert point.restaurant_id == restaurant_id

    def test_get_points_by_search_address(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по поисковому слову в адресе"""

        search = "химиков"
        response = get_points_by_param(admin_auth, {"search": search})
        assert response.status_code == 200
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert any(re.fullmatch(f".*{search}.*", street.lower()) for street in point.address.split()) is True

    def test_get_points_by_search_name(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по поисковому слову в названии"""

        search = "ом127742"
        response = get_points_by_param(admin_auth, {"search": search})
        assert response.status_code == 200
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert any(re.fullmatch(f".*{search}.*", name.lower()) for name in point.name.split()) is True

    def test_get_points_by_country(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по стране"""

        country = {"1": "Россия", "2": "Беларусь", "3": "Казахстан", "12": "Армения"}
        for key, value in country.items():
            response = get_points_by_param(admin_auth, {"country_id": key, "flag": "true", "limit": "6000"})
            assert response.status_code == 200
            for item in response.json()["points"]:
                point = PointGet.model_validate(item)
                assert point.country == value
                # тест падает потому что в России есть пвз Армении и пвз без страны, а в Казахстане есть пвз Киргизии

    def test_change_point(self, admin_auth):
        """Редактировать ПВЗ"""

        point_id = 60711
        body = PointChange(
            card=True,
            cash=True,
            active=True,
            restaurant_id="37",
            sklad="SKLAD_NN"
        )
        response = change_point(admin_auth, point_id, body)
        assert response.status_code == 200

        response = get_point(admin_auth, point_id)
        assert response.status_code == 200
        point = PointGet.model_validate(response.json()["point"])
        assert point.card == body.card
        assert point.cash == body.cash
        assert point.active == body.active
        assert point.restaurant_id == body.restaurant_id
        assert point.sklad == body.sklad

        body_2 = PointChange(
            card=False,
            cash=False,
            active=False,
            restaurant_id="39",
            sklad="SKLAD_CHBK"
        )
        response = change_point(admin_auth, point_id, body_2)
        assert response.status_code == 200

        response = get_point(admin_auth, point_id)
        assert response.status_code == 200
        point = PointGet.model_validate(response.json()["point"])
        assert point.card == body_2.card
        assert point.cash == body_2.cash
        assert point.active == body_2.active
        assert point.restaurant_id == body_2.restaurant_id
        assert point.sklad == body_2.sklad

        change_point(admin_auth, point_id, body)  # возвращаем исходные значения
