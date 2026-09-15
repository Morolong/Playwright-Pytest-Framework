from pages.login_page import LoginPage
from playwright.sync_api import expect

def test_valid_login(page, registered_user):
    username = registered_user["username"]
    password = registered_user["password"]

    login_page = LoginPage(page)

    login_page.log_out()

    login_page.goto()
    login_page.login(username, password)

    expect(page.get_by_role("heading", name="Accounts Overview")).to_be_visible()
