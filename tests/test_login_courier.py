import requests
from utils.helpers import register_new_courier_and_return_login_password, BASE_URL


def test_courier_login():
    data = register_new_courier_and_return_login_password()
    login, password, _ = data
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/courier/login', json=payload)
    assert response.status_code == 200
    assert "id" in response.json()


def test_courier_login_missing_field():
    payload = {
        "login": "some_login"
    }
    response = requests.post(f'{BASE_URL}/courier/login', json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Недостаточно данных для входа"}


def test_courier_login_invalid_credentials():
    payload = {
        "login": "invalid_login",
        "password": "invalid_password"
    }
    response = requests.post(f'{BASE_URL}/courier/login', json=payload)
    assert response.status_code == 404
    assert response.json() == {"message": "Учетная запись не найдена"}
