import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.impute import KNNImputer


def preprocess_data(
    df: pd.DataFrame,
    target_col: str = "Churn",
    missing_strategy: str = "median",      # "median", "mean", "drop", "knn", "zero"
    scale_numeric: bool = True,
    scaler_type: str = "standard",         # "standard", "robust", "minmax"
    remove_outliers: bool = False,
) -> pd.DataFrame:
    """
    Cleaning + optional scaling/outlier removal for Telco churn.
    """

    df = df.copy()  # avoid modifying original

    # 1. Tidy column names
    df.columns = df.columns.str.strip()

    # 2. Drop ID columns
    for col in ["customerID", "CustomerID", "customer_id"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    # 3. Convert target to 0/1 if needed
    if target_col in df.columns and df[target_col].dtype == "object":
        df[target_col] = (
            df[target_col]
            .str.strip()
            .map({"No": 0, "Yes": 1})
        )

    # 4. Fix TotalCharges
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # 5. Fix SeniorCitizen
    if "SeniorCitizen" in df.columns:
        df["SeniorCitizen"] = df["SeniorCitizen"].fillna(0).astype(int)

    # ==========================================
    # 6. Missing value handling
    # ==========================================
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if target_col in num_cols:
        num_cols.remove(target_col)  # don't impute target

    if missing_strategy == "drop":
        df = df.dropna()
    elif missing_strategy == "zero":
        df[num_cols] = df[num_cols].fillna(0)
    elif missing_strategy == "mean":
        df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
    elif missing_strategy == "median":
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    elif missing_strategy == "knn":
        imputer = KNNImputer(n_neighbors=5)
        df[num_cols] = imputer.fit_transform(df[num_cols])
    else:
        raise ValueError(f"Unknown missing_strategy: {missing_strategy}")

    # ==========================================
    # 7. Optional: Remove outliers (IQR method)
    # ==========================================
    if remove_outliers:
        for col in num_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower) & (df[col] <= upper)]

    # ==========================================
    # 8. Optional: Scale numeric features
    # ==========================================
    if scale_numeric and len(num_cols) > 0:
        if scaler_type == "standard":
            scaler = StandardScaler()
        elif scaler_type == "robust":
            scaler = RobustScaler()
        elif scaler_type == "minmax":
            scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaler_type: {scaler_type}")

        df[num_cols] = scaler.fit_transform(df[num_cols])

    return df