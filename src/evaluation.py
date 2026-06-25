from pathlib import Path

import numpy as np
import pandas as pd


def calculate_rmse(observed, predicted):
    observed = np.asarray(observed, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    return float(np.sqrt(np.mean((observed - predicted) ** 2)))


def calculate_mae(observed, predicted):
    observed = np.asarray(observed, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    return float(np.mean(np.abs(observed - predicted)))


def calculate_r2(observed, predicted):
    observed = np.asarray(observed, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    ss_residual = np.sum((observed - predicted) ** 2)
    ss_total = np.sum((observed - np.mean(observed)) ** 2)

    if ss_total == 0:
        return float("nan")

    return float(1 - (ss_residual / ss_total))


def calculate_bias(observed, predicted):
    observed = np.asarray(observed, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    return float(np.mean(predicted - observed))


def evaluate_nee_model(
    df,
    output_path=Path("results") / "metrics" / "baseline_metrics_2012.csv",
):
    """Calculate and save metrics comparing modeled NEE with observed NEE."""
    output_path = Path(output_path)
    comparison = df[["NEE_VUT_REF", "NEE_model"]].dropna()

    observed = comparison["NEE_VUT_REF"]
    predicted = comparison["NEE_model"]

    metrics = {
        "RMSE": calculate_rmse(observed, predicted),
        "MAE": calculate_mae(observed, predicted),
        "R2": calculate_r2(observed, predicted),
        "Bias": calculate_bias(observed, predicted),
    }

    metrics_df = pd.DataFrame(
        {"metric": list(metrics.keys()), "value": list(metrics.values())}
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_df.to_csv(output_path, index=False)

    return metrics_df
