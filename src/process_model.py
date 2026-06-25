import numpy as np


def run_baseline_process_model(
    df,
    alpha=0.02,
    R0=2.0,
    k=0.05,
    vpd_sensitivity=0.05,
):
    """Run a simple daytime carbon flux model with VPD limitation on GPP."""
    model_df = df.copy()

    vpd_for_scaling = model_df["VPD_F"].clip(lower=0)
    model_df["VPD_stomatal_scalar"] = np.exp(-vpd_sensitivity * vpd_for_scaling)

    model_df["GPP_model"] = (
        alpha * model_df["SW_IN_F"] * model_df["VPD_stomatal_scalar"]
    )
    model_df["RECO_model"] = R0 * np.exp(k * model_df["TA_F"])
    model_df["NEE_model"] = model_df["RECO_model"] - model_df["GPP_model"]
    model_df["residual"] = model_df["NEE_VUT_REF"] - model_df["NEE_model"]

    return model_df
