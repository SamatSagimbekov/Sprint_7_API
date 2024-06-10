import requests
import allure
from utils.helpers import register_new_courier_and_return_login_password, BASE_URL

class TestDeleteCourier:

    @allure.title("Удаление курьера успешно")
    def test_delete_courier_success(self, courier):
        login_payload = {"login": courier["login"], "password": courier["password"]}
        login_response = requests.post(f'{BASE_URL}/login', json=login_payload)
        courier_id = login_response.json().get("id")

        delete_response = requests.delete(f'{BASE_URL}/courier/{courier_id}')
        assert delete_response.status_code == 200
        assert delete_response.json()["ok"] == True

    @allure.title("Удаление курьера без указания ID")
    def test_delete_courier_missing_id(self):
        delete_response = requests.delete(f'{BASE_URL}/courier')
        assert delete_response.status_code == 400

    @allure.title("Удаление несуществующего курьера")
    def test_delete_courier_nonexistent_id(self):
        delete_response = requests.delete(f'{BASE_URL}/courier/999999')
        assert delete_response.status_code == 404

class TestAcceptOrder:

    @allure.title("Принятие заказа успешно")
    def test_accept_order_success(self, courier):
        order_payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test street",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-06-01",
            "comment": "Test comment",
            "color": ["BLACK"]
        }
        order_response = requests.post(f'{BASE_URL}/orders', json=order_payload)
        order_track = order_response.json().get("track")

        login_payload = {"login": courier["login"], "password": courier["password"]}
        login_response = requests.post(f'{BASE_URL}/courier/login', json=login_payload)
        courier_id = login_response.json().get("id")

        accept_response = requests.put(
            f'{BASE_URL}/orders/accept/{order_track}',
            json={"courierId": courier_id}
        )
        assert accept_response.status_code == 200
        assert accept_response.json()["ok"] == True

    @allure.title("Принятие заказа без указания ID курьера")
    def test_accept_order_missing_courier_id(self):
        accept_response = requests.put(
            f'{BASE_URL}/orders/accept/1',
            json={}
        )
        assert accept_response.status_code == 400

    @allure.title("Принятие заказа с несуществующим ID курьера")
    def test_accept_order_invalid_courier_id(self):
        accept_response = requests.put(
            f'{BASE_URL}/orders/accept/1',
            json={"courierId": 999999}
        )
        assert accept_response.status_code == 404

    @allure.title("Принятие заказа без указания ID заказа")
    def test_accept_order_missing_order_id(self, courier):
        login_payload = {"login": courier["login"], "password": courier["password"]}
        login_response = requests.post(f'{BASE_URL}/courier/login', json=login_payload)
        courier_id = login_response.json().get("id")

        accept_response = requests.put(
            f'{BASE_URL}/orders/accept/',
            json={"courierId": courier_id}
        )
        assert accept_response.status_code == 400

class TestGetOrderByTrack:

    @allure.title("Получение заказа по номеру трека")
    def test_get_order_by_track(self):
        order_payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test street",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-06-01",
            "comment": "Test comment",
            "color": ["BLACK"]
        }
        order_response = requests.post(f'{BASE_URL}/orders', json=order_payload)
        order_track = order_response.json().get("track")

        get_response = requests.get(f'{BASE_URL}/orders/track?t={order_track}')
        assert get_response.status_code == 200
        assert "order" in get_response.json()

    @allure.title("Получение заказа без номера трека")
    def test_get_order_by_track_missing_track(self):
        get_response = requests.get(f'{BASE_URL}/orders/track')
        assert get_response.status_code == 400

    @allure.title("Получение заказа по несуществующему номеру трека")
    def test_get_order_by_track_nonexistent(self):
        get_response = requests.get(f'{BASE_URL}/orders/track?t=999999')
        assert get_response.status_code == 404
