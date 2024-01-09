from .pages.company_points import *
from .models.company_points_models import *


class TestCompanyPoints:
    def test_create_company_point(self, admin_auth):
        """Создать правило самовывоза, проверить его и удалить"""

        company_point = CompanyPointCreate(
            default_point=False,
            cities=["824", "444"],
            regions=["8", "25"],
            zones=["835", "836"],
            restaurants=["132"],
            services=["3"],
            rules=[
                PointRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=300,
                    payment_methods=PointTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                )
            ]
        )
        response = create_company_point(admin_auth, company_point)
        assert response.status_code == 200
        company_point_create_response = CompanyPointGet.model_validate(response.json()["setting"])
        company_point_id = company_point_create_response.id

        response = get_company_point(admin_auth, company_point_id)
        assert response.status_code == 200
        company_point_get = CompanyPointGet.model_validate(response.json()["data"])

        response = delete_company_point(admin_auth, company_point_id)
        assert response.status_code == 200
        assert response.json() == {"data": {}}

        assert company_point_get.company_id == "1"
        assert company_point_get.default_point == company_point.default_point
        assert {str(city.id) for city in company_point_get.cities} == set(company_point.cities)
        assert {str(region.id) for region in company_point_get.regions} == set(company_point.regions)
        assert {str(restaurant.id) for restaurant in company_point_get.restaurants} == set(company_point.restaurants)
        assert {str(zone.id) for zone in company_point_get.zones} == set(company_point.zones)
        assert {str(service.id) for service in company_point_get.services} == set(company_point.services)
        assert company_point_get.rules == company_point.rules

    def test_get_company_point_by_service(self, admin_auth):
        """Получить все правила самовывоза, отфильтрованные по сервису"""

        service_id = 3
        response = get_company_points_by_param(admin_auth, {"service_id": service_id})
        assert response.status_code == 200
        for item in response.json()["settings"]:
            company_point = CompanyPointGet.model_validate(item)
            assert service_id in [service.id for service in company_point.services]

    def test_get_company_point_by_restaurant(self, admin_auth):
        """Получить все правила самовывоза, отфильтрованные по складу"""

        restaurant_id = 37
        response = get_company_points_by_param(admin_auth, {"restaurant_id": restaurant_id})
        assert response.status_code == 200
        for item in response.json()["settings"]:
            company_point = CompanyPointGet.model_validate(item)
            assert restaurant_id in [restaurant.id for restaurant in company_point.restaurants]  # тест падает из-за бага

    def test_get_company_point_by_search(self, admin_auth):
        """Получить все правила самовывоза, отфильтрованные по поисковому слову"""

        search = "кемеровская"
        response = get_company_points_by_param(admin_auth, {"search": search})
        assert response.status_code == 200
        for item in response.json()["settings"]:
            company_point = CompanyPointGet.model_validate(item)
            assert search.lower() in [regions.name.lower() for regions in company_point.regions]

        search = "норильск"
        response = get_company_points_by_param(admin_auth, {"search": search})
        assert response.status_code == 200
        for item in response.json()["settings"]:
            company_point = CompanyPointGet.model_validate(item)
            assert search.lower() in [cities.name.lower() for cities in company_point.cities]

    def test_create_same_region_company_point(self, admin_auth):
        """Нельзя создать правило самовывоза, если уже есть правило для этого региона и сервиса"""

        company_point = CompanyPointCreate(
            default_point=False,
            cities=[],
            regions=["8", "25"],
            zones=[],
            restaurants=[],
            services=["3"],
            rules=[
                PointRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=300,
                    payment_methods=PointTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                )
            ]
        )
        response = create_company_point(admin_auth, company_point)
        assert response.status_code == 200
        company_point_create_response = CompanyPointGet.model_validate(response.json()["setting"])
        company_point_id = company_point_create_response.id

        company_point_2 = CompanyPointCreate(
            default_point=False,
            cities=[],
            regions=["8", "25"],
            zones=[],
            restaurants=[],
            services=["3", "348039"],
            rules=[
                PointRule(
                    minimal_sum="500",
                    name="от 500 р",
                    price=300,
                    payment_methods=PointTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                )
            ]
        )
        response = create_company_point(admin_auth, company_point_2)
        assert response.status_code == 409  # тест падает из-за бага
        assert response.json() == {"message": "правило для этого/этих региона/регионов и данной курьерской службы уже создано"}

        response = delete_company_point(admin_auth, company_point_id)
        assert response.status_code == 200
        assert response.json() == {"data": {}}

    def test_create_same_city_company_point(self, admin_auth):
        """Нельзя создать правило самовывоза, если уже есть правило для этого города и сервиса"""

        company_point = CompanyPointCreate(
            default_point=False,
            cities=["824", "444"],
            regions=[],
            zones=[],
            restaurants=[],
            services=["3"],
            rules=[
                PointRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=300,
                    payment_methods=PointTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                )
            ]
        )
        response = create_company_point(admin_auth, company_point)
        assert response.status_code == 200
        company_point_create_response = CompanyPointGet.model_validate(response.json()["setting"])
        company_point_id = company_point_create_response.id

        company_point_2 = CompanyPointCreate(
            default_point=False,
            cities=["444"],
            regions=[],
            zones=[],
            restaurants=[],
            services=["3"],
            rules=[
                PointRule(
                    minimal_sum="500",
                    name="от 500 р",
                    price=300,
                    payment_methods=PointTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                )
            ]
        )
        response = create_company_point(admin_auth, company_point_2)
        assert response.status_code == 409  # тест падает из-за бага
        assert response.json() == {"message": "правило для этого/этих города/городов и данной курьерской службы уже создано"}

        response = delete_company_point(admin_auth, company_point_id)
        assert response.status_code == 200
        assert response.json() == {"data": {}}

    def test_create_same_restaurant_company_point(self, admin_auth):
        """Нельзя создать правило самовывоза, если уже есть правило для этого склада и сервиса"""

        company_point = CompanyPointCreate(
            default_point=False,
            cities=[],
            regions=[],
            zones=[],
            restaurants=["132"],
            services=["3"],
            rules=[
                PointRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=300,
                    payment_methods=PointTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                )
            ]
        )
        response = create_company_point(admin_auth, company_point)
        assert response.status_code == 200
        company_point_create_response = CompanyPointGet.model_validate(response.json()["setting"])
        company_point_id = company_point_create_response.id

        company_point_2 = CompanyPointCreate(
            default_point=False,
            cities=[],
            regions=[],
            zones=[],
            restaurants=["132"],
            services=["3"],
            rules=[
                PointRule(
                    minimal_sum="500",
                    name="от 500 р",
                    price=300,
                    payment_methods=PointTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                )
            ]
        )
        response = create_company_point(admin_auth, company_point_2)
        assert response.status_code == 409  # тест падает из-за бага
        assert response.json() == {"message": "правило для этого склада и данной курьерской службы уже создано"}

        response = delete_company_point(admin_auth, company_point_id)
        assert response.status_code == 200
        assert response.json() == {"data": {}}

    def test_create_same_zone_company_point(self, admin_auth):
        """Нельзя создать правило самовывоза, если уже есть правило для этой зоны и сервиса"""

        company_point = CompanyPointCreate(
            default_point=False,
            cities=[],
            regions=[],
            zones=["835", "836"],
            restaurants=["132"],
            services=["3"],
            rules=[
                PointRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=300,
                    payment_methods=PointTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                )
            ]
        )
        response = create_company_point(admin_auth, company_point)
        assert response.status_code == 200
        company_point_create_response = CompanyPointGet.model_validate(response.json()["setting"])
        company_point_id = company_point_create_response.id

        company_point_2 = CompanyPointCreate(
            default_point=False,
            cities=[],
            regions=[],
            zones=["835"],
            restaurants=["132"],
            services=["3"],
            rules=[
                PointRule(
                    minimal_sum="500",
                    name="от 500 р",
                    price=300,
                    payment_methods=PointTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                )
            ]
        )
        response = create_company_point(admin_auth, company_point_2)
        assert response.status_code == 409  # тест падает из-за бага
        assert response.json() == {"message": "правило для этого склада, зоны и данной курьерской службы уже создано"}

        response = delete_company_point(admin_auth, company_point_id)
        assert response.status_code == 200
        assert response.json() == {"data": {}}

    def test_change_company_point(self, admin_auth):
        """Создать правило самовывоза, отредактировать, удалить"""

        company_point = CompanyPointCreate(
            default_point=False,
            cities=["824", "444"],
            regions=["8", "25"],
            zones=["835", "836"],
            restaurants=["132"],
            services=["3"],
            rules=[
                PointRule(
                    minimal_sum="1000",
                    name="от 1000 р",
                    price=300,
                    payment_methods=PointTypePay(
                        cash=False, card=False, account=True, site=True
                    )
                )
            ]
        )
        response = create_company_point(admin_auth, company_point)
        assert response.status_code == 200
        company_point_create_response = CompanyPointGet.model_validate(response.json()["setting"])
        company_point_id = company_point_create_response.id

        company_point_change = CompanyPointCreate(
            default_point=False,
            cities=["824", "444"],
            regions=["8", "25"],
            zones=["835", "836"],
            restaurants=["132"],
            services=["3"],
            rules=[
                PointRule(
                    minimal_sum="500",
                    name="от 500 р",
                    price=100,
                    payment_methods=PointTypePay(
                        cash=True, card=True, account=False, site=False
                    )
                )
            ]
        )

        response = change_company_point(admin_auth, company_point_id, company_point_change)
        assert response.status_code == 200

        response = get_company_point(admin_auth, company_point_id)
        assert response.status_code == 200
        company_point_get = CompanyPointGet.model_validate(response.json()["data"])
        assert company_point_get.rules == company_point_change.rules

        response = delete_company_point(admin_auth, company_point_id)
        assert response.status_code == 200
        assert response.json() == {"data": {}}
