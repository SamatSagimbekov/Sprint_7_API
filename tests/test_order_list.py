import requests
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'


class TestOrderList:

    @allure.title("Получение списка заказов успешно")
    def test_get_order_list(self):
        response = requests.get(BASE_URL)
        assert response.status_code == 200
        assert "orders" in response.json()
