import random
import string

def random_username(prefix: str = "user") -> str:

    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}_{suffix}"