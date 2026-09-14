import pytest
from pages.request_loan import RequestLoanPage

class TestRequestLoan:

    def test_loan_request_fails_with_no_amount(self, page):
        loan_page = RequestLoanPage(page)

        loan_page.go_to_request_loan()
        loan_page.click_amount()
        loan_page.submit_application()

        loan_page.expect_error()

    def test_loan_request_fails_with_no_down_payment(self, page):
        loan_page = RequestLoanPage(page)

        loan_page.go_to_request_loan()
        loan_page.fill_amount("1000")
        loan_page.click_down_payment()
        loan_page.submit_application()

        loan_page.expect_error()

    def test_loan_request_approved_with_valid_data(self, page):
        loan_page = RequestLoanPage(page)

        loan_page.apply_for_loan(amount="1500", down_payment="150")

        loan_page.expect_loan_processed()
        loan_page.expect_loan_approved(
            loan_provider="Wealth Securities Dynamic",
            date_text="-14-2026",
        )

    def test_new_loan_account_details_are_displayed(self, page):
        loan_page = RequestLoanPage(page)

        loan_page.apply_for_loan(amount="1500", down_payment="150")
        loan_page.expect_loan_processed()