import pandas as pd
import json
from math import ceil


def save_df(df: pd.DataFrame, out_path: str, fmt: str = "csv") -> None:
    fmt = fmt.lower()
    if fmt == "csv":
        df.to_csv(out_path, index=False, encoding="utf-8")
    elif fmt == "json":
        df.to_json(out_path, orient="records", force_ascii=False, date_format="iso")
    elif fmt == "parquet":
        df.to_parquet(out_path, index=False)
    elif fmt in ("xlsx", "excel"):
        df.to_excel(out_path, index=False)
    else:
        raise ValueError(f"Format {fmt} not supported")


def save_df_stream(df: pd.DataFrame, out_path: str, fmt: str = "csv", chunksize: int = 1000) -> None:
    """
    Saves a large DataFrame in chunks (writes to disk without loading everything into memory at once).
    """
    n = len(df)
    parts = ceil(n / chunksize)
    first = True
    for i in range(parts):
        start = i * chunksize
        end = min(n, start + chunksize)
        part = df.iloc[start:end]
        if fmt == "csv":
            part.to_csv(out_path, mode="a", header=first, index=False, encoding="utf-8")
        elif fmt == "json":
            # lines=True for NDJSON
            part.to_json(out_path, orient="records", lines=True, force_ascii=False, mode="a")
        elif fmt == "parquet":
            # append parquet requires more work; creating files by part and then concatenating is out of scope
            part.to_parquet(f"{out_path}.part{i}.parquet", index=False)
        else:
            raise ValueError("Format not supported in save_df_stream")
        first = False