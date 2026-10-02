"""Rebuild the web dashboard's summary from repository CSVs using exact cents."""
import csv
import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path


def build_summary(root):
    totals = {key: defaultdict(Decimal) for key in ('monthly', 'categories', 'channels')}
    dates = []
    count = 0
    revenue = Decimal(0)
    with (root / 'data/raw/techgear_transactions.csv').open(newline='') as handle:
        for row in csv.DictReader(handle):
            amount = Decimal(row['total_amount'])
            revenue += amount
            count += 1
            dates.append(row['order_date'][:10])
            for group, key in [('monthly', row['order_date'][:7]),
                               ('categories', row['product_category']),
                               ('channels', row['sales_channel'])]:
                totals[group][key] += amount
    if not count:
        raise ValueError('No transactions to summarize')
    for group in totals.values():
        assert sum(group.values()) == revenue, 'Group totals must reconcile to source'
    result = dict(transactions=count, revenue=float(revenue))
    result.update({name: {key: float(value) for key, value in sorted(group.items())}
                   for name, group in totals.items()})
    result.update(date_start=min(dates), date_end=max(dates), source=
                  'Repository synthetic TechGear+ transaction dataset; total_amount includes shipping and subtracts discounts.')
    output = root / 'web/summary.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(f'{count:,} transactions; recorded total ${revenue:,.2f}; wrote {output}')
    return result


if __name__ == '__main__':
    build_summary(Path(__file__).resolve().parents[1])
