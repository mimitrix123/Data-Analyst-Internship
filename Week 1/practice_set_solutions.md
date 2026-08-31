# Week 1 — Excel & Data Fundamentals

## Practice Set Solutions

> The supplied Week 1 material links to the Global Superstore 2016 dataset, but the ZIP does not contain the dataset itself. Therefore, the answers below give the exact Excel method/formulas and a reproducible Python solution. `sample_sales_data.csv` is included only as a small demonstration dataset; replace it with the linked dataset for the final numeric results.

## 1. Remove duplicates and handle missing values

1. Select the complete data range and convert it to a Table with **Ctrl + T**.
2. Go to **Data → Remove Duplicates**.
3. Select the columns that define a unique record, such as Order ID + Product ID.
4. Click **OK** and record the number of duplicate rows removed.
5. Find missing values using **Home → Find & Select → Go To Special → Blanks**.
6. For numeric fields, use a justified value such as the median/mean, or remove the row if the field is essential and unusable.
7. For categorical fields, use `Unknown` when appropriate.
8. Recheck the cleaned dataset and document the changes.

Useful formulas:
- Missing count: `=COUNTBLANK(A2:A1000)`
- Duplicate check: `=COUNTIF($A$2:$A$1000,A2)>1`

## 2. Pivot Table showing region-wise sales

1. Select the cleaned sales table.
2. Choose **Insert → PivotTable**.
3. Put **Region** in **Rows**.
4. Put **Sales/Revenue** in **Values** and set it to **Sum**.
5. Sort total sales from largest to smallest.
6. Format the values as currency/number.

| Region | Total Sales |
|---|---:|
| Central | Sum of Sales |
| East | Sum of Sales |
| South | Sum of Sales |
| West | Sum of Sales |
| **Grand Total** | **Total Sales** |

## 3. Mean, median and mode using Excel formulas

Assume sales are in `E2:E1000`:

- **Mean:** `=AVERAGE(E2:E1000)`
- **Median:** `=MEDIAN(E2:E1000)`
- **Mode:** `=MODE.SNGL(E2:E1000)`

Interpretation:
- Mean = arithmetic average.
- Median = middle value after sorting.
- Mode = most frequently occurring value.

## 4. Conditional formatting for top 10 sales

1. Select the Sales column.
2. Go to **Home → Conditional Formatting → Top/Bottom Rules → Top 10 Items**.
3. Keep the value at **10**.
4. Choose a highlight style.
5. The ten highest sales values are highlighted automatically.

Formula alternative:
`=E2>=LARGE($E$2:$E$1000,10)`

## 5. Bar chart for category-wise revenue

1. Create a PivotTable with **Category** in Rows and **Revenue/Sales** in Values.
2. Select the summary.
3. Choose **Insert → Bar Chart → Clustered Bar**.
4. Add the title **Category-wise Revenue**.
5. Add data labels and format the revenue axis as currency.
6. Sort categories highest-to-lowest.

## Week 1 Project — Pivot Table Dashboard

Required analysis:
- Total Revenue
- Sales by Category
- Yearly Sales Trends
- Department-wise Revenue

Recommended dashboard:
- **KPI card:** Total Revenue
- **Chart 1:** Category-wise Sales — clustered column chart
- **Chart 2:** Year-wise Sales — line chart
- **Chart 3:** Department-wise Revenue — horizontal bar chart
- **Slicers:** Year, Region, Category, Department

| Dashboard item | Rows | Values | Visual |
|---|---|---|---|
| Total Revenue | — | Sum of Sales/Revenue | KPI card |
| Sales by Category | Category | Sum of Sales | Column chart |
| Yearly Sales Trends | Year | Sum of Sales | Line chart |
| Department-wise Revenue | Department | Sum of Sales | Bar chart |

## Python solution

Run:

```bash
python week1_solution.py global_superstore_2016.xlsx
```

The script performs duplicate removal, basic missing-value treatment, descriptive statistics, and region/category/year/department summaries where those columns are present.
