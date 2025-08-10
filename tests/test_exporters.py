def test_save_parquet(tmp_path):
    df = pd.DataFrame([{"a":1,"b":"x"},{"a":2,"b":"y"}])
    out = tmp_path / "test.parquet"
    save_df(df, str(out), "parquet")
    assert out.exists()
import pandas as pd
from datafaux.utils.exporters import save_df
import os

def test_save_csv(tmp_path):
    df = pd.DataFrame([{"a":1,"b":"x"},{"a":2,"b":"y"}])
    out = tmp_path / "test.csv"
    save_df(df, str(out), "csv")
    assert out.exists()
    content = out.read_text(encoding="utf-8")
    assert "a,b" in content