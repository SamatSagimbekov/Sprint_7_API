import pytest


@pytest.fixture(scope="session")
def courier():
    from utils.helpers import register_new_courier_and_return_login_password
    data = register_new_courier_and_return_login_password()
    yield data

