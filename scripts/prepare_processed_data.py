
"""Run the end-to-end data preprocessing and feature engineering pipeline.

Pipeline:
    1. Load configuration from params.yaml
    2. Load raw dataset
    3. Preprocess data
    4. Validate and normalize target column
    5. Build engineered features
    6. Persist processed dataset

Usage:
    python scripts/preprocess.py
    python scripts/preprocess.py --params params.yaml
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
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "pipeline.log", encoding="utf-8"),
    ],
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
        return yaml.safe_load(file)


# ---------------------------------------------------------------------------
# Target validation
# ---------------------------------------------------------------------------

def validate_target(df: pd.DataFrame, target_col: str) -> pd.DataFrame:
    """Convert and validate the target column."""
    if target_col not in df.columns:
        raise ValueError(
            f"Target column '{target_col}' not found."
        )

    if df[target_col].dtype == "object":
        df[target_col] = (
            df[target_col]
            .str.strip()
            .map({"No": 0, "Yes": 1})
        )

    if df[target_col].isna().any():
        raise ValueError(
            f"Target column '{target_col}' contains missing values."
        )

    if not set(df[target_col].unique()).issubset({0, 1}):
        raise ValueError(
            f"Target column '{target_col}' must contain only 0/1."
        )

    return df


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(params_path: str | Path | None = None) -> None:
    """Run the preprocessing pipeline."""

    params = load_params(params_path)
    p = params.get("preprocess", {})

    raw_path = PROJECT_ROOT / p.get(
        "raw_path",
        "data/raw/churn.csv",
    )

    output_path = PROJECT_ROOT / p.get(
        "output_path",
        "data/processed/churn_processed.csv",
    )

    target_col = p.get("target_col", "Churn")

    logger.info("Starting preprocessing pipeline")
    logger.info("Loading data: %s", raw_path)

    # 1. Load data
    df = pd.read_csv(raw_path)

    logger.info(
        "Raw data shape: %s",
        df.shape,
    )

    # 2. Preprocess
    logger.info("Preprocessing data")

    df = preprocess_data(
        df,
        target_col=target_col,
        missing_strategy=p.get("missing_strategy", "median"),
        scale_numeric=p.get("scale_numeric", True),
        scaler_type=p.get("scaler_type", "standard"),
        remove_outliers=p.get("remove_outliers", False),
    )

    # 3. Validate target
    logger.info("Validating target: %s", target_col)

    df = validate_target(
        df,
        target_col,
    )

    # 4. Feature engineering
    logger.info("Building features")

    df = build_features(
        df,
        target_col=target_col,
    )

    # 5. Save
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        output_path,
        index=False,
    )

    logger.info(
        "Processed data saved: %s",
        output_path,
    )

    logger.info(
        "Final data shape: %s",
        df.shape,
    )

    logger.info("Pipeline completed successfully")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the data preprocessing pipeline."
    )

    parser.add_argument(
        "--params",
        default=None,
        help="Path to params.yaml",
    )

    args = parser.parse_args()

    run_pipeline(args.params)

