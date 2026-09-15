import random
import string
from datetime import date


def random_username(prefix: str = "user") -> str:

    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}_{suffix}"

def random_loan_amount() -> int:
    return random.randint(1, 999)


def random_down_payment(loan_amount: int | None = None) -> int:
    if loan_amount is None:
        return random.randint(1, 100)

    max_down_payment = int(loan_amount * 0.90)

    if max_down_payment < 1:
        return 1

    return random.randint(1, max_down_payment)

def expected_loan_date() -> str:
    today = date.today()
    return f"{today.month}-{today.day}-{today.year}"