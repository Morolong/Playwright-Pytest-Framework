class LoginPage: 
    def __init__(self, page): 
        self.page = page
        self.username_input = page.locator("input[name=\"username\"]")
        self.password_input = page.locator("input[name=\"password\"]")
        self.login_button = page.get_by_role("button", name="Log In")
        self.log_out_link = page.get_by_role("link", name="Log Out")

    def goto(self): 
        self.page.goto("https://parabank.parasoft.com/parabank/index.htm")

    def login(self, username: str, password: str): 
        self.username_input.fill(username)
        self.password_input.fill(password) 
        self.login_button.click()

    def log_out(self):
        self.log_out_link.click()