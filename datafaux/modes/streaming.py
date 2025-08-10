import pandas as pd
from ..utils.faker_helpers import get_faker
import random
from typing import Callable


def generate_stream(generator_func: Callable, out_path: str, *, count: int = 10000, chunksize: int = 1000,
                    fmt: str = "csv", **kwargs):
    """
    Generates data in streaming mode by calling `generator_func` which must accept (count, chunksize, **kwargs)
    and be iterable (yield DataFrame chunks).
    """
    import math
    try:
        from tqdm import tqdm
        use_tqdm = True
    except ImportError:
        use_tqdm = False

    total_chunks = math.ceil(count / chunksize)
    iterator = generator_func(count=count, chunksize=chunksize, **kwargs)
    if use_tqdm:
        iterator = tqdm(iterator, total=total_chunks, desc="Generating chunks")
    first_chunk = True
    for chunk in iterator:
        if fmt == "csv":
            chunk.to_csv(out_path, mode="a", header=first_chunk, index=False, encoding="utf-8")
        elif fmt == "json":
            chunk.to_json(out_path, orient="records", lines=True, force_ascii=False, mode="a")
        else:
            raise ValueError(f"Streaming not supported for format {fmt}")
        first_chunk = False


def people_stream(count=1000000, seed=None, locale="en_US", chunksize=1000):
    from ..utils.faker_helpers import get_faker
    fake = get_faker(locale, seed)
    import uuid
    from datetime import datetime

    produced = 0
    while produced < count:
        batch = []
        take = min(chunksize, count - produced)
        for _ in range(take):
            batch.append({
                "person_id": str(uuid.uuid4()),
                "name": fake.name(),
                "email": fake.safe_email(),
                "phone": fake.phone_number(),
                "address": fake.address().replace("\n", ", "),
                "age": random.randint(18, 80),
                "registered_at": fake.date_time_between(start_date='-3y', end_date='now').isoformat()
            })
        produced += take
        yield pd.DataFrame(batch)
