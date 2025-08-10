import pandas as pd
from datafaux.modes.testers import inject_errors
from datafaux.modes.streaming import people_stream


def test_inject_errors():
    df = pd.DataFrame([{"a": 1, "b": "x"} for _ in range(10)])
    df_err = inject_errors(df.copy(), error_rate=0.5)
    assert df_err.isnull().sum().sum() > 0 or any(df_err.applymap(lambda x: isinstance(x, dict)).sum())


def test_people_stream():
    gen = people_stream(count=200, chunksize=50)
    chunks = list(gen)
    assert len(chunks) == 4
    assert all(isinstance(c, pd.DataFrame) for c in chunks)