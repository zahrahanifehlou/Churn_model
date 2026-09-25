def validate_telco_data(df):
    failed = []

    required_columns = [
        "customerID",
        "gender",
        "Partner",
        "Dependents",
        "PhoneService",
        "InternetService",
        "Contract",
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
    ]

    for column in required_columns:
        if column not in df.columns:
            failed.append(f"column_exists: {column}")

    if "customerID" in df.columns:
        if df["customerID"].isna().any():
            failed.append("customerID_not_null")

    if "gender" in df.columns:
        invalid = ~df["gender"].isin(["Male", "Female"])
        if invalid.any():
            failed.append("gender_valid_values")

    if "Partner" in df.columns:
        invalid = ~df["Partner"].isin(["Yes", "No"])
        if invalid.any():
            failed.append("Partner_valid_values")

    if "Dependents" in df.columns:
        invalid = ~df["Dependents"].isin(["Yes", "No"])
        if invalid.any():
            failed.append("Dependents_valid_values")

    if "PhoneService" in df.columns:
        invalid = ~df["PhoneService"].isin(["Yes", "No"])
        if invalid.any():
            failed.append("PhoneService_valid_values")

    if "Contract" in df.columns:
        invalid = ~df["Contract"].isin(
            ["Month-to-month", "One year", "Two year"]
        )
        if invalid.any():
            failed.append("Contract_valid_values")

    if "InternetService" in df.columns:
        invalid = ~df["InternetService"].isin(
            ["DSL", "Fiber optic", "No"]
        )
        if invalid.any():
            failed.append("InternetService_valid_values")

    if "tenure" in df.columns:
        if not df["tenure"].between(0, 120).all():
            failed.append("tenure_range")

    if "MonthlyCharges" in df.columns:
        if not df["MonthlyCharges"].between(0, 200).all():
            failed.append("MonthlyCharges_range")

    if "TotalCharges" in df.columns:
        if (df["TotalCharges"].dropna() < 0).any():
            failed.append("TotalCharges_non_negative")

    if "tenure" in df.columns:
        if df["tenure"].isna().any():
            failed.append("tenure_not_null")

    if "MonthlyCharges" in df.columns:
        if df["MonthlyCharges"].isna().any():
            failed.append("MonthlyCharges_not_null")

    if all(
        column in df.columns
        for column in ["TotalCharges", "MonthlyCharges"]
    ):
        comparison = (
            df["TotalCharges"] >= df["MonthlyCharges"]
        )

        if comparison.mean() < 0.95:
            failed.append(
                "TotalCharges_greater_than_MonthlyCharges"
            )

    if failed:
        print(
            f"❌ Data validation FAILED: "
            f"{len(failed)} checks failed"
        )
        print("   Failed expectations:", failed)

        return False, failed

    print("✅ Data validation PASSED")

    return True, []