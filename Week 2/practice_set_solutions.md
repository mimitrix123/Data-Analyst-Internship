# Week 2 — Python for Data Analysis + SQL

## Practice Questions — Solved

### 1. Load CSV and display basic information
```python
import pandas as pd

df = pd.read_csv("data.csv")
print(df.head())
print(df.shape)
print(df.columns)
print(df.info())
print(df.describe(include="all"))
```

### 2. Handle missing values and duplicates
```python
print(df.isna().sum())
df = df.drop_duplicates().copy()
num_cols = df.select_dtypes(include="number").columns
cat_cols = df.select_dtypes(exclude="number").columns
for c in num_cols:
    df[c] = df[c].fillna(df[c].median())
for c in cat_cols:
    df[c] = df[c].fillna("Unknown")
```

### 3. Group by category and find total revenue
```python
result = df.groupby("Category", as_index=False)["Revenue"].sum()
result = result.sort_values("Revenue", ascending=False)
print(result)
```

### 4. Sort by multiple columns
```python
sorted_df = df.sort_values(["Category", "Revenue"], ascending=[True, False])
print(sorted_df)
```

### 5. Correlation matrix
```python
corr = df.select_dtypes(include="number").corr()
print(corr.round(2))
```

## SQL Assignment — solved patterns

### Top customers
```sql
SELECT customer_id,
       SUM(amount) AS total_spend,
       COUNT(DISTINCT order_id) AS orders
FROM orders
GROUP BY customer_id
ORDER BY total_spend DESC
LIMIT 10;
```

### Average order value
```sql
SELECT AVG(order_total) AS average_order_value
FROM (
    SELECT order_id, SUM(amount) AS order_total
    FROM orders
    GROUP BY order_id
) x;
```

### Category revenue
```sql
SELECT category, SUM(amount) AS total_revenue
FROM orders
GROUP BY category
ORDER BY total_revenue DESC;
```

### JOIN + CASE
```sql
SELECT c.customer_name,
       SUM(o.amount) AS revenue,
       CASE
           WHEN SUM(o.amount) >= 10000 THEN 'High Value'
           WHEN SUM(o.amount) >= 5000 THEN 'Medium Value'
           ELSE 'Standard'
       END AS customer_segment
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY revenue DESC;
```

### Subquery — customers above average spend
```sql
SELECT customer_id, total_spend
FROM (
    SELECT customer_id, SUM(amount) AS total_spend
    FROM orders
    GROUP BY customer_id
) s
WHERE total_spend > (SELECT AVG(total_spend) FROM (
    SELECT customer_id, SUM(amount) AS total_spend
    FROM orders
    GROUP BY customer_id
) a);
```

> Column names may need to be changed to match the supplied database.
