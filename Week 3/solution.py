"""Week 3 — Python & Data Wrangling solution.
Usage: python solution.py data.csv
"""
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python solution.py <data.csv>")
    path = Path(sys.argv[1])
    df = pd.read_csv(path)

    # Inspect
    print("Shape:", df.shape)
    print("Missing values:\n", df.isna().sum())

    # Remove duplicate records
    df = df.drop_duplicates().copy()

    # Handle missing values
    for col in df.select_dtypes(include="number"):
        df[col] = df[col].fillna(df[col].median())
    for col in df.select_dtypes(exclude="number"):
        df[col] = df[col].fillna("Unknown")

    # Example filtering: keep rows with positive sales/revenue if available
    sales_col = next((c for c in df.columns if str(c).lower() in {"sales", "revenue", "amount"}), None)
    if sales_col:
        df[sales_col] = pd.to_numeric(df[sales_col], errors="coerce")
        filtered = df[df[sales_col] > 0].copy()
        df["Sales_Band"] = pd.cut(df[sales_col], bins=[-float("inf"), 1000, 5000, float("inf")], labels=["Low", "Medium", "High"])
    else:
        filtered = df.copy()

    # Create a useful derived column where quantity and unit price exist
    quantity = next((c for c in df.columns if str(c).lower() == "quantity"), None)
    price = next((c for c in df.columns if str(c).lower() in {"unit price", "unit_price", "price"}), None)
    if quantity and price:
        df["Calculated_Revenue"] = pd.to_numeric(df[quantity], errors="coerce") * pd.to_numeric(df[price], errors="coerce")

    out = Path("week3_output")
    out.mkdir(exist_ok=True)
    df.to_csv(out / "cleaned_data.csv", index=False)
    filtered.to_csv(out / "filtered_data.csv", index=False)

    # Simple visualization
    if sales_col:
        df[sales_col].plot(kind="hist", bins=20, title="Sales Distribution")
        plt.xlabel(sales_col)
        plt.tight_layout()
        plt.savefig(out / "sales_distribution.png", dpi=150)
        plt.close()

    print("Saved cleaned/filtered data and visualization to", out.resolve())


if __name__ == "__main__":
    main()
