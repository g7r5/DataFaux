import pandas as pd
from ..utils.faker_helpers import get_faker
import uuid
import random


def generate_default(count=100, seed=None, locale="en_US"):
    fake = get_faker(locale, seed)
    rows = []
    for _ in range(count):
        rows.append({
            "patient_id": str(uuid.uuid4()),
            "name": fake.name(),
            "dob": fake.date_of_birth(minimum_age=0, maximum_age=99).isoformat(),
            "gender": random.choice(["M","F","O"]),
            "last_visit": fake.date_time_between(start_date='-2y', end_date='now').isoformat(),
            "notes": fake.sentence(nb_words=8)
        })
    return pd.DataFrame(rows)