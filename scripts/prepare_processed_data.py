import os
import sys
import argparse
from pathlib import Path

import pandas as pd
import yaml

# make src importable
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.data.preprocess import preprocess_data
from src.features.build_features import build_features


def load_params(params_path: str = "params.yaml") -> dict:
    with open(params_path, "r") as f:
        return yaml.safe_load(f)


def main(params_path: str = "params.yaml"):
    params = load_params(params_path)
    preprocess_params = params.get("preprocess", {})

    # Paths from params (or defaults)
    raw_path = preprocess_params.get("raw_path", "data/raw/churn.csv")
    output_path = preprocess_params.get("output_path", "data/processed/churn_processed.csv")
    target_col = preprocess_params.get("target_col", "Churn")

    print(f"Loading raw data from: {raw_path}")
    df = pd.read_csv(raw_path)

    # 1) Preprocess
    df = preprocess_data(
        df,
        target_col=target_col,
        # pass any extra params you want later
        **{k: v for k, v in preprocess_params.items()
           if k not in ["raw_path", "output_path", "target_col"]}
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
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df_processed.to_csv(output_path, index=False)
    print(f"✅ Processed dataset saved to {output_path} | Shape: {df_processed.shape}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", default="params.yaml", help="Path to params.yaml")
    args = parser.parse_args()
    main(args.params)