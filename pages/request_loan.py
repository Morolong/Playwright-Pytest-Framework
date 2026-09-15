from playwright.sync_api import Page, expect


class RequestLoanPage:

    def __init__(self, page: Page):
        self.page = page

        self.request_loan_link = page.get_by_role("link", name="Request Loan")

        self.amount_input = page.locator("#amount")
        self.down_payment_input = page.locator("#downPayment")
        self.apply_now_button = page.get_by_role("button", name="Apply Now")

        self.error_heading = page.get_by_role("heading", name="Error!")
        self.error_message = page.get_by_text("An internal error has")

        self.processed_heading = page.get_by_role(
            "heading",
            name="Loan Request Processed"
        )
        self.congrats_message = page.get_by_text(
            "Congratulations, your loan"
        )

        self.account_details_heading = page.get_by_role(
            "heading",
            name="Account Details"
        )
        self.balance_field = page.locator("#balance")
        self.available_balance_field = page.locator("#availableBalance")

    def go_to_request_loan(self):
        self.request_loan_link.click()

    def click_amount(self):
        self.amount_input.click()

    def fill_amount(self, amount: int | str):
        self.amount_input.click()
        self.amount_input.fill(str(amount))

    def click_down_payment(self):
        self.down_payment_input.click()

    def fill_down_payment(self, down_payment: int | str):
        self.down_payment_input.click()
        self.down_payment_input.fill(str(down_payment))

    def submit_application(self):
        self.apply_now_button.click()

    def apply_for_loan(
        self,
        amount: int | str = "",
        down_payment: int | str = "",
    ):
        self.go_to_request_loan()

        if amount:
            self.fill_amount(amount)
        else:
            self.click_amount()

        if down_payment:
            self.fill_down_payment(down_payment)
        else:
            self.click_down_payment()

        self.submit_application()

    def loan_result_row(
        self,
        loan_provider: str,
        date_text: str,
        status_text: str = "Approved",
    ):
        return {
            "provider": self.page.get_by_role(
                "cell",
                name=loan_provider
            ),
            "date": self.page.get_by_role(
                "cell",
                name=date_text
            ),
            "status": self.page.get_by_role(
                "cell",
                name=status_text
            ),
        }

    def new_account_link(self, account_number: str):
        return self.page.get_by_role("link", name=account_number)

    def open_new_loan_account(self, account_number: str):
        self.new_account_link(account_number).click()

    def expect_error(self):
        expect(self.error_heading).to_be_visible()
        expect(self.error_message).to_be_visible()

    def expect_loan_processed(self):
        expect(self.processed_heading).to_be_visible()

    def expect_loan_approved(
        self,
        loan_provider: str,
        date_text: str,
    ):
        row = self.loan_result_row(
            loan_provider,
            date_text,
            "Approved",
        )

        expect(row["provider"]).to_be_visible()
        expect(row["date"]).to_be_visible()
        expect(row["status"]).to_be_visible()
        expect(self.congrats_message).to_be_visible()

    def expect_account_details(self, account_number: str):
        expect(self.account_details_heading).to_be_visible()
        expect(
            self.page.get_by_role(
                "cell",
                name=account_number
            )
        ).to_be_visible()
        expect(
            self.page.get_by_role(
                "cell",
                name="LOAN"
            )
        ).to_be_visible()
        expect(self.balance_field).to_be_visible()
        expect(self.available_balance_field).to_be_visible()