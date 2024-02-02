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
        logger.info(f"Тест проверяет пвз с id {point_id}")
        response = get_point(admin_auth, point_id)
        assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"
        assert PointGet.model_validate(response.json()["point"]), f"В пвз с id {point_id} полученный ответ не соответствует модели"

    def test_get_all_points(self, admin_auth):
        """Получить все ПВЗ без параметров (по умолчанию метод возвращает только активные ПВЗ)"""

        response = get_points_by_param(admin_auth)
        assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert point.active is True, "Не все полученные пвз активны"
        pagination = PointsPagination.model_validate(response.json()["pagination"])
        assert pagination.limit == 20, "Дефолтный лимит пагинации не равен 20"
        assert pagination.page == 1, "Дефолтная страница пагинации не равна 1"
        # тут нужно сделать запрос в базу, чтобы проверить count и total_pages

    def test_get_inactive_points(self, admin_auth):
        """Получить не активные ПВЗ"""

        response = get_points_by_param(admin_auth, {"active": "false"})
        assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert point.active is False, "Не все полученные пвз неактивны"

    def test_get_points_by_service(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по сервису.
        Здесь идет выборка по определенным сервисам, чтобы в ответ не приходил пустой список"""

        response = get_services(admin_auth, {"country_id": "1"})
        services_count = len(response.json())
        if services_count == 0:
            logger.info("В ответ пришло 0 сервисов, тест не был пройден")
            return

        services = {}
        for service in response.json():
            if service["name"] in ["BOXBERRY", "СДЭК", "FivePost", "Halva"]:
                services.update({service["id"]: service["name"]})
        logger.info(f"Тест проверяет сервисы {services}")

        for key in services.keys():
            service_id = str(key)
            response = get_points_by_param(admin_auth, {"service_id": service_id})
            assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"

            for item in response.json()["points"]:
                point = PointsGet.model_validate(item)
                assert point.service_id == service_id, (f"Id сервиса {point.service_id} в пвз {point.id} "
                                                        f"не равно искомому {service_id}")

    def test_get_points_by_region(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по региону
        Здесь идет выборка по определенным регионам, чтобы в ответ не приходил пустой список"""

        response = get_regions(admin_auth, {"country_id": "1"})
        regions = []
        for region in response.json()["regions"]:
            if region["name"] in ["Московская", "Ленинградская", "Ростовская", "Самарская"]:
                regions.append(region["id"])
        logger.info(f"Тест проверяет регионы с id {regions}")
        for region_id in regions:
            response = get_points_by_param(admin_auth, {"region_id": region_id})
            assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"
            for item in response.json()["points"]:
                point = PointsGet.model_validate(item)
                assert point.region_id == region_id, (f"Id региона {point.region_id} в пвз {point.id} "
                                                      f"не равно искомому {region_id}")

    def test_get_points_by_city(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по городу
        Здесь идет выборка по определенным городам, чтобы в ответ не приходил пустой список"""

        response = get_cities(admin_auth, {"country_id": "1"})
        cities = []
        for city in response.json()["cities"]:
            if city["name"] in ["Волгоград", "Челябинск", "Ростов-на-Дону", "Воронеж"]:
                cities.append(city["id"])
        logger.info(f"Тест проверяет города с id {cities}")
        for city_id in cities:
            response = get_points_by_param(admin_auth, {"city_id": city_id})
            assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"
            for item in response.json()["points"]:
                point = PointsGet.model_validate(item)
                assert point.city_id == city_id, (f"Id города {point.city_id} в пвз {point.id} "
                                                  f"не равно искомому {city_id}")

    def test_get_points_by_restaurant(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по складу
        Здесь добавлено условие, что список не должен быть пустым, потому что не все склады используются в пвз"""

        response = get_restaurants(admin_auth)
        restaurants_count = len(response.json()["restaurants"])
        if restaurants_count == 0:
            logger.info("В ответ пришло 0 пвз, тест не был пройден")
            return

        while True:
            num = random.randint(0, restaurants_count)
            restaurant_id = str(get_restaurants(admin_auth).json()["restaurants"][num]["id"])
            logger.info(f"Тест проверяет ресторан с id {restaurant_id}")
            response = get_points_by_param(admin_auth, {"restaurant_id": restaurant_id})
            assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"
            if len(response.json()["points"]) != 0:
                for item in response.json()["points"]:
                    point = PointsGet.model_validate(item)
                    assert point.restaurant_id == restaurant_id, (f"Id ресторана {point.restaurant_id} в пвз {point.id}"
                                                                  f" не равно искомому {restaurant_id}")
                break

    def test_get_points_by_search_address(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по поисковому слову в адресе
        Здесь берется рандомный адрес из полученного списка пвз и происходит поиск по этому адресу"""

        response = get_points_by_param(admin_auth, {"limit": "100"})
        points_count = len(response.json()["points"])
        if points_count == 0:
            logger.info("В ответ пришло 0 пвз, тест не был пройден")
            return

        num = random.randint(0, points_count)
        search_word = PointsGet.model_validate(response.json()["points"][num]).address
        logger.info(f"Тест проверяет адрес {search_word}")
        response = get_points_by_param(admin_auth, {"search": search_word})
        assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert search_word in point.address, f"В пвз {point.id} в адресе {point.address} нет слова {search_word}"

    def test_get_points_by_search_name(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по поисковому слову в названии
        Здесь берется рандомное название из полученного списка пвз и происходит поиск по этому названию"""

        response = get_points_by_param(admin_auth, {"limit": "100"})
        points_count = len(response.json()["points"])
        if points_count == 0:
            logger.info("В ответ пришло 0 пвз, тест не был пройден")
            return

        num = random.randint(0, points_count)
        search_word = PointsGet.model_validate(response.json()["points"][num]).name
        logger.info(f"Тест проверяет название {search_word}")
        response = get_points_by_param(admin_auth, {"search": search_word})
        assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"
        for item in response.json()["points"]:
            point = PointsGet.model_validate(item)
            assert search_word in point.name, f"В пвз {point.id} в названии {point.name} нет слова {search_word}"

    def test_get_points_by_country(self, admin_auth):
        """Получить ПВЗ, отфильтрованные по стране
        Поиск происходит по списку стран, в которых в данный момент подключена доставка"""

        response = get_countries(admin_auth)
        countries = {}
        for country in response.json()["countries"]:
            if country["name"] in ["Россия", "Беларусь", "Казахстан", "Армения"]:
                countries.update({country["id"]: country["name"]})
        logger.info(f"Тест проверяет страны {countries}")
        for key, value in countries.items():
            response = get_points_by_param(admin_auth, {"country_id": key})
            limit = PointsPagination.model_validate(response.json()["pagination"]).limit
            response = get_points_by_param(admin_auth, {"country_id": key, "flag": "true", "limit": limit})
            assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"
            for item in response.json()["points"]:
                point = PointGet.model_validate(item)
                assert point.country == value, f"В пвз {point.id} страна {point.country} отличается от искомой страны {value}"

        # тест падает потому что в России есть пвз Армении, Киргизии и пвз без страны, и в Казахстане есть пвз Киргизии

    def test_change_point(self, admin_auth):
        """Редактировать ПВЗ
        Получаем рандомный пвз, меняем его настройки на противоположные, проверяем, возвращаем всё обратно"""

        response = get_points_by_param(admin_auth, {"limit": "100"})
        num = random.randint(0, 99)
        point_id = response.json()["points"][num]["id"]
        logger.info(f"Тест проверяет пвз с id {point_id}")

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
        assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"

        response = get_point(admin_auth, point_id)
        assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"
        point = PointGet.model_validate(response.json()["point"])
        assert point.card == body.card, f"Значение card в пвз {point.card} не поменялось на значение {body.card}"
        assert point.cash == body.cash, f"Значение cash в пвз {point.cash} не поменялось на значение {body.cash}"
        assert point.active == body.active, f"Значение active в пвз {point.active} не поменялось на значение {body.active}"

        # возвращаем исходные значения
        body_2 = PointChange(
            card=card,
            cash=cash,
            active=active,
        )
        response = change_point(admin_auth, point_id, body_2)
        assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"

        response = get_point(admin_auth, point_id)
        assert response.status_code == 200, f"Код ответа = {response.status_code}, сообщение = {response.text}"
        point = PointGet.model_validate(response.json()["point"])
        assert point.card == body_2.card, f"Значение card в пвз {point.card} не поменялось на значение {body_2.card}"
        assert point.cash == body_2.cash, f"Значение cash в пвз {point.cash} не поменялось на значение {body_2.cash}"
        assert point.active == body_2.active, f"Значение active в пвз {point.active} не поменялось на значение {body_2.active}"
