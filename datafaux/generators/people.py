from faker import Faker
import pandas as pd
import random
import uuid
from ..utils.faker_helpers import get_faker

# default fields
DEFAULT_FIELDS = [
    ("person_id", "uuid"),
    ("name", "name"),
    ("email", "email"),
    ("phone", "phone_number"),
    ("address", "address"),
    ("age", "int"),
    ("registered_at", "datetime"),
]


def generate_default(count=100, seed=None, locale="en_US"):
    fake = get_faker(locale, seed)
    rows = []
    for _ in range(count):
        rows.append({
            "person_id": str(uuid.uuid4()),
            "name": fake.name(),
            "email": fake.safe_email(),
            "phone": fake.phone_number(),
            "address": fake.address().replace("\n", ", "),
            "age": random.randint(18, 80),
            "registered_at": fake.date_time_between(start_date='-3y', end_date='now').isoformat()
        })
    return pd.DataFrame(rows)


def generate_from_schema(schema, count=100, seed=None, locale="en_US"):
    fake = get_faker(locale, seed)
    fields = schema.get("fields") or []
    rows = []
    for _ in range(count):
        rec = {}
        for f in fields:
            fname = f.get("name")
            ftype = f.get("type")
            if ftype in ("name", "full_name"):
                rec[fname] = fake.name()
            elif ftype in ("email",):
                rec[fname] = fake.safe_email()
            elif ftype in ("address",):
                rec[fname] = fake.address().replace("\n", ", ")
            elif ftype in ("phone", "phone_number"):
                rec[fname] = fake.phone_number()
            elif ftype == "uuid":
                rec[fname] = str(uuid.uuid4())
            elif ftype == "int":
                rec[fname] = fake.random_int(min=f.get("min", 0), max=f.get("max", 100))
            elif ftype == "datetime":
                rec[fname] = fake.date_time_between(start_date=f.get("start", "-3y"), end_date="now").isoformat()
            else:
                rec[fname] = fake.word()
        rows.append(rec)
    return pd.DataFrame(rows)
