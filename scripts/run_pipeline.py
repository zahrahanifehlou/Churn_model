#!/usr/bin/env python3

"""
End-to-end Telco churn ML pipeline.

Pipeline:

    1. Load configuration
    2. Load raw data
    3. Validate data
    4. Preprocess data
    5. Build features
    6. Save processed dataset
    7. Train / validation / test split
    8. Optimize XGBoost with Optuna
    9. Train final model using best parameters
   10. Evaluate on test set
   11. Log experiment to MLflow
   12. Save model artifacts

Usage:

    python scripts/run_pipeline.py

    python scripts/run_pipeline.py --params params.yaml
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

import joblib
import mlflow
import mlflow.xgboost
import optuna
import pandas as pd
import yaml

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from sklearn.model_selection import train_test_split

from xgboost import XGBClassifier


# ============================================================================
# PROJECT SETUP
# ============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT),
)


# ============================================================================
# LOCAL MODULES
# ============================================================================

from src.data.load_data import load_data
from src.data.preprocess import preprocess_data
from src.features.build_features import build_features
from src.utils.validate_data import validate_telco_data


# ============================================================================
# LOGGING
# ============================================================================

LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

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


# ============================================================================
# CONFIGURATION
# ============================================================================

def load_params(
    params_path: str | Path | None = None,
) -> dict:
    """Load params.yaml."""

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


# ============================================================================
# TARGET VALIDATION
# ============================================================================

def validate_target(
    df: pd.DataFrame,
    target_col: str,
) -> pd.DataFrame:
    """Validate and normalize target."""

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
            f"Target '{target_col}' contains missing values."
        )

    if not set(
        df[target_col].unique()
    ).issubset({0, 1}):

        raise ValueError(
            f"Target '{target_col}' must contain only 0/1."
        )

    return df


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def run_pipeline(
    params_path: str | Path | None = None,
) -> None:

    # ------------------------------------------------------------------------
    # CONFIG
    # ------------------------------------------------------------------------

    params = load_params(
        params_path
    )

    preprocess_config = params.get(
        "preprocess",
        {},
    )

    modeling_config = params.get(
        "modeling",
        {},
    )

    optuna_config = modeling_config.get(
        "optuna",
        {},
    )

    xgb_config = modeling_config.get(
        "xgboost",
        {},
    )

    mlflow_config = params.get(
        "mlflow",
        {},
    )

    # ------------------------------------------------------------------------
    # PARAMETERS
    # ------------------------------------------------------------------------

    raw_path = PROJECT_ROOT / preprocess_config.get(
        "raw_path",
        "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv",
    )

    processed_path = PROJECT_ROOT / preprocess_config.get(
        "output_path",
        "data/processed/telco_churn_processed.csv",
    )

    target_col = modeling_config.get(
        "target_col",
        "Churn",
    )

    test_size = modeling_config.get(
        "test_size",
        0.20,
    )

    validation_size = modeling_config.get(
        "validation_size",
        0.20,
    )

    random_state = modeling_config.get(
        "random_state",
        42,
    )

    threshold = modeling_config.get(
        "threshold",
        0.40,
    )

    n_trials = optuna_config.get(
        "n_trials",
        30,
    )

    optuna_direction = optuna_config.get(
        "direction",
        "maximize",
    )

    experiment_name = mlflow_config.get(
        "experiment_name",
        "Telco Churn",
    )

    tracking_uri = mlflow_config.get(
        "tracking_uri",
        "mlruns",
    )

    # =========================================================================
    # START
    # =========================================================================

    logger.info("=" * 70)
    logger.info("TELCO CHURN — OPTUNA + XGBOOST + MLFLOW")
    logger.info("=" * 70)

    # =========================================================================
    # MLFLOW
    # =========================================================================

    if tracking_uri.startswith(
        ("http://", "https://", "file:")
    ):
        mlflow.set_tracking_uri(
            tracking_uri
        )
    else:
        mlflow.set_tracking_uri(
            str(
                PROJECT_ROOT / tracking_uri
            )
        )

    mlflow.set_experiment(
        experiment_name
    )

    with mlflow.start_run():

        # =====================================================================
        # LOG CONFIGURATION
        # =====================================================================

        mlflow.log_params({
            "model": "xgboost",
            "target": target_col,
            "test_size": test_size,
            "validation_size": validation_size,
            "random_state": random_state,
            "threshold": threshold,
            "optuna_n_trials": n_trials,
            "optuna_direction": optuna_direction,
        })

        # =====================================================================
        # 1. LOAD
        # =====================================================================

        logger.info(
            "[1/8] Loading data..."
        )

        df = load_data(
            str(raw_path)
        )

        logger.info(
            "Raw shape: %s",
            df.shape,
        )

        mlflow.log_metric(
            "raw_rows",
            len(df),
        )

        # =====================================================================
        # 2. VALIDATION
        # =====================================================================

        logger.info(
            "[2/8] Validating data..."
        )

        if "TotalCharges" in df.columns:

            df["TotalCharges"] = pd.to_numeric(
                df["TotalCharges"],
                errors="coerce",
            )

        is_valid, failed = validate_telco_data(
            df
        )

        mlflow.log_metric(
            "data_quality_pass",
            int(is_valid),
        )

        if not is_valid:

            mlflow.log_text(
                json.dumps(
                    failed,
                    indent=2,
                ),
                artifact_file="failed_expectations.json",
            )

            raise ValueError(
                f"Data validation failed: {failed}"
            )

        logger.info(
            "Data validation passed."
        )

        # =====================================================================
        # 3. PREPROCESS
        # =====================================================================

        logger.info(
            "[3/8] Preprocessing..."
        )

        df = preprocess_data(
            df,
            target_col=target_col,
            missing_strategy=preprocess_config.get(
                "missing_strategy",
                "median",
            ),
            scale_numeric=preprocess_config.get(
                "scale_numeric",
                True,
            ),
            scaler_type=preprocess_config.get(
                "scaler_type",
                "standard",
            ),
            remove_outliers=preprocess_config.get(
                "remove_outliers",
                False,
            ),
        )

        processed_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_csv(
            processed_path,
            index=False,
        )

        if mlflow_config.get(
            "log_processed_data",
            True,
        ):

            mlflow.log_artifact(
                str(processed_path),
                artifact_path="data",
            )

        logger.info(
            "Processed shape: %s",
            df.shape,
        )

        # =====================================================================
        # 4. FEATURE ENGINEERING
        # =====================================================================

        logger.info(
            "[4/8] Building features..."
        )

        df = validate_target(
            df,
            target_col,
        )

        df = build_features(
            df,
            target_col=target_col,
        )

        # Boolean → integer
        for column in df.select_dtypes(
            include=["bool"]
        ).columns:

            df[column] = (
                df[column]
                .astype(int)
            )

        feature_columns = list(
            df.drop(
                columns=[target_col]
            ).columns
        )

        logger.info(
            "Number of features: %d",
            len(feature_columns),
        )

        # =====================================================================
        # SAVE PREPROCESSING ARTIFACT
        # =====================================================================

        artifacts_dir = (
            PROJECT_ROOT / "artifacts"
        )

        artifacts_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        preprocessing_artifact = {
            "feature_columns": feature_columns,
            "target": target_col,
        }

        preprocessing_path = (
            artifacts_dir
            / "preprocessing.pkl"
        )

        joblib.dump(
            preprocessing_artifact,
            preprocessing_path,
        )

        mlflow.log_artifact(
            str(preprocessing_path),
            artifact_path="preprocessing",
        )

        mlflow.log_text(
            "\n".join(feature_columns),
            artifact_file="feature_columns.txt",
        )

        # =====================================================================
        # 5. TRAIN / VALIDATION / TEST SPLIT
        # =====================================================================

        logger.info(
            "[5/8] Splitting data..."
        )

        X = df.drop(
            columns=[target_col]
        )

        y = df[target_col]

        # First split:
        # train+validation / test
        X_train_val, X_test, y_train_val, y_test = (
            train_test_split(
                X,
                y,
                test_size=test_size,
                stratify=y,
                random_state=random_state,
            )
        )

        # Second split:
        # train / validation
        validation_ratio = (
            validation_size
            / (1 - test_size)
        )

        X_train, X_val, y_train, y_val = (
            train_test_split(
                X_train_val,
                y_train_val,
                test_size=validation_ratio,
                stratify=y_train_val,
                random_state=random_state,
            )
        )

        logger.info(
            "Train: %d",
            len(X_train),
        )

        logger.info(
            "Validation: %d",
            len(X_val),
        )

        logger.info(
            "Test: %d",
            len(X_test),
        )

        mlflow.log_metrics({
            "train_samples": len(X_train),
            "validation_samples": len(X_val),
            "test_samples": len(X_test),
        })

        # =====================================================================
        # CLASS IMBALANCE
        # =====================================================================

        negative_count = (
            y_train == 0
        ).sum()

        positive_count = (
            y_train == 1
        ).sum()

        if positive_count == 0:

            raise ValueError(
                "Training set contains no positive samples."
            )

        scale_pos_weight = (
            negative_count
            / positive_count
        )

        mlflow.log_metric(
            "scale_pos_weight",
            scale_pos_weight,
        )

        logger.info(
            "scale_pos_weight: %.4f",
            scale_pos_weight,
        )

        # =====================================================================
        # 6. OPTUNA
        # =====================================================================

        logger.info(
            "[6/8] Starting Optuna optimization..."
        )

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
                X_val
            )[:, 1]

            predictions = (
                probabilities >= threshold
            ).astype(int)

            recall = recall_score(
                y_val,
                predictions,
                zero_division=0,
            )

            logger.info(
                "Trial %d | Recall: %.4f",
                trial.number,
                recall,
            )

            return recall

        study = optuna.create_study(
            direction=optuna_direction,
        )

        study.optimize(
            objective,
            n_trials=n_trials,
        )

        # =====================================================================
        # BEST OPTUNA RESULT
        # =====================================================================

        logger.info(
            "Optuna optimization completed."
        )

        logger.info(
            "Best trial: %d",
            study.best_trial.number,
        )

        logger.info(
            "Best validation recall: %.4f",
            study.best_value,
        )

        logger.info(
            "Best parameters: %s",
            study.best_params,
        )

        mlflow.log_metric(
            "best_validation_recall",
            study.best_value,
        )

        mlflow.log_params({
            f"best_{key}": value
            for key, value
            in study.best_params.items()
        })

        # =====================================================================
        # 7. FINAL MODEL
        # =====================================================================

        logger.info(
            "[7/8] Training final model..."
        )

        final_params = {
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
            **final_params
        )

        train_start = time.time()

        # Train using train + validation data
        final_model.fit(
            X_train_val,
            y_train_val,
        )

        train_time = (
            time.time()
            - train_start
        )

        mlflow.log_metric(
            "final_train_time_seconds",
            train_time,
        )

        # =====================================================================
        # 8. FINAL TEST EVALUATION
        # =====================================================================

        logger.info(
            "[8/8] Evaluating final model on TEST set..."
        )

        prediction_start = time.time()

        test_proba = final_model.predict_proba(
            X_test
        )[:, 1]

        test_pred = (
            test_proba >= threshold
        ).astype(int)

        prediction_time = (
            time.time()
            - prediction_start
        )

        accuracy = accuracy_score(
            y_test,
            test_pred,
        )

        precision = precision_score(
            y_test,
            test_pred,
            zero_division=0,
        )

        recall = recall_score(
            y_test,
            test_pred,
            zero_division=0,
        )

        f1 = f1_score(
            y_test,
            test_pred,
            zero_division=0,
        )

        roc_auc = roc_auc_score(
            y_test,
            test_proba,
        )

        mlflow.log_metrics({
            "test_accuracy": accuracy,
            "test_precision": precision,
            "test_recall": recall,
            "test_f1": f1,
            "test_roc_auc": roc_auc,
            "prediction_time_seconds": prediction_time,
        })

        report = classification_report(
            y_test,
            test_pred,
            digits=3,
        )

        mlflow.log_text(
            report,
            artifact_file="classification_report.txt",
        )

        # =====================================================================
        # LOG FINAL MODEL
        # =====================================================================

        logger.info(
            "Logging final model to MLflow..."
        )

        mlflow.xgboost.log_model(
            final_model,
            artifact_path="model",
        )

        # =====================================================================
        # SUMMARY
        # =====================================================================

        logger.info("=" * 70)
        logger.info(
            "PIPELINE COMPLETED SUCCESSFULLY"
        )
        logger.info("=" * 70)

        logger.info(
            "Best validation recall: %.4f",
            study.best_value,
        )

        logger.info(
            "Test Accuracy: %.4f",
            accuracy,
        )

        logger.info(
            "Test Precision: %.4f",
            precision,
        )

        logger.info(
            "Test Recall: %.4f",
            recall,
        )

        logger.info(
            "Test F1: %.4f",
            f1,
        )

        logger.info(
            "Test ROC AUC: %.4f",
            roc_auc,
        )

        logger.info(
            "\nClassification Report:\n%s",
            report,
        )

        logger.info(
            "MLflow Run ID: %s",
            mlflow.active_run().info.run_id,
        )


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "Run Telco churn "
            "XGBoost + Optuna + MLflow pipeline."
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