# [TechGear+ Sales Dashboard](https://dashboard-demo-gray.vercel.app/)

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![SQL](https://img.shields.io/badge/SQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/current/tutorial-sql.html)
[![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![Vercel](https://img.shields.io/badge/Vercel-171717?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)

Explore 50,000 synthetic sales transactions with coordinated filters and downloadable monthly summaries.

## Explore

Year, category, channel, and region filters update every KPI and chart. The dashboard identifies the largest category contributor within the selected records.

## Data

- Recorded sales amount: **$35,890,284.39**.
- Date coverage: January 1, 2022 through September 28, 2025.
- 2025 is partial. Full-year growth comparisons would be misleading.
- Recorded totals include shipping and subtract discounts.

The explorer aggregates source amounts in integer cents and reconciles all 50,000 transactions. Synthetic data demonstrates the analysis workflow, not actual business performance.

## Files

- `data/raw/`: source transactions, products, and customers.
- `scripts/`: data generation and validation.
- `sql/`: analytical queries.
- `web/`: deployed dashboard and aggregation data.
