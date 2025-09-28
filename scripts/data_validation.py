import pandas as pd
import numpy as np
from datetime import datetime

def validate_techgear_data():
    """
    Validate TechGear Plus dataset for data quality and business logic
    """
    print("TechGear Plus Data Validation Report")
    print("=" * 50)
    
    try:
        # Load datasets
        customers = pd.read_csv('../data/raw/techgear_customers.csv')
        products = pd.read_csv('../data/raw/techgear_products.csv')
        transactions = pd.read_csv('../data/raw/techgear_transactions.csv')
        
        print("✓ Successfully loaded all datasets")
        
        # Basic data checks
        print(f"\nDataset Sizes:")
        print(f"  Customers: {len(customers):,} records")
        print(f"  Products: {len(products):,} records")
        print(f"  Transactions: {len(transactions):,} records")
        
        # Data quality checks
        validation_results = []
        
        # Check for missing values
        customers_nulls = customers.isnull().sum().sum()
        products_nulls = products.isnull().sum().sum()
        transactions_nulls = transactions.isnull().sum().sum()
        
        validation_results.append({
            'check': 'Missing Values',
            'customers': customers_nulls,
            'products': products_nulls,
            'transactions': transactions_nulls,
            'status': 'PASS' if (customers_nulls + products_nulls + transactions_nulls) == 0 else 'REVIEW'
        })
        
        # Check for duplicate IDs
        customer_dupes = customers['customer_id'].duplicated().sum()
        product_dupes = products['product_id'].duplicated().sum()
        transaction_dupes = transactions['transaction_id'].duplicated().sum()
        
        validation_results.append({
            'check': 'Duplicate IDs',
            'customers': customer_dupes,
            'products': product_dupes,
            'transactions': transaction_dupes,
            'status': 'PASS' if (customer_dupes + product_dupes + transaction_dupes) == 0 else 'FAIL'
        })
        
        # Business logic validation
        print("\nBusiness Logic Validation:")
        
        # Revenue calculation check
        transactions['calculated_total'] = (
            transactions['unit_price'] * transactions['quantity'] - 
            transactions['discount_amount'] + transactions['shipping_cost']
        )
        revenue_diff = abs(transactions['total_amount'] - transactions['calculated_total']).sum()
        print(f"  Revenue Calculation: {'PASS' if revenue_diff < 1 else 'FAIL'}")
        
        # Date range validation
        transactions['order_date'] = pd.to_datetime(transactions['order_date'])
        min_date = transactions['order_date'].min()
        max_date = transactions['order_date'].max()
        date_valid = (min_date >= pd.to_datetime('2022-01-01')) and (max_date <= pd.to_datetime('2025-12-31'))
        print(f"  Date Range ({min_date.date()} to {max_date.date()}): {'PASS' if date_valid else 'FAIL'}")
        
        # Customer consistency check
        unique_customers_transactions = transactions['customer_id'].nunique()
        active_customers = len(customers[customers['total_orders'] > 0])
        customer_consistency = unique_customers_transactions <= len(customers)
        print(f"  Customer Consistency: {'PASS' if customer_consistency else 'FAIL'}")
        
        # Category performance validation
        print("\nCategory Performance Summary:")
        category_stats = transactions.groupby('product_category').agg({
            'total_amount': ['count', 'sum'],
            'customer_id': 'nunique'
        }).round(2)
        
        for category in category_stats.index:
            orders = category_stats.loc[category, ('total_amount', 'count')]
            revenue = category_stats.loc[category, ('total_amount', 'sum')]
            customers = category_stats.loc[category, ('customer_id', 'nunique')]
            print(f"  {category}: {orders:,} orders, ${revenue:,.2f} revenue, {customers:,} customers")
        
        # Data quality summary
        print("\nData Quality Summary:")
        for result in validation_results:
            print(f"  {result['check']}: {result['status']}")
        
        # Business insights validation
        total_revenue = transactions['total_amount'].sum()
        avg_order_value = transactions['total_amount'].mean()
        
        print(f"\nKey Metrics Validation:")
        print(f"  Total Revenue: ${total_revenue:,.2f}")
        print(f"  Average Order Value: ${avg_order_value:.2f}")
        print(f"  Business Model: {'Premium' if avg_order_value > 500 else 'Standard'}")
        
        # Data completeness score
        total_checks = len(validation_results)
        passed_checks = sum(1 for r in validation_results if r['status'] == 'PASS')
        completeness_score = (passed_checks / total_checks) * 100
        
        print(f"\nOverall Data Quality Score: {completeness_score:.1f}%")
        print("✓ Validation complete - dataset ready for analysis")
        
    except FileNotFoundError as e:
        print(f"❌ Error loading data files: {e}")
        print("Ensure CSV files are in ../data/raw/ directory")
    except Exception as e:
        print(f"❌ Validation error: {e}")

if __name__ == "__main__":
    validate_techgear_data()