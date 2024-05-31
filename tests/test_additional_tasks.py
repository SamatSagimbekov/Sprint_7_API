import requests
from utils.helpers import register_new_courier_and_return_login_password, BASE_URL


def test_delete_courier_success():
    data = register_new_courier_and_return_login_password()
    login, password, _ = data
    login_response = requests.post(f'{BASE_URL}/courier/login', json={"login": login, "password": password})
    courier_id = login_response.json().get("id")
    delete_response = requests.delete(f'{BASE_URL}/courier/{courier_id}')
    assert delete_response.status_code == 200
    assert delete_response.json() == {"ok": True}


def test_delete_courier_no_id():
    response = requests.delete(f'{BASE_URL}/courier/')
    assert response.status_code == 400
    assert response.json() == {"message": "Недостаточно данных для удаления учетной записи"}


def test_delete_courier_invalid_id():
    response = requests.delete(f'{BASE_URL}/courier/invalid_id')
    assert response.status_code == 404
    assert response.json() == {"message": "Курьер не найден"}


def test_accept_order_success():
    courier_data = register_new_courier_and_return_login_password()
    login, password, _ = courier_data
    login_response = requests.post(f'{BASE_URL}/courier/login', json={"login": login, "password": password})
    courier_id = login_response.json().get("id")
    order_response = requests.post(f'{BASE_URL}/orders', json={"firstName": "Ivan", "lastName": "Ivanov", "address": "Some address", "metroStation": 4, "phone": "+7 800 355 35 35", "rentTime": 5, "deliveryDate": "2023-06-06", "comment": "Test comment"})
    order_id = order_response.json().get("track")
    accept_response = requests.put(f'{BASE_URL}/orders/accept/{order_id}', params={"courierId": courier_id})
    assert accept_response.status_code == 200
    assert accept_response.json() == {"ok": True}


def test_accept_order_missing_courier_id():
    order_response = requests.post(f'{BASE_URL}/orders', json={"firstName": "Ivan", "lastName": "Ivanov", "address": "Some address", "metroStation": 4, "phone": "+7 800 355 35 35", "rentTime": 5, "deliveryDate": "2023-06-06", "comment": "Test comment"})
    order_id = order_response.json().get("track")
    accept_response = requests.put(f'{BASE_URL}/orders/accept/{order_id}', params={})
    assert accept_response.status_code == 400
    assert accept_response.json() == {"message": "Недостаточно данных для принятия заказа"}


def test_accept_order_invalid_courier_id():
    order_response = requests.post(f'{BASE_URL}/orders', json={"firstName": "Ivan", "lastName": "Ivanov", "address": "Some address", "metroStation": 4, "phone": "+7 800 355 35 35", "rentTime": 5, "deliveryDate": "2023-06-06", "comment": "Test comment"})
    order_id = order_response.json().get("track")
    accept_response = requests.put(f'{BASE_URL}/orders/accept/{order_id}', params={"courierId": "invalid_id"})
    assert accept_response.status_code == 404
    assert accept_response.json() == {"message": "Курьер не найден"}


def test_accept_order_missing_order_id():
    courier_data = register_new_courier_and_return_login_password()
    login, password, _ = courier_data
    login_response = requests.post(f'{BASE_URL}/courier/login', json={"login": login, "password": password})
    courier_id = login_response.json().get("id")
    accept_response = requests.put(f'{BASE_URL}/orders/accept/', params={"courierId": courier_id})
    assert accept_response.status_code == 400
    assert accept_response.json() == {"message": "Недостаточно данных для принятия заказа"}


def test_accept_order_invalid_order_id():
    courier_data = register_new_courier_and_return_login_password()
    login, password, _ = courier_data
    login_response = requests.post(f'{BASE_URL}/courier/login', json={"login": login, "password": password})
    courier_id = login_response.json().get("id")
    accept_response = requests.put(f'{BASE_URL}/orders/accept/invalid_id', params={"courierId": courier_id})
    assert accept_response.status_code == 404
    assert accept_response.json() == {"message": "Заказ не найден"}


def test_get_order_by_number_success():
    order_response = requests.post(f'{BASE_URL}/orders', json={"firstName": "Ivan", "lastName": "Ivanov", "address": "Some address", "metroStation": 4, "phone": "+7 800 355 35 35", "rentTime": 5, "deliveryDate": "2023-06-06", "comment": "Test comment"})
    order_id = order_response.json().get("track")
    get_response = requests.get(f'{BASE_URL}/orders/track?t={order_id}')
    assert get_response.status_code == 200
    assert "order" in get_response.json()


def test_get_order_by_number_missing():
    get_response = requests.get(f'{BASE_URL}/orders/track')
    assert get_response.status_code == 400
    assert get_response.json() == {"message": "Недостаточно данных для поиска заказа"}


def test_get_order_by_number_invalid():
    get_response = requests.get(f'{BASE_URL}/orders/track?t=invalid_id')
    assert get_response.status_code == 404
    assert get_response.json() == {"message": "Заказ не найден"}
