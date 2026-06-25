from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "TIMESTAMP_START",
    "NEE_VUT_REF",
    "SW_IN_F",
    "TA_F",
    "VPD_F",
]

DEFAULT_PROCESSED_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "processed"
    / "FI_Hyy_2012_daytime_clean.csv"
)


def load_and_clean_fluxnet_data(
    raw_csv_path,
    output_path=DEFAULT_PROCESSED_PATH,
    year=2012,
    daytime_swin_threshold=20,
):
    """Load one FLUXNET2015 CSV file and save the cleaned daytime subset."""
    raw_csv_path = Path(raw_csv_path)
    output_path = Path(output_path)

    if not raw_csv_path.exists():
        raise FileNotFoundError(f"Raw CSV file not found: {raw_csv_path}")

    header = pd.read_csv(raw_csv_path, nrows=0)
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in header.columns
    ]
    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"CSV is missing required columns: {missing_text}")

    df = pd.read_csv(
        raw_csv_path,
        usecols=REQUIRED_COLUMNS,
        na_values=-9999,
        dtype={"TIMESTAMP_START": "string"},
    )
    df = df.replace(-9999, np.nan)

    timestamp_text = df["TIMESTAMP_START"].str.strip()
    df["TIMESTAMP_START"] = pd.to_datetime(
        timestamp_text,
        format="%Y%m%d%H%M",
        errors="coerce",
    )

    numeric_columns = ["NEE_VUT_REF", "SW_IN_F", "TA_F", "VPD_F"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=["TIMESTAMP_START"])
    df = df[df["TIMESTAMP_START"].dt.year == year]
    df = df[df["SW_IN_F"] > daytime_swin_threshold]
    df = df.dropna(subset=numeric_columns)

    df = df.sort_values("TIMESTAMP_START").reset_index(drop=True)
    df["year"] = df["TIMESTAMP_START"].dt.year
    df["month"] = df["TIMESTAMP_START"].dt.month
    df["day_of_year"] = df["TIMESTAMP_START"].dt.dayofyear
    df["hour"] = df["TIMESTAMP_START"].dt.hour + (
        df["TIMESTAMP_START"].dt.minute / 60.0
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    return df
