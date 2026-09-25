"""
Test Phase 1: End-to-end data preprocessing and feature engineering.

Pipeline:
    1. Load parameters from params.yaml
    2. Load raw dataset
    3. Preprocess data
    4. Validate target column
    5. Build engineered features
    6. Save processed dataset

Usage:
    python tests/test_pipeline_phase1.py
    python tests/test_pipeline_phase1.py --params params.yaml
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd
import yaml

# ---------------------------------------------------------------------------
# Project setup
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT))

from src.data.preprocess import preprocess_data
from src.features.build_features import build_features


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def load_params(params_path: str | Path | None = None) -> dict:
    """Load parameters from params.yaml."""

    params_path = Path(params_path or "params.yaml")

    if not params_path.is_absolute():
        params_path = PROJECT_ROOT / params_path

    if not params_path.exists():
        raise FileNotFoundError(
            f"Parameters file not found: {params_path}"
        )

    with params_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


# ---------------------------------------------------------------------------
# Target validation
# ---------------------------------------------------------------------------

def validate_target(
    df: pd.DataFrame,
    target_col: str,
) -> pd.DataFrame:
    """Validate and normalize the target column."""

    if target_col not in df.columns:
        raise ValueError(
            f"Target column '{target_col}' not found."
        )

    # Convert Yes/No target into 1/0
    if df[target_col].dtype == "object":
        df[target_col] = (
            df[target_col]
            .astype(str)
            .str.strip()
            .map({
                "No": 0,
                "Yes": 1,
            })
        )

    # Check missing target values
    if df[target_col].isna().any():
        raise ValueError(
            f"Target column '{target_col}' contains missing values."
        )

    # Check binary target
    if not set(df[target_col].unique()).issubset({0, 1}):
        raise ValueError(
            f"Target column '{target_col}' must contain only 0/1."
        )

    return df


# ---------------------------------------------------------------------------
# Pipeline test
# ---------------------------------------------------------------------------

def main(params_path: str | Path | None = None) -> None:
    """Run the Phase 1 preprocessing test."""

    print("=" * 70)
    print("TESTING PHASE 1: LOAD → PREPROCESS → FEATURE ENGINEERING")
    print("=" * 70)

    # -----------------------------------------------------------------------
    # Load configuration
    # -----------------------------------------------------------------------

    print("\n[0] Loading configuration...")

    params = load_params(params_path)
    p = params.get("preprocess", {})

    raw_path = PROJECT_ROOT / p.get(
        "raw_path",
        "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv",
    )

    output_path = PROJECT_ROOT / p.get(
        "output_path",
        "data/processed/churn_processed.csv",
    )

    target_col = p.get(
        "target_col",
        "Churn",
    )

    print(f"Raw data:    {raw_path}")
    print(f"Output data: {output_path}")
    print(f"Target:      {target_col}")

    # -----------------------------------------------------------------------
    # 1. Load data
    # -----------------------------------------------------------------------

    print("\n[1] Loading data...")

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {raw_path}"
        )

    df = pd.read_csv(raw_path)

    print(f"Data loaded successfully.")
    print(f"Shape: {df.shape}")
    print(f"Columns: {len(df.columns)}")

    # -----------------------------------------------------------------------
    # 2. Preprocess
    # -----------------------------------------------------------------------

    print("\n[2] Preprocessing data...")

    df_clean = preprocess_data(
        df,
        target_col=target_col,
        missing_strategy=p.get(
            "missing_strategy",
            "median",
        ),
        scale_numeric=p.get(
            "scale_numeric",
            True,
        ),
        scaler_type=p.get(
            "scaler_type",
            "standard",
        ),
        remove_outliers=p.get(
            "remove_outliers",
            False,
        ),
    )

    print(
        f"Data after preprocessing: {df_clean.shape}"
    )

    # -----------------------------------------------------------------------
    # 3. Validate target
    # -----------------------------------------------------------------------

    print("\n[3] Validating target...")

    df_clean = validate_target(
        df_clean,
        target_col,
    )

    print(
        f"Target '{target_col}' is valid."
    )

    print(
        f"Target values: "
        f"{sorted(df_clean[target_col].unique())}"
    )

    print(
        f"Target distribution:\n"
        f"{df_clean[target_col].value_counts()}"
    )

    # -----------------------------------------------------------------------
    # 4. Feature engineering
    # -----------------------------------------------------------------------

    print("\n[4] Building features...")

    df_features = build_features(
        df_clean,
        target_col=target_col,
    )

    print(
        f"Data after feature engineering: "
        f"{df_features.shape}"
    )

    # -----------------------------------------------------------------------
    # 5. Basic validation
    # -----------------------------------------------------------------------

    print("\n[5] Running basic validation...")

    assert len(df_features) > 0, (
        "Feature dataset is empty."
    )

    assert target_col in df_features.columns, (
        f"Target column '{target_col}' disappeared."
    )

    assert not df_features[target_col].isna().any(), (
        "Target contains missing values."
    )

    assert set(
        df_features[target_col].unique()
    ).issubset({0, 1}), (
        "Target is not binary."
    )

    print("✓ Dataset is not empty")
    print("✓ Target column exists")
    print("✓ Target contains no missing values")
    print("✓ Target contains only 0/1")

    # -----------------------------------------------------------------------
    # 6. Save processed data
    # -----------------------------------------------------------------------

    print("\n[6] Saving processed dataset...")

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df_features.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Processed dataset saved to:\n"
        f"{output_path}"
    )

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------

    print("\n" + "=" * 70)
    print("PHASE 1 TEST PASSED")
    print("=" * 70)

    print(f"Raw shape:        {df.shape}")
    print(f"Preprocessed:     {df_clean.shape}")
    print(f"Final features:   {df_features.shape}")
    print(f"Output:           {output_path}")

    print("\nFirst 3 rows:")
    print(df_features.head(3))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "Test Phase 1 preprocessing "
            "and feature engineering."
        )
    )

    parser.add_argument(
        "--params",
        default=None,
        help="Path to params.yaml",
    )

    args = parser.parse_args()

    main(args.params)