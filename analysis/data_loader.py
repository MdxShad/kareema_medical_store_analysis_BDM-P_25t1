from __future__ import annotations
import io
import os
import pandas as pd

DEMO_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'KAREEMA MEDICAL STORE  - Sales_Data.csv')


def load_demo_data() -> pd.DataFrame:
    if os.path.exists(DEMO_CSV):
        return pd.read_csv(DEMO_CSV)
    raise FileNotFoundError('Demo dataset not found in data/.')


def load_csv_bytes(content: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(content))
