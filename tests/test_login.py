from pages.login_page import LoginPage
from playwright.sync_api import expect 
from test_data.users import VALID_USER

def test_valid_login(page): 
    login_page = LoginPage(page)

    login_page.goto()

    login_page.login(VALID_USER["username"], 
                     VALID_USER["password"]
                     )
    
    expect(page.get_by_role("heading", name="Accounts Overview")).to_be_visible()
