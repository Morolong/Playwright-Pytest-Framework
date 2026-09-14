from playwright.sync_api import Page, expect


class RegisterPage:

    def __init__(self, page: Page):
        self.page = page

        self.register_link = page.get_by_role("link", name="Register")

        self.first_name_input = page.locator("#customer\\.firstName")
        self.last_name_input = page.locator("#customer\\.lastName")
        self.street_input = page.locator("#customer\\.address\\.street")
        self.city_input = page.locator("#customer\\.address\\.city")
        self.state_input = page.locator("#customer\\.address\\.state")
        self.zip_code_input = page.locator("#customer\\.address\\.zipCode")
        self.phone_number_input = page.locator("#customer\\.phoneNumber")
        self.ssn_input = page.locator("#customer\\.ssn")
        self.username_input = page.locator("#customer\\.username")
        self.password_input = page.locator("#customer\\.password")
        self.repeat_password_input = page.locator("#repeatedPassword")
        self.register_button = page.get_by_role("button", name="Register")

        self.welcome_heading = page.get_by_role("heading", name="Welcome")
        self.error_heading = page.get_by_role("heading", name="Error!")
        self.first_name_required_error = page.get_by_text("First name is required.")

    def go_to_register(self):
        self.register_link.click()

    def fill_personal_details(self, personal_details):
        self.first_name_input.fill(personal_details["first_name"])
        self.last_name_input.fill(personal_details["last_name"])
        self.street_input.fill(personal_details["street"])
        self.city_input.fill(personal_details["city"])
        self.state_input.fill(personal_details["state"])
        self.zip_code_input.fill(personal_details["zip_code"])
        self.phone_number_input.fill(personal_details["phone"])
        self.ssn_input.fill(personal_details["ssn"])

    def fill_credentials(self, user):
        self.username_input.fill(user["username"])
        self.password_input.fill(user["password"])
        self.repeat_password_input.fill(user["password"])

    def submit_registration(self):
        self.register_button.click()

    def register(self, personal_details, user):
        self.go_to_register()
        self.fill_personal_details(personal_details)
        self.fill_credentials(user)
        self.submit_registration()

    def expect_registration_success(self):
        expect(self.welcome_heading).to_be_visible()

    def expect_first_name_required_error(self):
        expect(self.first_name_required_error).to_be_visible()