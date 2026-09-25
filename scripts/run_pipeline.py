#!/usr/bin/env python3

"""
End-to-end Telco churn ML pipeline.

Steps:
1. Load data
2. Validate data
3. Preprocess data
4. Build features
5. Split train / validation / test
6. Optimize XGBoost with Optuna
7. Train final model
8. Evaluate on test set
9. Log results to MLflow
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import mlflow
import mlflow.xgboost
import optuna
import pandas as pd
import yaml

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from xgboost import XGBClassifier


# ============================================================
# PROJECT SETUP
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


# ============================================================
# LOCAL MODULES
# ============================================================

from src.data.load_data import load_data
from src.data.preprocess import preprocess_data
from src.features.build_features import build_features
from src.utils.validate_data import validate_telco_data


# ============================================================
# LOGGING
# ============================================================

LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            LOG_DIR / "pipeline.log",
            encoding="utf-8"
        )
    ]
)

logger = logging.getLogger(__name__)


# ============================================================
# LOAD PARAMS
# ============================================================

def load_params(path="params.yaml"):

    path = PROJECT_ROOT / path

    if not path.exists():
        raise FileNotFoundError(
            f"Parameters file not found: {path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return yaml.safe_load(file) or {}


# ============================================================
# VALIDATE TARGET
# ============================================================

def validate_target(df, target):

    if target not in df.columns:
        raise ValueError(
            f"Target column '{target}' not found."
        )

    if df[target].dtype == "object":

        df[target] = df[target].map({
            "No": 0,
            "Yes": 1
        })

    if df[target].isna().any():

        raise ValueError(
            f"Target '{target}' contains missing values."
        )

    if not set(df[target].unique()).issubset({0, 1}):

        raise ValueError(
            f"Target '{target}' must contain only 0/1."
        )

    return df


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_pipeline(
    params_path="params.yaml"
):

    # ========================================================
    # CONFIGURATION
    # ========================================================

    params = load_params(
        params_path
    )

    preprocess_config = params.get(
        "preprocess",
        {}
    )

    modeling_config = params.get(
        "modeling",
        {}
    )

    optuna_config = modeling_config.get(
        "optuna",
        {}
    )

    xgb_config = modeling_config.get(
        "xgboost",
        {}
    )

    mlflow_config = params.get(
        "mlflow",
        {}
    )

    # --------------------------------------------------------
    # PARAMETERS
    # --------------------------------------------------------

    raw_path = PROJECT_ROOT / preprocess_config.get(
        "raw_path",
        "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    )

    processed_path = PROJECT_ROOT / preprocess_config.get(
        "output_path",
        "data/processed/telco_churn_processed.csv"
    )

    target = modeling_config.get(
        "target_col",
        "Churn"
    )

    test_size = modeling_config.get(
        "test_size",
        0.20
    )

    validation_size = modeling_config.get(
        "validation_size",
        0.20
    )

    random_state = modeling_config.get(
        "random_state",
        42
    )

    threshold = modeling_config.get(
        "threshold",
        0.40
    )

    n_trials = optuna_config.get(
        "n_trials",
        30
    )

    experiment_name = mlflow_config.get(
        "experiment_name",
        "Telco Churn"
    )

    tracking_uri = mlflow_config.get(
        "tracking_uri",
        "mlruns"
    )

    # ========================================================
    # START
    # ========================================================

    logger.info("=" * 70)
    logger.info(
        "TELCO CHURN — OPTUNA + XGBOOST + MLFLOW"
    )
    logger.info("=" * 70)

    # ========================================================
    # MLFLOW
    # ========================================================

    if tracking_uri.startswith(("http://", "https://", "sqlite:///")):
        mlflow.set_tracking_uri(tracking_uri)
    else:
        mlflow.set_tracking_uri(str(PROJECT_ROOT / tracking_uri))

    mlflow.set_experiment(
        experiment_name
    )

    # ========================================================
    # MLFLOW RUN
    # ========================================================

    with mlflow.start_run():

        mlflow.log_params({
            "model": "XGBoost",
            "target": target,
            "test_size": test_size,
            "validation_size": validation_size,
            "random_state": random_state,
            "threshold": threshold,
            "optuna_n_trials": n_trials,
        })

        # ====================================================
        # 1. LOAD
        # ====================================================

        logger.info(
            "[1/8] Loading data..."
        )

        df = load_data(
            str(raw_path)
        )

        logger.info(
            "Raw shape: %s",
            df.shape
        )

        logger.info(
            "Number of rows: %d",
            len(df)
        )

        mlflow.log_metric(
            "raw_rows",
            len(df)
        )

        # ====================================================
        # 2. VALIDATION
        # ====================================================

        logger.info(
            "[2/8] Validating data..."
        )

        if "TotalCharges" in df.columns:

            df["TotalCharges"] = pd.to_numeric(
                df["TotalCharges"],
                errors="coerce"
            )

        valid, failed = validate_telco_data(
            df
        )

        if not valid:

            logger.error(
                "Data validation FAILED"
            )

            logger.error(
                "Failed checks: %s",
                failed
            )

            raise ValueError(
                f"Data validation failed: {failed}"
            )

        logger.info(
            "Data validation PASSED"
        )

        # ====================================================
        # 3. PREPROCESS
        # ====================================================

        logger.info(
            "[3/8] Preprocessing..."
        )

        df = preprocess_data(
            df,
            target_col=target,
            missing_strategy=preprocess_config.get(
                "missing_strategy",
                "median"
            ),
            scale_numeric=preprocess_config.get(
                "scale_numeric",
                True
            ),
            scaler_type=preprocess_config.get(
                "scaler_type",
                "standard"
            ),
            remove_outliers=preprocess_config.get(
                "remove_outliers",
                False
            )
        )

        processed_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_csv(
            processed_path,
            index=False
        )

        logger.info(
            "Processed shape: %s",
            df.shape
        )

        logger.info(
            "Processed data saved to: %s",
            processed_path
        )

        if mlflow_config.get(
            "log_processed_data",
            True
        ):

            mlflow.log_artifact(
                str(processed_path),
                artifact_path="data"
            )

        # ====================================================
        # 4. FEATURE ENGINEERING
        # ====================================================

        logger.info(
            "[4/8] Building features..."
        )

        df = validate_target(
            df,
            target
        )

        df = build_features(
            df,
            target_col=target
        )

        # bool → int
        for column in df.select_dtypes(
            include="bool"
        ).columns:

            df[column] = df[column].astype(int)

        feature_columns = list(
            df.drop(
                columns=[target]
            ).columns
        )

        logger.info(
            "Number of features: %d",
            len(feature_columns)
        )

        logger.info(
            "Features: %s",
            feature_columns
        )

        # ====================================================
        # 5. TRAIN / VALIDATION / TEST
        # ====================================================

        logger.info(
            "[5/8] Splitting data..."
        )

        X = df.drop(
            columns=[target]
        )

        y = df[target]

        # Train + Test
        X_train_val, X_test, y_train_val, y_test = (
            train_test_split(
                X,
                y,
                test_size=test_size,
                random_state=random_state,
                stratify=y
            )
        )

        # Train + Validation
        validation_ratio = (
            validation_size /
            (1 - test_size)
        )

        X_train, X_val, y_train, y_val = (
            train_test_split(
                X_train_val,
                y_train_val,
                test_size=validation_ratio,
                random_state=random_state,
                stratify=y_train_val
            )
        )

        logger.info(
            "Train samples: %d",
            len(X_train)
        )

        logger.info(
            "Validation samples: %d",
            len(X_val)
        )

        logger.info(
            "Test samples: %d",
            len(X_test)
        )

        mlflow.log_metrics({
            "train_samples": len(X_train),
            "validation_samples": len(X_val),
            "test_samples": len(X_test)
        })

        # ====================================================
        # CLASS IMBALANCE
        # ====================================================

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
            negative_count /
            positive_count
        )

        logger.info(
            "Negative samples: %d",
            negative_count
        )

        logger.info(
            "Positive samples: %d",
            positive_count
        )

        logger.info(
            "scale_pos_weight: %.4f",
            scale_pos_weight
        )

        mlflow.log_metric(
            "scale_pos_weight",
            scale_pos_weight
        )

        # ====================================================
        # 6. OPTUNA
        # ====================================================

        logger.info(
            "[6/8] Starting Optuna optimization..."
        )

        def objective(trial):

            params = {

                "n_estimators": trial.suggest_int(
                    "n_estimators",
                    xgb_config["n_estimators"]["min"],
                    xgb_config["n_estimators"]["max"]
                ),

                "learning_rate": trial.suggest_float(
                    "learning_rate",
                    xgb_config["learning_rate"]["min"],
                    xgb_config["learning_rate"]["max"]
                ),

                "max_depth": trial.suggest_int(
                    "max_depth",
                    xgb_config["max_depth"]["min"],
                    xgb_config["max_depth"]["max"]
                ),

                "subsample": trial.suggest_float(
                    "subsample",
                    xgb_config["subsample"]["min"],
                    xgb_config["subsample"]["max"]
                ),

                "colsample_bytree": trial.suggest_float(
                    "colsample_bytree",
                    xgb_config["colsample_bytree"]["min"],
                    xgb_config["colsample_bytree"]["max"]
                ),

                "min_child_weight": trial.suggest_int(
                    "min_child_weight",
                    xgb_config["min_child_weight"]["min"],
                    xgb_config["min_child_weight"]["max"]
                ),

                "gamma": trial.suggest_float(
                    "gamma",
                    xgb_config["gamma"]["min"],
                    xgb_config["gamma"]["max"]
                ),

                "reg_alpha": trial.suggest_float(
                    "reg_alpha",
                    xgb_config["reg_alpha"]["min"],
                    xgb_config["reg_alpha"]["max"]
                ),

                "reg_lambda": trial.suggest_float(
                    "reg_lambda",
                    xgb_config["reg_lambda"]["min"],
                    xgb_config["reg_lambda"]["max"]
                ),

                "random_state": random_state,
                "n_jobs": -1,
                "scale_pos_weight": scale_pos_weight,
                "eval_metric": "logloss"
            }

            model = XGBClassifier(
                **params
            )

            model.fit(
                X_train,
                y_train
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
                zero_division=0
            )

            logger.info(
                "Trial %d | Recall: %.4f",
                trial.number,
                recall
            )

            return recall

        study = optuna.create_study(
            direction="maximize"
        )

        study.optimize(
            objective,
            n_trials=n_trials
        )

        # ====================================================
        # BEST OPTUNA RESULT
        # ====================================================

        logger.info(
            "Optuna optimization completed."
        )

        logger.info(
            "Best trial: %d",
            study.best_trial.number
        )

        logger.info(
            "Best validation recall: %.4f",
            study.best_value
        )

        logger.info(
            "Best parameters:"
        )

        for key, value in study.best_params.items():

            logger.info(
                "    %s: %s",
                key,
                value
            )

        mlflow.log_metric(
            "best_validation_recall",
            study.best_value
        )

        mlflow.log_params({
            f"best_{key}": value
            for key, value
            in study.best_params.items()
        })

        # ====================================================
        # 7. FINAL MODEL
        # ====================================================

        logger.info(
            "[7/8] Training final model..."
        )

        final_params = {
            **study.best_params,
            "random_state": random_state,
            "n_jobs": -1,
            "scale_pos_weight": scale_pos_weight,
            "eval_metric": "logloss"
        }

        logger.info(
            "Final model parameters:"
        )

        for key, value in final_params.items():

            logger.info(
                "    %s: %s",
                key,
                value
            )

        final_model = XGBClassifier(
            **final_params
        )

        # Train using train + validation
        final_model.fit(
            X_train_val,
            y_train_val
        )

        logger.info(
            "Final model training completed."
        )

        # ====================================================
        # 8. TEST
        # ====================================================

        logger.info(
            "[8/8] Evaluating final model on TEST set..."
        )

        probabilities = final_model.predict_proba(
            X_test
        )[:, 1]

        predictions = (
            probabilities >= threshold
        ).astype(int)

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        precision = precision_score(
            y_test,
            predictions,
            zero_division=0
        )

        recall = recall_score(
            y_test,
            predictions,
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            predictions,
            zero_division=0
        )

        roc_auc = roc_auc_score(
            y_test,
            probabilities
        )

        # ====================================================
        # TEST OUTPUT
        # ====================================================

        logger.info("=" * 70)
        logger.info("FINAL TEST RESULTS")
        logger.info("=" * 70)

        logger.info(
            "Accuracy : %.4f",
            accuracy
        )

        logger.info(
            "Precision: %.4f",
            precision
        )

        logger.info(
            "Recall   : %.4f",
            recall
        )

        logger.info(
            "F1       : %.4f",
            f1
        )

        logger.info(
            "ROC-AUC  : %.4f",
            roc_auc
        )

        # ====================================================
        # CLASSIFICATION REPORT
        # ====================================================

        report = classification_report(
            y_test,
            predictions,
            digits=3
        )

        logger.info(
            "\nClassification Report:\n%s",
            report
        )

        # ====================================================
        # MLFLOW METRICS
        # ====================================================

        mlflow.log_metric(
            "test_accuracy",
            accuracy
        )

        mlflow.log_metric(
            "test_precision",
            precision
        )

        mlflow.log_metric(
            "test_recall",
            recall
        )

        mlflow.log_metric(
            "test_f1",
            f1
        )

        mlflow.log_metric(
            "test_roc_auc",
            roc_auc
        )

        mlflow.log_text(
            report,
            "classification_report.txt"
        )

        # ====================================================
        # SAVE MODEL TO MLFLOW
        # ====================================================

        logger.info(
            "Logging final model to MLflow..."
        )

        mlflow.xgboost.log_model(
            final_model,
            "model"
        )

        # ====================================================
        # FINAL
        # ====================================================

        run_id = mlflow.active_run().info.run_id

        logger.info("=" * 70)
        logger.info(
            "PIPELINE COMPLETED SUCCESSFULLY"
        )
        logger.info("=" * 70)

        logger.info(
            "MLflow Run ID: %s",
            run_id
        )

        logger.info(
            "Best validation recall: %.4f",
            study.best_value
        )

        logger.info(
            "Test Accuracy : %.4f",
            accuracy
        )

        logger.info(
            "Test Precision: %.4f",
            precision
        )

        logger.info(
            "Test Recall   : %.4f",
            recall
        )

        logger.info(
            "Test F1       : %.4f",
            f1
        )

        logger.info(
            "Test ROC-AUC  : %.4f",
            roc_auc
        )


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--params",
        default="params.yaml",
        help="Path to params.yaml"
    )

    args = parser.parse_args()

    run_pipeline(
        args.params
    )