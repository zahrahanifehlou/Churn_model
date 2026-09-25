"""
Run Phase 2: XGBoost modeling with Optuna hyperparameter optimization.

Pipeline:
    1. Load configuration from params.yaml
    2. Load processed dataset
    3. Validate target
    4. Split data into train/test sets
    5. Calculate class imbalance weight
    6. Optimize XGBoost hyperparameters with Optuna
    7. Evaluate recall using configured threshold
    8. Log experiment results

Usage:
    python scripts/train.py
    python scripts/train.py --params params.yaml
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import optuna
import pandas as pd
import yaml

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


# ---------------------------------------------------------------------------
# Project setup
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT))


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
        logging.FileHandler(
            LOG_DIR / "pipeline.log",
            encoding="utf-8",
        ),
    ],
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def load_params(
    params_path: str | Path | None = None,
) -> dict:
    """Load parameters from params.yaml."""

    params_path = Path(
        params_path or "params.yaml"
    )

    if not params_path.is_absolute():
        params_path = PROJECT_ROOT / params_path

    if not params_path.exists():
        raise FileNotFoundError(
            f"Parameters file not found: {params_path}"
        )

    with params_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return yaml.safe_load(file) or {}


# ---------------------------------------------------------------------------
# Target validation
# ---------------------------------------------------------------------------

def validate_target(
    df: pd.DataFrame,
    target_col: str,
) -> pd.DataFrame:
    """Validate and normalize target column."""

    if target_col not in df.columns:
        raise ValueError(
            f"Target column '{target_col}' not found."
        )

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

    if df[target_col].isna().any():
        raise ValueError(
            f"Target column '{target_col}' contains NaNs."
        )

    if not set(
        df[target_col].unique()
    ).issubset({0, 1}):
        raise ValueError(
            f"Target column '{target_col}' "
            "must contain only 0/1."
        )

    return df


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(
    params_path: str | Path | None = None,
) -> None:
    """Run XGBoost + Optuna modeling pipeline."""

    # -----------------------------------------------------------------------
    # Load configuration
    # -----------------------------------------------------------------------

    params = load_params(params_path)

    config = params.get(
        "modeling",
        {},
    )

    xgb_config = config.get(
        "xgboost",
        {},
    )

    optuna_config = config.get(
        "optuna",
        {},
    )

    data_path = PROJECT_ROOT / config.get(
        "data_path",
        "data/processed/telco_churn_processed.csv",
    )

    target_col = config.get(
        "target_col",
        "Churn",
    )

    test_size = config.get(
        "test_size",
        0.20,
    )

    random_state = config.get(
        "random_state",
        42,
    )

    use_stratify = config.get(
        "stratify",
        True,
    )

    threshold = config.get(
        "threshold",
        0.40,
    )

    n_trials = optuna_config.get(
        "n_trials",
        30,
    )

    direction = optuna_config.get(
        "direction",
        "maximize",
    )

    metric = optuna_config.get(
        "metric",
        "recall",
    )

    logger.info("=" * 70)
    logger.info("PHASE 2: XGBOOST MODELING")
    logger.info("=" * 70)

    logger.info(
        "Loading processed dataset: %s",
        data_path,
    )

    # -----------------------------------------------------------------------
    # Load data
    # -----------------------------------------------------------------------

    if not data_path.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {data_path}"
        )

    df = pd.read_csv(data_path)

    logger.info(
        "Dataset shape: %s",
        df.shape,
    )

    # -----------------------------------------------------------------------
    # Validate target
    # -----------------------------------------------------------------------

    df = validate_target(
        df,
        target_col,
    )

    logger.info(
        "Target '%s' validated.",
        target_col,
    )

    logger.info(
        "Target distribution:\n%s",
        df[target_col].value_counts(),
    )

    # -----------------------------------------------------------------------
    # Separate X and y
    # -----------------------------------------------------------------------

    X = df.drop(
        columns=[target_col]
    )

    y = df[target_col]

    logger.info(
        "Features: %d",
        X.shape[1],
    )

    logger.info(
        "Samples: %d",
        X.shape[0],
    )

    # -----------------------------------------------------------------------
    # Train/test split
    # -----------------------------------------------------------------------

    stratify_value = y if use_stratify else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=stratify_value,
        random_state=random_state,
    )

    logger.info(
        "Training shape: %s",
        X_train.shape,
    )

    logger.info(
        "Test shape: %s",
        X_test.shape,
    )

    # -----------------------------------------------------------------------
    # Class imbalance
    # -----------------------------------------------------------------------

    negative_count = (
        y_train == 0
    ).sum()

    positive_count = (
        y_train == 1
    ).sum()

    scale_pos_weight = (
        negative_count / positive_count
    )

    logger.info(
        "Negative samples: %d",
        negative_count,
    )

    logger.info(
        "Positive samples: %d",
        positive_count,
    )

    logger.info(
        "scale_pos_weight: %.4f",
        scale_pos_weight,
    )

    # -----------------------------------------------------------------------
    # Optuna objective
    # -----------------------------------------------------------------------

    def objective(
        trial: optuna.Trial,
    ) -> float:

        params = {
            "n_estimators": trial.suggest_int(
                "n_estimators",
                xgb_config["n_estimators"]["min"],
                xgb_config["n_estimators"]["max"],
            ),

            "learning_rate": trial.suggest_float(
                "learning_rate",
                xgb_config["learning_rate"]["min"],
                xgb_config["learning_rate"]["max"],
            ),

            "max_depth": trial.suggest_int(
                "max_depth",
                xgb_config["max_depth"]["min"],
                xgb_config["max_depth"]["max"],
            ),

            "subsample": trial.suggest_float(
                "subsample",
                xgb_config["subsample"]["min"],
                xgb_config["subsample"]["max"],
            ),

            "colsample_bytree": trial.suggest_float(
                "colsample_bytree",
                xgb_config["colsample_bytree"]["min"],
                xgb_config["colsample_bytree"]["max"],
            ),

            "min_child_weight": trial.suggest_int(
                "min_child_weight",
                xgb_config["min_child_weight"]["min"],
                xgb_config["min_child_weight"]["max"],
            ),

            "gamma": trial.suggest_float(
                "gamma",
                xgb_config["gamma"]["min"],
                xgb_config["gamma"]["max"],
            ),

            "reg_alpha": trial.suggest_float(
                "reg_alpha",
                xgb_config["reg_alpha"]["min"],
                xgb_config["reg_alpha"]["max"],
            ),

            "reg_lambda": trial.suggest_float(
                "reg_lambda",
                xgb_config["reg_lambda"]["min"],
                xgb_config["reg_lambda"]["max"],
            ),

            "random_state": random_state,
            "n_jobs": xgb_config.get(
                "n_jobs",
                -1,
            ),
            "scale_pos_weight": scale_pos_weight,
            "eval_metric": xgb_config.get(
                "eval_metric",
                "logloss",
            ),
        }

        model = XGBClassifier(
            **params
        )

        model.fit(
            X_train,
            y_train,
        )

        probabilities = model.predict_proba(
            X_test
        )[:, 1]

        predictions = (
            probabilities >= threshold
        ).astype(int)

        recall = recall_score(
            y_test,
            predictions,
            pos_label=1,
        )

        logger.info(
            "Trial %d | recall=%.4f",
            trial.number,
            recall,
        )

        return recall

    # -----------------------------------------------------------------------
    # Optuna study
    # -----------------------------------------------------------------------

    logger.info(
        "Starting Optuna optimization."
    )

    logger.info(
        "Number of trials: %d",
        n_trials,
    )

    logger.info(
        "Optimization metric: %s",
        metric,
    )

    study = optuna.create_study(
        direction=direction,
    )

    study.optimize(
        objective,
        n_trials=n_trials,
    )

    # -----------------------------------------------------------------------
    # Best result
    # -----------------------------------------------------------------------

    logger.info("=" * 70)
    logger.info("OPTUNA OPTIMIZATION COMPLETED")
    logger.info("=" * 70)

    logger.info(
        "Best trial: %d",
        study.best_trial.number,
    )

    logger.info(
        "Best recall: %.4f",
        study.best_value,
    )

    logger.info(
        "Best parameters: %s",
        study.best_params,
    )

    # -----------------------------------------------------------------------
    # Train final model
    # -----------------------------------------------------------------------

    logger.info(
        "Training final model using best parameters."
    )

    best_params = {
        **study.best_params,
        "random_state": random_state,
        "n_jobs": xgb_config.get(
            "n_jobs",
            -1,
        ),
        "scale_pos_weight": scale_pos_weight,
        "eval_metric": xgb_config.get(
            "eval_metric",
            "logloss",
        ),
    }

    final_model = XGBClassifier(
        **best_params
    )

    final_model.fit(
        X_train,
        y_train,
    )

    # -----------------------------------------------------------------------
    # Final evaluation
    # -----------------------------------------------------------------------

    probabilities = final_model.predict_proba(
        X_test
    )[:, 1]

    predictions = (
        probabilities >= threshold
    ).astype(int)

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )

    # -----------------------------------------------------------------------
    # Log metrics
    # -----------------------------------------------------------------------

    logger.info("=" * 70)
    logger.info("FINAL MODEL METRICS")
    logger.info("=" * 70)

    logger.info(
        "Threshold: %.2f",
        threshold,
    )

    logger.info(
        "Accuracy: %.4f",
        accuracy,
    )

    logger.info(
        "Precision: %.4f",
        precision,
    )

    logger.info(
        "Recall: %.4f",
        recall,
    )

    logger.info(
        "F1: %.4f",
        f1,
    )

    logger.info(
        "Final model parameters: %s",
        best_params,
    )

    logger.info("=" * 70)
    logger.info(
        "PHASE 2 COMPLETED SUCCESSFULLY"
    )
    logger.info("=" * 70)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "Run Phase 2 XGBoost "
            "modeling pipeline."
        )
    )

    parser.add_argument(
        "--params",
        default=None,
        help="Path to params.yaml",
    )

    args = parser.parse_args()

    run_pipeline(
        args.params
    )