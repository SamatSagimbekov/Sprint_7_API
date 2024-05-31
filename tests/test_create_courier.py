import requests
from utils.helpers import register_new_courier_and_return_login_password, BASE_URL


def test_create_courier():
    data = register_new_courier_and_return_login_password()
    assert data, "Failed to register a new courier"


def test_create_duplicate_courier():
    data = register_new_courier_and_return_login_password()
    login, password, first_name = data
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(f'{BASE_URL}/courier', json=payload)
    assert response.status_code == 409
    assert response.json() == {"message": "Этот логин уже используется. Попробуйте другой."}


def test_create_courier_missing_field():
    payload = {
        "login": "some_login",
        "password": "some_password"
    }
    response = requests.post(f'{BASE_URL}/courier', json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Недостаточно данных для создания учетной записи"}


def test_create_courier_success_response():
    data = register_new_courier_and_return_login_password()
    assert data, "Failed to register a new courier"
