# Sales dashboard

The deployed dashboard reads `summary.json`, generated from the repository's synthetic transaction CSV. It reports recorded total_amount including shipping and subtracting discounts. The year selector changes the monthly chart and recorded sales total; the other cards and breakdowns are explicitly all-years.

From the repository root:

```sh
python scripts/build_web_summary.py
python scripts/data_validation.py
```

The summary generator uses Decimal cents and asserts that all group totals reconcile. The validator returns nonzero on failures. The historical dataset has 677 rows with rounding differences above one cent, up to $0.03, within the documented legacy rounding bound. Recorded totals are retained; newly generated data rounds adjusted unit prices and discounts before calculating totals.

Vercel: Framework Other, Root Directory `web`.
