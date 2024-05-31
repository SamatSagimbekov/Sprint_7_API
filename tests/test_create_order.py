import requests
from utils.helpers import BASE_URL


def test_create_order():
    payload = {
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "address": "Some address",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2023-06-06",
        "comment": "Test comment",
        "color": ["BLACK"]
    }
    response = requests.post(f'{BASE_URL}/orders', json=payload)
    assert response.status_code == 201
    assert "track" in response.json()
