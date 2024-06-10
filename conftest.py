import pytest
from utils.helpers import register_new_courier_and_return_login_password

@pytest.fixture(scope="session")
def courier():
    data = register_new_courier_and_return_login_password()
    yield data
