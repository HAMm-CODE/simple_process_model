from pathlib import Path

from data_cleaning import load_and_clean_fluxnet_data
from evaluation import evaluate_nee_model
from plotting import create_all_plots
from process_model import run_baseline_process_model


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DATA_PATH = ROOT_DIR / "data" / "processed" / "FI_Hyy_2012_daytime_clean.csv"
MODEL_OUTPUT_PATH = ROOT_DIR / "results" / "outputs" / "baseline_model_output_2012.csv"
METRICS_PATH = ROOT_DIR / "results" / "metrics" / "baseline_metrics_2012.csv"
FIGURE_DIR = ROOT_DIR / "results" / "figures"


def find_fluxnet_csv(raw_data_dir=RAW_DATA_DIR):
    """Find the first likely FLUXNET2015 CSV file inside data/raw."""
    raw_data_dir = Path(raw_data_dir)

    search_patterns = [
        "FLX_*FLUXNET2015*FULLSET*HH*.csv",
        "FLX_*FLUXNET2015*.csv",
        "*.csv",
    ]

    for pattern in search_patterns:
        matches = sorted(raw_data_dir.glob(pattern))
        if matches:
            return matches[0]

    raise FileNotFoundError(
        "No CSV file found in data/raw. Place the FLUXNET2015 half-hourly "
        "CSV file there and run: python src/main.py"
    )


def create_output_folders():
    folders = [
        RAW_DATA_DIR,
        PROCESSED_DATA_PATH.parent,
        MODEL_OUTPUT_PATH.parent,
        METRICS_PATH.parent,
        FIGURE_DIR,
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)


def main():
    create_output_folders()

    try:
        raw_csv_path = find_fluxnet_csv()
    except FileNotFoundError as error:
        print(error)
        return 1

    cleaned_df = load_and_clean_fluxnet_data(
        raw_csv_path=raw_csv_path,
        output_path=PROCESSED_DATA_PATH,
    )
    model_df = run_baseline_process_model(cleaned_df)

    MODEL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    model_df.to_csv(MODEL_OUTPUT_PATH, index=False)

    evaluate_nee_model(model_df, output_path=METRICS_PATH)
    create_all_plots(model_df, figure_dir=FIGURE_DIR)

    print("Baseline daytime process model run complete.")
    print(f"Cleaned daytime records: {len(cleaned_df)}")
    print(f"Model output CSV: {MODEL_OUTPUT_PATH}")
    print(f"Metrics CSV: {METRICS_PATH}")
    print(f"Figure folder: {FIGURE_DIR}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
