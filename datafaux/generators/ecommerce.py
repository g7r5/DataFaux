from ..utils.faker_helpers import get_faker
import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

PRODUCTS_SAMPLE = [
    {"sku": "SKU-1001", "name": "T-shirt", "price": 19.99},
    {"sku": "SKU-1002", "name": "Pants", "price": 49.90},
    {"sku": "SKU-1003", "name": "Sneakers", "price": 79.95},
    {"sku": "SKU-1004", "name": "Backpack", "price": 39.0},
]


def generate_default(count=100, customers_df=None, seed=None, locale="en_US"):
    fake = get_faker(locale, seed)

    if customers_df is None:
        customers_df = pd.DataFrame([{
            "customer_id": str(uuid.uuid4()),
            "name": fake.name(),
            "email": fake.safe_email(),
        } for _ in range(max(1, count // 3))])

    orders = []
    for _ in range(count):
        cust = customers_df.sample(1).iloc[0]
        nitems = random.randint(1, 4)
        items = []
        total = 0.0
        for _ in range(nitems):
            p = random.choice(PRODUCTS_SAMPLE)
            qty = random.randint(1, 5)
            items.append({"sku": p["sku"], "name": p["name"], "unit_price": p["price"], "qty": qty})
            total += p["price"] * qty
        orders.append({
            "order_id": str(uuid.uuid4()),
            "customer_id": cust["customer_id"],
            "order_date": (datetime.utcnow() - timedelta(days=random.randint(0, 365))).isoformat(),
            "items": items,
            "total": round(total, 2),
            "currency": "USD" if locale.startswith("en") else "EUR"
        })
    return pd.DataFrame(orders)


def generate_from_schema(schema, count=100, seed=None, locale="en_US"):
    # For now, reuses generate_default; in future versions, it will map the schema
    return generate_default(count=count, seed=seed, locale=locale)