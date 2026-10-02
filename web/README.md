# Source-backed sales dashboard

`summary.json` aggregates the repository's three synthetic CSV files. It contains 50,000 transactions totaling $35,890,284.39 in `total_amount`. That field subtracts discounts and includes shipping. The monthly chart and total respond to the year filter; category, channel, transaction count, and average show all years, as labeled.

Vercel: Framework Other, Root Directory `web`. This is a published dataset snapshot, not a live sales feed. Regenerate the summary when the source CSVs change. No model or paid API is required.
