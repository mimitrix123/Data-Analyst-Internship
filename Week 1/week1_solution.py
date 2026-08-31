"""Week 1 Excel & Data Fundamentals - reproducible solution.

Usage:
    python week1_solution.py path/to/data.xlsx
    python week1_solution.py path/to/data.csv
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd


def load_data(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    return pd.read_csv(path)


def find_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    normalized = {str(c).strip().lower(): c for c in df.columns}
    for name in candidates:
        if name.lower() in normalized:
            return normalized[name.lower()]
    for c in df.columns:
        low = str(c).strip().lower()
        if any(name.lower() in low for name in candidates):
            return c
    return None


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python week1_solution.py <csv-or-excel-file>")

    source = Path(sys.argv[1])
    df = load_data(source)
    out = Path("week1_output")
    out.mkdir(exist_ok=True)

    duplicate_count = int(df.duplicated().sum())
    clean = df.drop_duplicates().copy()

    for col in clean.columns:
        if pd.api.types.is_numeric_dtype(clean[col]):
            if clean[col].isna().any():
                clean[col] = clean[col].fillna(clean[col].median())
        else:
            clean[col] = clean[col].fillna("Unknown")

    sales_col = find_col(clean, ["Sales", "Revenue", "Amount"])
    region_col = find_col(clean, ["Region"])
    category_col = find_col(clean, ["Category"])
    department_col = find_col(clean, ["Department", "Dept"])
    date_col = find_col(clean, ["Order Date", "Date", "OrderDate"])

    if not sales_col:
        raise SystemExit("Could not identify a Sales/Revenue column.")

    sales = pd.to_numeric(clean[sales_col], errors="coerce").dropna()
    stats = pd.DataFrame({
        "metric": ["duplicate_rows_removed", "mean", "median", "mode"],
        "value": [duplicate_count, sales.mean(), sales.median(), sales.mode().iloc[0] if not sales.mode().empty else None],
    })
    stats.to_csv(out / "descriptive_statistics.csv", index=False)

    if region_col:
        clean.groupby(region_col, dropna=False)[sales_col].sum().sort_values(ascending=False).to_csv(out / "region_wise_sales.csv", header=["Total Sales"])
    if category_col:
        clean.groupby(category_col, dropna=False)[sales_col].sum().sort_values(ascending=False).to_csv(out / "category_wise_revenue.csv", header=["Total Revenue"])
    if department_col:
        clean.groupby(department_col, dropna=False)[sales_col].sum().sort_values(ascending=False).to_csv(out / "department_wise_revenue.csv", header=["Total Revenue"])
    if date_col:
        dates = pd.to_datetime(clean[date_col], errors="coerce")
        yearly = clean.assign(_year=dates.dt.year).dropna(subset=["_year"])
        yearly.groupby("_year")[sales_col].sum().sort_index().to_csv(out / "yearly_sales_trend.csv", header=["Total Sales"])

    clean.to_csv(out / "cleaned_data.csv", index=False)
    print(f"Done. Cleaned {len(df)} rows -> {len(clean)} rows. Output: {out.resolve()}")


if __name__ == "__main__":
    main()
