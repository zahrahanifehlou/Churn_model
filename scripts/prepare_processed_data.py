import sys
import argparse
from pathlib import Path

import pandas as pd
import yaml

# Project root = one level above scripts/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.preprocess import preprocess_data
from src.features.build_features import build_features


def load_params(params_path: str | Path | None = None) -> dict:
    if params_path is None:
        params_path = PROJECT_ROOT / "params.yaml"
    else:
        params_path = Path(params_path)
        if not params_path.is_absolute():
            params_path = PROJECT_ROOT / params_path

    with open(params_path, "r") as f:
        return yaml.safe_load(f)


def main(params_path: str | Path | None = None):
    params = load_params(params_path)
    p = params.get("preprocess", {})

    # ===== Paths (always relative to project root) =====
    raw_path = PROJECT_ROOT / p.get("raw_path", "data/raw/churn.csv")
    output_path = PROJECT_ROOT / p.get("output_path", "data/processed/churn_processed.csv")
    target_col = p.get("target_col", "Churn")

    # ===== Preprocessing parameters =====
    missing_strategy = p.get("missing_strategy", "median")
    scale_numeric = p.get("scale_numeric", True)
    scaler_type = p.get("scaler_type", "standard")
    remove_outliers = p.get("remove_outliers", False)

    print(f"Loading raw data from: {raw_path}")
    print(
        f"Parameters → missing_strategy={missing_strategy}, "
        f"scale_numeric={scale_numeric}, scaler_type={scaler_type}, "
        f"remove_outliers={remove_outliers}"
    )

    df = pd.read_csv(raw_path)

    # 1) Preprocess
    df = preprocess_data(
        df,
        target_col=target_col,
        missing_strategy=missing_strategy,
        scale_numeric=scale_numeric,
        scaler_type=scaler_type,
        remove_outliers=remove_outliers,
    )

    # 2) Ensure target is 0/1
    if target_col in df.columns and df[target_col].dtype == "object":
        df[target_col] = (
            df[target_col]
            .str.strip()
            .map({"No": 0, "Yes": 1})
            .astype("Int64")
        )

    # Sanity checks
    assert df[target_col].isna().sum() == 0, f"{target_col} has NaNs after preprocess"
    assert set(df[target_col].unique()) <= {0, 1}, f"{target_col} not 0/1 after preprocess"

    # 3) Feature engineering
    df_processed = build_features(df, target_col=target_col)

    # 4) Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_processed.to_csv(output_path, index=False)
    print(f"✅ Processed dataset saved to {output_path} | Shape: {df_processed.shape}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--params",
        default=None,
        help="Path to params.yaml (default: project_root/params.yaml)",
    )
    args = parser.parse_args()
    main(args.params)