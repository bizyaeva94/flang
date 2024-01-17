import random
import logging

from .pages.points import *
from .pages.restaurants import get_restaurants
from .pages.services import get_services
from .pages.regions import get_regions
from .pages.company_cities import get_cities
from .pages.countries import get_countries
from .models.points_models import *


logger = logging.getLogger(__name__)


class TestPoints:
    def test_get_point(self, admin_auth):
        """Получить один ПВЗ
        Здесь берется рандомный пвз из списка первой сотни всех пвз"""

        response = get_points_by_param(admin_auth, {"limit": "100"})
        num = random.randint(0, 99)
        point_id = response.json()["points"][num]["id"]
        logger.info(point_id)
        response = get_point(admin_auth, point_id)
        assert response.status_code == 200
        PointGet.model_validate(response.json()["point"])

    def test_get_all_points(self, admin_auth):
        """Получить все ПВЗ без параметров (по умолчанию метод возвращает только активные ПВЗ)"""

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
        """Получить ПВЗ, отфильтрованные по сервису.
        Здесь идет выборка по определенным сервисам, чтобы в ответ не приходил пустой список"""

        response = get_services(admin_auth, {"country_id": "1"})
        services_count = len(response.json())
        if services_count == 0:
            return

        services = {}
        for service in response.json():
            if service["name"] in ["BOXBERRY", "СДЭК", "FivePost", "Halva"]:
                services.update({service["id"]: service["name"]})

        for key in services.keys():
            service_id = str(key)
            response = get_points_by_param(admin_auth, {"service_id": service_id})
            assert response.status_code == 200

            for item in response.json()["points"]:
                point = PointsGet.model_validate(item)
                assert point.service_id == service_id

    def test_get_points_by_region(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по региону
        Здесь идет выборка по определенным регионам, чтобы в ответ не приходил пустой список"""

        response = get_regions(admin_auth, {"country_id": "1"})
        regions = []
        for region in response.json()["regions"]:
            if region["name"] in ["Московская", "Ленинградская", "Ростовская", "Самарская"]:
                regions.append(region["id"])
        for region_id in regions:
            logger.info(f"region_id = {region_id}")
            response = get_points_by_param(admin_auth, {"region_id": region_id})
            assert response.status_code == 200
            for item in response.json()["points"]:
                point = PointsGet.model_validate(item)
                assert point.region_id == region_id

    def test_get_points_by_city(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по городу
        Здесь идет выборка по определенным городам, чтобы в ответ не приходил пустой список"""

        response = get_cities(admin_auth, {"country_id": "1"})
        cities = []
        for city in response.json()["cities"]:
            if city["name"] in ["Волгоград", "Челябинск", "Ростов-на-Дону", "Воронеж"]:
                cities.append(city["id"])
        for city_id in cities:
            logger.info(f"city_id = {city_id}")
            response = get_points_by_param(admin_auth, {"city_id": city_id})
            assert response.status_code == 200
            for item in response.json()["points"]:
                point = PointsGet.model_validate(item)
                assert point.city_id == city_id

    def test_get_points_by_restaurant(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по складу
        Здесь добавлено условие, что список не должен быть пустым, потому что не все склады используются в пвз"""

        response = get_restaurants(admin_auth)
        restaurants_count = len(response.json()["restaurants"])
        if restaurants_count == 0:
            return

        while True:
            num = random.randint(0, restaurants_count)
            restaurant_id = str(get_restaurants(admin_auth).json()["restaurants"][num]["id"])
            response = get_points_by_param(admin_auth, {"restaurant_id": restaurant_id})
            assert response.status_code == 200
            if len(response.json()["points"]) != 0:
                for item in response.json()["points"]:
                    point = PointsGet.model_validate(item)
                    assert point.restaurant_id == restaurant_id
                break

    def test_get_points_by_search_address(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по поисковому слову в адресе
        Здесь берется рандомный адрес из полученного списка пвз и происходит поиск по этому адресу"""

        response = get_points_by_param(admin_auth, {"limit": "100"})
        points_count = len(response.json()["points"])
        if points_count == 0:
            return

        num = random.randint(0, points_count)
        search_word = PointsGet.model_validate(response.json()["points"][num]).address
        response = get_points_by_param(admin_auth, {"search": search_word})
        assert response.status_code == 200
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert search_word in point.address

    def test_get_points_by_search_name(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по поисковому слову в названии
        Здесь берется рандомное название из полученного списка пвз и происходит поиск по этому названию"""

        response = get_points_by_param(admin_auth, {"limit": "100"})
        points_count = len(response.json()["points"])
        if points_count == 0:
            return

        num = random.randint(0, points_count)
        search_word = PointsGet.model_validate(response.json()["points"][num]).name
        response = get_points_by_param(admin_auth, {"search": search_word})
        assert response.status_code == 200
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert search_word in point.name

    def test_get_points_by_country(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по стране
        Поиск происходит по списку стран, в которых в данный момент подключена доставка"""

        response = get_countries(admin_auth)
        countries = {}
        for country in response.json()["countries"]:
            if country["name"] in ["Россия", "Беларусь", "Казахстан", "Армения"]:
                countries.update({country["id"]: country["name"]})
        for key, value in countries.items():
            response = get_points_by_param(admin_auth, {"country_id": key})
            limit = PointsPagination.model_validate(response.json()["pagination"]).limit
            response = get_points_by_param(admin_auth, {"country_id": key, "flag": "true", "limit": limit})
            assert response.status_code == 200
            for item in response.json()["points"]:
                point = PointGet.model_validate(item)
                assert point.country == value

        # тест падает потому что в России есть пвз Армении, Киргизии и пвз без страны, и в Казахстане есть пвз Киргизии

    def test_change_point(self, admin_auth):
        """Редактировать ПВЗ
        Получаем рандомный пвз, меняем его настройки на противоположные, проверяем, возвращаем всё обратно"""

        response = get_points_by_param(admin_auth, {"limit": "100"})
        num = random.randint(0, 99)
        point_id = response.json()["points"][num]["id"]
        logger.info(point_id)

        response = get_point(admin_auth, point_id)
        point = PointGet.model_validate(response.json()["point"])
        card = point.card
        cash = point.cash
        active = point.active
        logger.info(f"original card = {card}, cash = {cash}, active = {active}")

        body = PointChange(
            card=not card,
            cash=not cash,
            active=not active,
        )
        logger.info(f"changed body = {body}")
        response = change_point(admin_auth, point_id, body)
        assert response.status_code == 200

        response = get_point(admin_auth, point_id)
        assert response.status_code == 200
        point = PointGet.model_validate(response.json()["point"])
        assert point.card == body.card
        assert point.cash == body.cash
        assert point.active == body.active

        # возвращаем исходные значения
        body_2 = PointChange(
            card=card,
            cash=cash,
            active=active,
        )
        response = change_point(admin_auth, point_id, body_2)
        assert response.status_code == 200

        response = get_point(admin_auth, point_id)
        assert response.status_code == 200
        point = PointGet.model_validate(response.json()["point"])
        assert point.card == body_2.card
        assert point.cash == body_2.cash
        assert point.active == body_2.active
