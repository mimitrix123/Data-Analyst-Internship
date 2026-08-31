"""Week 4 — End-to-End Data Analyst Capstone.

Works with CSV/XLSX files containing a Sales/Revenue target. Produces EDA,
a baseline regression model, summaries and charts. Adjust column aliases if
needed for a different dataset.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def load(path: Path) -> pd.DataFrame:
    return pd.read_excel(path) if path.suffix.lower() in {".xlsx", ".xls"} else pd.read_csv(path)


def find(df, names):
    for c in df.columns:
        if str(c).strip().lower() in {n.lower() for n in names}:
            return c
    for c in df.columns:
        if any(n.lower() in str(c).lower() for n in names):
            return c
    return None


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python capstone_solution.py <data.csv-or-xlsx>")
    df = load(Path(sys.argv[1])).drop_duplicates().copy()
    out = Path("capstone_output")
    out.mkdir(exist_ok=True)

    target = find(df, ["Sales", "Revenue", "Amount"])
    if target is None:
        raise SystemExit("No Sales/Revenue/Amount target column found.")
    df[target] = pd.to_numeric(df[target], errors="coerce")
    df = df.dropna(subset=[target])

    # EDA
    summary = df.describe(include="all").transpose()
    summary.to_csv(out / "eda_summary.csv")
    missing = df.isna().sum().sort_values(ascending=False)
    missing.to_csv(out / "missing_values.csv", header=["missing_count"])

    # Identify a date column and add useful time features
    date_col = find(df, ["Order Date", "Date", "OrderDate"])
    if date_col:
        dates = pd.to_datetime(df[date_col], errors="coerce")
        df["Year"] = dates.dt.year
        df["Month"] = dates.dt.month

    # Key summaries
    for label, col in [("category", find(df, ["Category"])), ("region", find(df, ["Region"])), ("department", find(df, ["Department", "Dept"]))]:
        if col:
            df.groupby(col)[target].sum().sort_values(ascending=False).to_csv(out / f"{label}_revenue.csv", header=["Total Revenue"])

    # Regression baseline: all remaining columns except the target
    X = df.drop(columns=[target])
    y = df[target]
    # Remove raw date columns because the generic pipeline cannot encode them safely
    X = X.drop(columns=[date_col], errors="ignore")
    numeric = X.select_dtypes(include="number").columns.tolist()
    categorical = X.select_dtypes(exclude="number").columns.tolist()
    transformers = []
    if numeric:
        transformers.append(("num", SimpleImputer(strategy="median"), numeric))
    if categorical:
        transformers.append(("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical))
    if not transformers:
        raise SystemExit("No usable predictor columns found.")

    model = Pipeline([("preprocess", ColumnTransformer(transformers)), ("model", LinearRegression())])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    metrics = pd.DataFrame({"metric": ["MAE", "RMSE", "R2"], "value": [mean_absolute_error(y_test, pred), mean_squared_error(y_test, pred) ** 0.5, r2_score(y_test, pred)]})
    metrics.to_csv(out / "regression_metrics.csv", index=False)

    # Chart for stakeholder report
    plt.figure(figsize=(8, 5))
    plt.scatter(y_test, pred, alpha=0.7)
    plt.xlabel("Actual Sales/Revenue")
    plt.ylabel("Predicted Sales/Revenue")
    plt.title("Actual vs Predicted Sales")
    plt.tight_layout()
    plt.savefig(out / "actual_vs_predicted.png", dpi=160)
    plt.close()

    df.to_csv(out / "cleaned_capstone_data.csv", index=False)
    print("Capstone outputs saved to", out.resolve())


if __name__ == "__main__":
    main()
