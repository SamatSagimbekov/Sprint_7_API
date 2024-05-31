import requests
from utils.helpers import BASE_URL


def test_get_orders():
    response = requests.get(f'{BASE_URL}/orders')
    assert response.status_code == 200
    assert "orders" in response.json()
