# Simple Process Model Baseline

This project creates a first daytime baseline run for a simple carbon flux process model using FLUXNET2015 half-hourly eddy covariance data.

The first run is configured for the FI-Hyy site and the year 2012. The workflow keeps daytime records only, using `SW_IN_F > 20`, because daytime observations are the main focus of this baseline.

## Input Data

Place the raw FLUXNET2015 CSV file in:

```text
data/raw/
```

The workflow expects a CSV file containing these columns:

- `TIMESTAMP_START`
- `NEE_VUT_REF`
- `SW_IN_F`
- `TA_F`
- `VPD_F`

Missing FLUXNET values marked as `-9999` are converted to missing values before filtering.

## Model Variables

The baseline uses:

- `NEE_VUT_REF`: observed or processed net ecosystem exchange
- `SW_IN_F`: incoming shortwave radiation
- `TA_F`: gap-filled air temperature
- `VPD_F`: gap-filled vapor pressure deficit

## Baseline Equations

The model calculates:

```text
GPP_model = alpha * SW_IN_F * VPD_stomatal_scalar
RECO_model = R0 * exp(k * TA_F)
NEE_model = RECO_model - GPP_model
residual = NEE_VUT_REF - NEE_model
```

Default parameter values:

- `alpha = 0.02`
- `R0 = 2.0`
- `k = 0.05`
- `vpd_sensitivity = 0.05`

The `VPD_stomatal_scalar` term reduces modeled GPP as vapor pressure deficit increases.

## Output Files

Running the workflow creates:

- `data/processed/FI_Hyy_2012_daytime_clean.csv`
- `results/outputs/baseline_model_output_2012.csv`
- `results/metrics/baseline_metrics_2012.csv`
- `results/figures/nee_timeseries_2012.png`
- `results/figures/observed_vs_predicted_nee_2012.png`
- `results/figures/residuals_timeseries_2012.png`
- `results/figures/residuals_vs_swin_2012.png`
- `results/figures/residuals_vs_temperature_2012.png`
- `results/figures/residuals_vs_vpd_2012.png`

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the workflow from the project root:

```bash
python src/main.py
```
