import random
import pandas as pd


def inject_errors(df: pd.DataFrame, error_rate: float = 0.05) -> pd.DataFrame:
    """
    Injects random errors into the DataFrame for testing purposes.

    Error types:
      - empty: None
      - wrong_type: unexpected structure
      - outlier: out-of-range value for numeric types
    """
    if df.empty:
        return df

    # Select indices to modify
    total_cells = len(df) * len(df.columns)
    n_errors = max(1, int(total_cells * error_rate))

    for _ in range(n_errors):
        idx = random.choice(df.index.tolist())
        col = random.choice(df.columns.tolist())
        kind = random.choice(["empty", "wrong_type", "outlier"])
        if kind == "empty":
            df.at[idx, col] = None
        elif kind == "wrong_type":
            df.at[idx, col] = "WRONG_TYPE_INJECTED"
        elif kind == "outlier":
            try:
                if pd.api.types.is_numeric_dtype(df[col]):
                    current = df[col].dropna()
                    if not current.empty:
                        df.at[idx, col] = current.max() * 1000
                    else:
                        df.at[idx, col] = 999999
                else:
                    df.at[idx, col] = "OUTLIER_VALUE"
            except Exception:
                df.at[idx, col] = None
    return df