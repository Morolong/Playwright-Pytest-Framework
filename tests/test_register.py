import pytest

from pages.register_page import RegisterPage
from test_data.users import VALID_USER
from test_data.personal_details import DEFAULT_PERSONAL_DETAILS
from utils.random_data import random_username


class TestRegister:

    def test_successful_registration(self, page, base_url):
        page.goto(base_url)
        register_page = RegisterPage(page)

        user = {
            "username": random_username(),
            "password": VALID_USER["password"],
        }

        register_page.register(
            personal_details=DEFAULT_PERSONAL_DETAILS,
            user=user,
        )

        register_page.expect_registration_success()

    def test_registration_fails_with_missing_required_field(self, page, base_url):
        page.goto(base_url)
        register_page = RegisterPage(page)

        missing_first_name = {
            **DEFAULT_PERSONAL_DETAILS,
            "first_name": "",
        }

        user = {
            "username": random_username(),
            "password": VALID_USER["password"],
        }

        register_page.go_to_register()
        register_page.fill_personal_details(missing_first_name)
        register_page.fill_credentials(user)
        register_page.submit_registration()

        register_page.expect_first_name_required_error()