import requests
from config import *
from .models import *
from .pages.courier import *


class TestCourier:
    courier_id = None
    first_name = f"autotest{time.time()}".replace(".", "")  # генерируется уникальное имя

    def test_courier(self, admin_auth):
        """Создание курьера, получение id из списка курьеров отфильтрованного по имени, удаление курьера"""

        response = create_courier(admin_auth, first_name=self.first_name)
        assert response.status_code == 200
        assert response.json() == {"message": "ok"}
        response = get_couriers(admin_auth, {"first_name": self.first_name})
        assert response.status_code == 200
        response = response.json()
        assert response["count"] > 0
        self.courier_id = response["couriers"][0]["id"]
        response = delete_courier(admin_auth, self.courier_id)
        assert response.status_code == 200
        assert response.json() == {"message": "ok"}

    def test_courier_workdays(self, courier_auth):
        """Открыть смену, проверить ее, закрыть смену, снова проверить"""

        courier_id = 449
        response = open_workday(courier_auth, courier_id)
        assert response.status_code == 200
        assert response.json() == {"message": "ok"}

        response = get_workdays(courier_auth, courier_id)
        assert response.status_code == 200
        data = CourierWorkdays.model_validate_json(response.text)
        assert data.workday.from_ is not None
        assert data.workday.to is None

        response = close_workday(courier_auth, courier_id)
        assert response.status_code == 200
        assert response.json() == {"message": "ok"}

        response = get_workdays(courier_auth, courier_id)
        assert response.status_code == 200
        data = CourierWorkdays.model_validate_json(response.text)
        assert data.workday.from_ is not None
        assert data.workday.to is not None
