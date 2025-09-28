import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Business configuration
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2025, 9, 28)
TOTAL_TRANSACTIONS = 50000

# Product categories with business rules
PRODUCT_CATEGORIES = {
    'Laptops & Computers': {
        'revenue_share': 0.35,
        'avg_price': 899,
        'price_range': (399, 2499),
        'margin': 0.22,
        'seasonal_boost': {'back_to_school': 1.4, 'holiday': 1.2}
    },
    'Mobile & Accessories': {
        'revenue_share': 0.25,
        'avg_price': 149,
        'price_range': (19, 899),
        'margin': 0.45,
        'seasonal_boost': {'holiday': 1.6}
    },
    'Gaming Equipment': {
        'revenue_share': 0.20,
        'avg_price': 349,
        'price_range': (29, 699),
        'margin': 0.35,
        'seasonal_boost': {'holiday': 1.8, 'summer': 1.3}
    },
    'Audio & Headphones': {
        'revenue_share': 0.15,
        'avg_price': 199,
        'price_range': (39, 599),
        'margin': 0.40,
        'seasonal_boost': {'holiday': 1.4}
    },
    'Smart Home Devices': {
        'revenue_share': 0.05,
        'avg_price': 179,
        'price_range': (49, 449),
        'margin': 0.28,
        'seasonal_boost': {'holiday': 1.3}
    }
}

# Sales channels with characteristics
SALES_CHANNELS = {
    'Website': {'share': 0.65, 'conversion_rate': 0.035, 'cac': 45},
    'Amazon': {'share': 0.20, 'conversion_rate': 0.028, 'cac': 35},
    'Retail Partners': {'share': 0.10, 'conversion_rate': 0.042, 'cac': 25},
    'Mobile App': {'share': 0.05, 'conversion_rate': 0.055, 'cac': 30}
}

# Geographic regions
REGIONS = {
    'West Coast': 0.35,
    'Northeast': 0.25,
    'Southeast': 0.20,
    'Midwest': 0.15,
    'Southwest': 0.05
}

# Customer segments
CUSTOMER_SEGMENTS = {
    'New': {'share': 0.40, 'aov_multiplier': 0.8},
    'Returning': {'share': 0.45, 'aov_multiplier': 1.6},
    'VIP': {'share': 0.15, 'aov_multiplier': 2.2}
}

def generate_product_catalog():
    """Generate realistic product catalog"""
    products = []
    product_id_counter = 1
    
    for category, config in PRODUCT_CATEGORIES.items():
        # Generate 15-25 products per category
        num_products = random.randint(15, 25)
        
        for i in range(num_products):
            # Generate realistic product names
            if category == 'Laptops & Computers':
                brands = ['TechPro', 'CompuMax', 'EliteBook', 'PowerStation']
                models = ['X1', 'Pro 15', 'Gaming Elite', 'Business Series', 'Ultra Thin']
            elif category == 'Mobile & Accessories':
                brands = ['PhoneGuard', 'MobiTech', 'PowerCell', 'ConnectPro']
                models = ['Wireless Charger', 'Screen Protector', 'Phone Case', 'Car Mount', 'Power Bank']
            elif category == 'Gaming Equipment':
                brands = ['GameMaster', 'ProPlayer', 'EliteGaming', 'TurboGear']
                models = ['Mechanical Keyboard', 'Gaming Mouse', 'Headset Pro', 'Controller Elite', 'Gaming Chair']
            elif category == 'Audio & Headphones':
                brands = ['SoundWave', 'AudioPro', 'BassMax', 'ClearSound']
                models = ['Wireless Earbuds', 'Over-Ear Headphones', 'Bluetooth Speaker', 'Sound Bar']
            else:  # Smart Home
                brands = ['SmartLife', 'HomeConnect', 'AutoHome', 'TechNest']
                models = ['Smart Thermostat', 'Security Camera', 'Smart Bulb', 'Voice Assistant', 'Smart Lock']
            
            product_name = f"{random.choice(brands)} {random.choice(models)}"
            
            # Price distribution within category
            price = np.random.normal(config['avg_price'], config['avg_price'] * 0.3)
            price = max(config['price_range'][0], min(config['price_range'][1], price))
            price = round(price, 2)
            
            cost_price = price * (1 - config['margin'])
            
            products.append({
                'product_id': f"P{product_id_counter:05d}",
                'product_name': product_name,
                'category': category,
                'retail_price': price,
                'cost_price': round(cost_price, 2),
                'launch_date': START_DATE + timedelta(days=random.randint(0, 700)),
                'supplier': f"Supplier_{random.randint(1, 20)}"
            })
            product_id_counter += 1
    
    return pd.DataFrame(products)

def get_seasonal_multiplier(date, category):
    """Calculate seasonal multiplier for given date and category"""
    month = date.month
    multiplier = 1.0
    
    # Holiday season (Nov-Dec)
    if month in [11, 12]:
        multiplier *= PRODUCT_CATEGORIES[category]['seasonal_boost'].get('holiday', 1.0)
    
    # Back to school (August)
    elif month == 8 and 'back_to_school' in PRODUCT_CATEGORIES[category]['seasonal_boost']:
        multiplier *= PRODUCT_CATEGORIES[category]['seasonal_boost']['back_to_school']
    
    # Summer gaming (June-July)
    elif month in [6, 7] and 'summer' in PRODUCT_CATEGORIES[category]['seasonal_boost']:
        multiplier *= PRODUCT_CATEGORIES[category]['seasonal_boost']['summer']
    
    return multiplier

def generate_customer_base(num_customers=15000):
    """Generate customer base with realistic acquisition patterns"""
    customers = []
    
    for i in range(num_customers):
        # Customer acquisition date - more recent customers more likely
        days_ago = int(np.random.exponential(365))  # Exponential distribution
        registration_date = END_DATE - timedelta(days=min(days_ago, 1000))
        
        customer_segment = np.random.choice(
            list(CUSTOMER_SEGMENTS.keys()),
            p=list(seg['share'] for seg in CUSTOMER_SEGMENTS.values())
        )
        
        acquisition_channels = ['Organic Search', 'Paid Search', 'Social Media', 
                              'Email Marketing', 'Referral', 'Direct']
        acquisition_channel = np.random.choice(acquisition_channels)
        
        customers.append({
            'customer_id': f"C{i+1:06d}",
            'registration_date': registration_date,
            'customer_segment': customer_segment,
            'acquisition_channel': acquisition_channel,
            'total_orders': 0,  # Will be updated later
            'total_spent': 0.0,  # Will be updated later
            'last_order_date': None  # Will be updated later
        })
    
    return pd.DataFrame(customers)

def generate_sales_transactions(products_df, customers_df):
    """Generate realistic sales transactions"""
    transactions = []
    
    # Calculate number of transactions per category
    category_transactions = {}
    for category, config in PRODUCT_CATEGORIES.items():
        category_transactions[category] = int(TOTAL_TRANSACTIONS * config['revenue_share'])
    
    # Adjust to exact total
    total_allocated = sum(category_transactions.values())
    if total_allocated != TOTAL_TRANSACTIONS:
        largest_category = max(category_transactions, key=category_transactions.get)
        category_transactions[largest_category] += TOTAL_TRANSACTIONS - total_allocated
    
    transaction_id_counter = 1
    
    # Generate transactions for each category
    for category, num_transactions in category_transactions.items():
        category_products = products_df[products_df['category'] == category]
        
        for _ in range(num_transactions):
            # Random date with business growth trend
            days_from_start = random.randint(0, (END_DATE - START_DATE).days)
            order_date = START_DATE + timedelta(days=days_from_start)
            
            # Growth factor (15% YoY growth)
            years_elapsed = (order_date - START_DATE).days / 365.25
            growth_factor = (1.15 ** years_elapsed)
            
            # Seasonal adjustment
            seasonal_multiplier = get_seasonal_multiplier(order_date, category)
            
            # Select customer (weighted toward more recent customers)
            customer_weights = np.exp(-(customers_df['registration_date'] - order_date).dt.days / 180)
            customer_weights = customer_weights.fillna(0)
            if customer_weights.sum() == 0:
                customer_weights = np.ones(len(customers_df))
            
            customer = customers_df.sample(weights=customer_weights).iloc[0]
            
            # Select product from category
            product = category_products.sample().iloc[0]
            
            # Determine quantity (most orders are single items)
            quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.7, 0.15, 0.08, 0.04, 0.03])
            
            # Calculate base price with some variation
            unit_price = product['retail_price'] * np.random.normal(1.0, 0.05)
            unit_price = max(unit_price * 0.9, unit_price)  # No more than 10% discount
            unit_price = round(unit_price, 2)
            
            # Customer segment adjustment
            segment_multiplier = CUSTOMER_SEGMENTS[customer['customer_segment']]['aov_multiplier']
            if segment_multiplier > 1.0:
                unit_price *= np.random.uniform(1.0, min(1.2, segment_multiplier))
            
            # Calculate amounts
            subtotal = unit_price * quantity
            
            # Discount (10% of orders have discounts)
            discount_amount = 0.0
            if random.random() < 0.1:
                discount_amount = subtotal * random.uniform(0.05, 0.20)
            
            # Shipping cost
            if subtotal > 75:
                shipping_cost = 0.0  # Free shipping over $75
            else:
                shipping_cost = random.choice([5.99, 7.99, 9.99])
            
            total_amount = subtotal - discount_amount + shipping_cost
            
            # Sales channel
            channel = np.random.choice(
                list(SALES_CHANNELS.keys()),
                p=list(ch['share'] for ch in SALES_CHANNELS.values())
            )
            
            # Region
            region = np.random.choice(
                list(REGIONS.keys()),
                p=list(REGIONS.values())
            )
            
            transactions.append({
                'transaction_id': f"T{transaction_id_counter:07d}",
                'customer_id': customer['customer_id'],
                'order_date': order_date,
                'product_category': category,
                'product_name': product['product_name'],
                'product_id': product['product_id'],
                'quantity': quantity,
                'unit_price': round(unit_price, 2),
                'total_amount': round(total_amount, 2),
                'discount_amount': round(discount_amount, 2),
                'shipping_cost': round(shipping_cost, 2),
                'sales_channel': channel,
                'region': region,
                'customer_type': customer['customer_segment']
            })
            
            transaction_id_counter += 1
    
    return pd.DataFrame(transactions)

def update_customer_metrics(customers_df, transactions_df):
    """Update customer metrics based on transactions"""
    customer_stats = transactions_df.groupby('customer_id').agg({
        'total_amount': ['count', 'sum'],
        'order_date': 'max'
    }).round(2)
    
    customer_stats.columns = ['calculated_orders', 'calculated_spent', 'calculated_last_date']
    
    # Update customers dataframe - drop old columns first to avoid overlap
    customers_clean = customers_df.drop(columns=['total_orders', 'total_spent', 'last_order_date'], errors='ignore')
    
    # Join with calculated stats
    customers_updated = customers_clean.set_index('customer_id').join(
        customer_stats, how='left'
    ).fillna({
        'calculated_orders': 0,
        'calculated_spent': 0.0
    })
    
    # Rename back to original column names
    customers_updated = customers_updated.rename(columns={
        'calculated_orders': 'total_orders',
        'calculated_spent': 'total_spent', 
        'calculated_last_date': 'last_order_date'
    })
    
    return customers_updated.reset_index()

def main():
    """Generate complete TechGear Plus dataset"""
    print("Generating TechGear Plus Sales Dataset...")
    print("=" * 50)
    
    # Generate datasets
    print("1. Creating product catalog...")
    products_df = generate_product_catalog()
    print(f"   Generated {len(products_df)} products across {len(PRODUCT_CATEGORIES)} categories")
    
    print("2. Creating customer base...")
    customers_df = generate_customer_base()
    print(f"   Generated {len(customers_df)} customers")
    
    print("3. Generating sales transactions...")
    transactions_df = generate_sales_transactions(products_df, customers_df)
    print(f"   Generated {len(transactions_df)} transactions")
    
    print("4. Updating customer metrics...")
    customers_df = update_customer_metrics(customers_df, transactions_df)
    
    # Save to CSV files in the raw data folder
    print("5. Saving datasets...")
    
    # Create raw data directory if it doesn't exist
    raw_data_dir = '../data/raw'
    os.makedirs(raw_data_dir, exist_ok=True)
    
    # Save CSV files to raw data folder
    products_df.to_csv(f'{raw_data_dir}/techgear_products.csv', index=False)
    customers_df.to_csv(f'{raw_data_dir}/techgear_customers.csv', index=False)
    transactions_df.to_csv(f'{raw_data_dir}/techgear_transactions.csv', index=False)
    
    # Display summary statistics
    print("\n" + "=" * 50)
    print("DATASET SUMMARY")
    print("=" * 50)
    
    print(f"Total Revenue: ${transactions_df['total_amount'].sum():,.2f}")
    print(f"Average Order Value: ${transactions_df['total_amount'].mean():.2f}")
    print(f"Date Range: {transactions_df['order_date'].min()} to {transactions_df['order_date'].max()}")
    
    print("\nRevenue by Category:")
    category_revenue = transactions_df.groupby('product_category')['total_amount'].sum().sort_values(ascending=False)
    for category, revenue in category_revenue.items():
        percentage = (revenue / transactions_df['total_amount'].sum()) * 100
        print(f"  {category}: ${revenue:,.2f} ({percentage:.1f}%)")
    
    print("\nRevenue by Channel:")
    channel_revenue = transactions_df.groupby('sales_channel')['total_amount'].sum().sort_values(ascending=False)
    for channel, revenue in channel_revenue.items():
        percentage = (revenue / transactions_df['total_amount'].sum()) * 100
        print(f"  {channel}: ${revenue:,.2f} ({percentage:.1f}%)")
    
    print("\nCustomer Segments:")
    segment_stats = transactions_df.groupby('customer_type').agg({
        'total_amount': ['mean', 'count']
    }).round(2)
    for segment in segment_stats.index:
        avg_order = segment_stats.loc[segment, ('total_amount', 'mean')]
        order_count = segment_stats.loc[segment, ('total_amount', 'count')]
        print(f"  {segment}: {order_count} orders, ${avg_order:.2f} avg order value")
    
    print(f"\nFiles created in data/raw/ folder:")
    print("  - techgear_products.csv")
    print("  - techgear_customers.csv") 
    print("  - techgear_transactions.csv")
    
    print("\nNext Steps:")
    print("1. Upload CSV files to SQLite Online")
    print("2. Run the database setup queries")
    print("3. Start building your Tableau dashboard!")

if __name__ == "__main__":
    main()