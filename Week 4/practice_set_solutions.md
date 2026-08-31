# Week 4 — Capstone Project Solutions

## 1. EDA

- Load the dataset and inspect shape, data types, duplicates and missing values.
- Calculate descriptive statistics for numerical columns.
- Inspect categorical distributions.
- Check sales/revenue by category, region and department.
- Create time features from the order date and inspect yearly/monthly trends.
- Use histograms, bar charts, line charts and scatter plots to identify patterns and outliers.

## 2. Regression model to predict sales

- Target: `Sales` / `Revenue` / `Amount`.
- Predictors: available numerical and categorical business variables.
- Split data into training and testing sets (80/20).
- Impute missing values.
- One-hot encode categorical variables.
- Train a baseline Linear Regression model.
- Evaluate with **MAE**, **RMSE**, and **R²**.
- Use the metrics to judge how useful the baseline model is before considering stronger models such as Random Forest or Gradient Boosting.

Executable implementation: `capstone_solution.py`.

## 3. Power BI dashboard

Create the following pages/visuals:

### KPI cards
- Total Revenue
- Total Orders
- Total Quantity
- Average Order Value
- Profit, if available

### Main visuals
- Revenue by Category — clustered column chart
- Revenue by Region — map/bar chart
- Monthly/Yearly Revenue — line chart
- Department-wise Revenue — bar chart
- Category × Region — matrix/heatmap

### Filters / slicers
- Year
- Region
- Category
- Department

### Useful DAX measures
```DAX
Total Revenue = SUM(Sales[Sales])
Total Orders = DISTINCTCOUNT(Sales[Order ID])
Total Quantity = SUM(Sales[Quantity])
Average Order Value = DIVIDE([Total Revenue], [Total Orders])
```

## 4. Stakeholder summary

**Executive finding format:** Revenue performance should be assessed by category, region, department and time. The dashboard highlights the strongest revenue contributors and periods of growth or decline, while the regression model provides a baseline estimate of how well available business variables explain sales.

**Recommendations:**
1. Prioritize high-revenue categories and regions while protecting their margins.
2. Investigate low-performing segments for pricing, product mix and demand issues.
3. Use monthly trends to improve inventory and campaign planning.
4. Track average order value and order volume together rather than relying on revenue alone.
5. Compare model predictions with actual sales and improve the model after establishing a reliable baseline.

## 5. Final deliverables checklist

- [x] Python cleaning/EDA script
- [x] Regression model script
- [x] SQL/Pandas analysis approach
- [x] Power BI dashboard design specification
- [x] Findings and recommendations template
- [ ] Final `.pbix` file after loading the actual dataset into Power BI
- [ ] Final numeric report after the actual dataset is supplied

The Week 4 PDF asks for an end-to-end case study covering Python cleaning/exploration, SQL or Pandas analysis, Excel/BI visualization and a final report. The uploaded ZIP does not include the actual linked dataset, so final numeric insights and a genuine `.pbix` file cannot be truthfully generated from the available materials.
