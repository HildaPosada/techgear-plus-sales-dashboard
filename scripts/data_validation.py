"""Validate source files from any working directory. Return nonzero on failures."""
from pathlib import Path
import sys
import pandas as pd


def validate_techgear_data(data_dir=None):
    data_dir = Path(data_dir) if data_dir else Path(__file__).resolve().parents[1] / 'data/raw'
    try:
        customers = pd.read_csv(data_dir / 'techgear_customers.csv')
        products = pd.read_csv(data_dir / 'techgear_products.csv')
        transactions = pd.read_csv(data_dir / 'techgear_transactions.csv')
        checks = {}
        checks['Unique, populated IDs'] = all(
            not df[col].isna().any() and not df[col].duplicated().any()
            for df, col in [(customers, 'customer_id'), (products, 'product_id'),
                            (transactions, 'transaction_id')])
        # A customer with no orders legitimately has no last order date.
        checks['Required fields populated'] = (
            not customers.drop(columns=['last_order_date']).isna().any().any()
            and not products.isna().any().any()
            and not transactions.isna().any().any()
            and (customers.last_order_date.isna() == (customers.total_orders == 0)).all())
        checks['Customer and product references'] = (
            transactions.customer_id.isin(customers.customer_id).all()
            and transactions.product_id.isin(products.product_id).all())
        dates = pd.to_datetime(transactions.order_date, errors='coerce')
        checks['Date coverage'] = (dates.notna().all()
                                  and dates.between('2022-01-01', '2025-12-31').all())
        checks['Valid quantities and amounts'] = (
            (transactions.quantity > 0).all()
            and (transactions.quantity % 1 == 0).all()
            and (transactions[['unit_price', 'discount_amount', 'shipping_cost',
                               'total_amount']] >= 0).all().all())
        calculated = (transactions.unit_price * transactions.quantity
                      - transactions.discount_amount + transactions.shipping_cost)
        delta = (transactions.total_amount - calculated).abs()
        # Legacy generator rounded its exported unit price after multiplying.
        # Bound is explicit, per row, and never excuses discrepancies beyond rounding.
        tolerance = transactions.quantity * 0.005 + 0.01
        checks['Amounts within legacy rounding bound'] = (delta <= tolerance + 1e-8).all()
        actual_orders = transactions.groupby('customer_id').size()
        checks['Customer order totals'] = (
            customers.customer_id.map(actual_orders).fillna(0).eq(customers.total_orders).all())
        print('TechGear source validation')
        for label, passed in checks.items():
            print(f"{'PASS' if passed else 'FAIL'}: {label}")
        currency_rows = int((delta > 0.01000001).sum())
        if currency_rows:
            print(f'WARNING: {currency_rows} legacy rows differ by more than one cent; '
                  f'maximum difference ${delta.max():.2f}.')
            print('Recorded total_amount is retained. This is not a clean financial ledger.')
            print('The generator now rounds unit prices and discounts before computing totals.')
        failures = sum(not bool(passed) for passed in checks.values())
        print(f'{len(checks) - failures}/{len(checks)} checks passed; {failures} failures.')
        return 1 if failures else 0
    except Exception as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(validate_techgear_data())
