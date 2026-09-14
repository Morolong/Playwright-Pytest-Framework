import pytest

from pages.register_page import RegisterPage
from test_data.personal_details import DEFAULT_PERSONAL_DETAILS
from test_data.users import VALID_USER
from utils.random_data import random_username


@pytest.fixture(scope="session")
def base_url():
    return "https://parabank.parasoft.com/parabank/index.htm"


@pytest.fixture
def registered_user(page, base_url):
    
    username = random_username()
    password = VALID_USER["password"]

    user = {
        "username": username,
        "password": password,
    }

    page.goto(base_url)

    register_page = RegisterPage(page)

    register_page.register(
        personal_details=DEFAULT_PERSONAL_DETAILS,
        user=user,
    )

    register_page.expect_registration_success()

    return {
        "page": page,
        "username": username,
        "password": password,
    }