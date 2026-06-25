from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def _save_figure(fig, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def plot_nee_timeseries(df, output_path):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(
        df["TIMESTAMP_START"],
        df["NEE_VUT_REF"],
        label="Observed NEE_VUT_REF",
        linewidth=0.9,
        alpha=0.8,
    )
    ax.plot(
        df["TIMESTAMP_START"],
        df["NEE_model"],
        label="Modeled NEE",
        linewidth=0.9,
        alpha=0.8,
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("NEE")
    ax.set_title("Daytime NEE Time Series, 2012")
    ax.legend()
    fig.autofmt_xdate()
    _save_figure(fig, output_path)


def plot_observed_vs_predicted(df, output_path):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(
        df["NEE_VUT_REF"],
        df["NEE_model"],
        s=10,
        alpha=0.45,
        edgecolors="none",
    )

    observed_min = df["NEE_VUT_REF"].min()
    predicted_min = df["NEE_model"].min()
    observed_max = df["NEE_VUT_REF"].max()
    predicted_max = df["NEE_model"].max()
    line_min = min(observed_min, predicted_min)
    line_max = max(observed_max, predicted_max)
    ax.plot([line_min, line_max], [line_min, line_max], color="black", linewidth=1)

    ax.set_xlabel("Observed NEE_VUT_REF")
    ax.set_ylabel("Predicted NEE_model")
    ax.set_title("Observed vs Predicted Daytime NEE, 2012")
    _save_figure(fig, output_path)


def plot_residuals_timeseries(df, output_path):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(
        df["TIMESTAMP_START"],
        df["residual"],
        linewidth=0.8,
        alpha=0.8,
    )
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xlabel("Date")
    ax.set_ylabel("Residual")
    ax.set_title("Residuals Over Time, 2012")
    fig.autofmt_xdate()
    _save_figure(fig, output_path)


def plot_residuals_vs_variable(df, variable, xlabel, output_path):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(
        df[variable],
        df["residual"],
        s=10,
        alpha=0.45,
        edgecolors="none",
    )
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Residual")
    ax.set_title(f"Residuals vs {xlabel}, 2012")
    _save_figure(fig, output_path)


def create_all_plots(df, figure_dir=Path("results") / "figures"):
    figure_dir = Path(figure_dir)

    plot_nee_timeseries(
        df,
        figure_dir / "nee_timeseries_2012.png",
    )
    plot_observed_vs_predicted(
        df,
        figure_dir / "observed_vs_predicted_nee_2012.png",
    )
    plot_residuals_timeseries(
        df,
        figure_dir / "residuals_timeseries_2012.png",
    )
    plot_residuals_vs_variable(
        df,
        "SW_IN_F",
        "SW_IN_F",
        figure_dir / "residuals_vs_swin_2012.png",
    )
    plot_residuals_vs_variable(
        df,
        "TA_F",
        "TA_F",
        figure_dir / "residuals_vs_temperature_2012.png",
    )
    plot_residuals_vs_variable(
        df,
        "VPD_F",
        "VPD_F",
        figure_dir / "residuals_vs_vpd_2012.png",
    )
