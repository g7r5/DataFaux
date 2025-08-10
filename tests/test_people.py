from datafaux.generators import people
import pandas as pd


def test_generate_default():
    df = people.generate_default(count=5, seed=123, locale="en_US")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5
    assert "email" in df.columns