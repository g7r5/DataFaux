import pandas as pd
from ..utils.faker_helpers import get_faker
import random
import uuid


def generate_default(count=100, seed=None, locale="en_US"):
    fake = get_faker(locale, seed)
    rows = []
    for _ in range(count):
        rows.append({
            "transaction_id": str(uuid.uuid4()),
            "account_id": str(uuid.uuid4()),
            "amount": round(random.uniform(-1000, 10000), 2),
            "currency": "USD",
            "description": fake.sentence(nb_words=6),
            "timestamp": fake.date_time_between(start_date='-2y', end_date='now').isoformat()
        })
    return pd.DataFrame(rows)