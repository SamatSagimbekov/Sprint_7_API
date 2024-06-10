import pytest
import requests
import allure
from utils.helpers import generate_random_string, BASE_URL

class TestCourierLogin:

    @pytest.fixture(scope="class")
    def courier_credentials(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(f'{BASE_URL}/courier', json=payload)
        assert response.status_code == 201
        return {"login": login, "password": password}

    @allure.title("Авторизация курьера успешно")
    def test_courier_login(self, courier_credentials):
        response = requests.post(f'{BASE_URL}/courier/login', json=courier_credentials)
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Авторизация курьера с отсутствующими полями")
    def test_courier_login_missing_fields(self):
        credentials = {"login": generate_random_string(10)}
        response = requests.post(f'{BASE_URL}/courier/login', json=credentials)
        assert response.status_code == 400

    @allure.title("Авторизация курьера с неверными учетными данными")
    def test_courier_login_invalid_credentials(self):
        credentials = {"login": "invalid_login", "password": "invalid_password"}
        response = requests.post(f'{BASE_URL}/courier/login', json=credentials)
        assert response.status_code == 404
