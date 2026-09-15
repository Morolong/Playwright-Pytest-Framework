import pytest

from pages.request_loan import RequestLoanPage
from utils.random_data import (
    random_loan_amount,
    random_down_payment,
    expected_loan_date,
)


class TestRequestLoan:

    def test_loan_request_fails_with_no_amount(self, page, registered_user):
        loan_page = RequestLoanPage(page)

        loan_page.go_to_request_loan()
        loan_page.click_amount()
        loan_page.submit_application()

        loan_page.expect_error()

    def test_loan_request_fails_with_no_down_payment(self, page, registered_user):
        loan_page = RequestLoanPage(page)

        loan_page.go_to_request_loan()

        loan_amount = random_loan_amount()

        loan_page.fill_amount(str(loan_amount))
        loan_page.click_down_payment()
        loan_page.submit_application()

        loan_page.expect_error()

    def test_loan_request_approved_with_valid_data(self, page, registered_user):
        loan_page = RequestLoanPage(page)

        loan_amount = random_loan_amount()

        down_payment = random_down_payment(loan_amount)

        expected_date = expected_loan_date()

        loan_page.apply_for_loan(
            amount=loan_amount,
            down_payment=down_payment,
        )

        loan_page.expect_loan_processed()

        loan_page.expect_loan_approved(
            loan_provider="Wealth Securities Dynamic",
            date_text=expected_date,
        )

    def test_new_loan_account_details_are_displayed(self, page, registered_user):
        loan_page = RequestLoanPage(page)

        loan_amount = random_loan_amount()
        down_payment = random_down_payment(loan_amount)

        loan_page.apply_for_loan(
            amount=loan_amount,
            down_payment=down_payment,
        )

        loan_page.expect_loan_processed()