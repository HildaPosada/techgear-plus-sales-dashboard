-- TechGear Plus Product Performance Analysis
-- Category breakdown and top-performing products
-- Works with: techgear_customers, techgear_products, techgear_transactions

-- =====================================================
-- PRODUCT CATEGORY PERFORMANCE
-- =====================================================

-- Category revenue breakdown with full metrics
SELECT 
    product_category,
    COUNT(*) as total_orders,
    '$' || printf('%,.2f', SUM(total_amount)) as total_revenue,
    ROUND(SUM(total_amount) * 100.0 / (SELECT SUM(total_amount) FROM techgear_transactions), 1) || '%' as revenue_share,
    '$' || printf('%.2f', AVG(total_amount)) as avg_order_value,
    SUM(quantity) as units_sold,
    COUNT(DISTINCT customer_id) as unique_customers
FROM techgear_transactions
GROUP BY product_category
ORDER BY SUM(total_amount) DESC;

-- Category performance with margins analysis
SELECT 
    p.category,
    COUNT(t.transaction_id) as total_orders,
    '$' || printf('%,.2f', SUM(t.total_amount)) as total_revenue,
    '$' || printf('%.2f', AVG(t.unit_price)) as avg_selling_price,
    '$' || printf('%.2f', AVG(p.retail_price)) as avg_retail_price,
    '$' || printf('%.2f', AVG(p.cost_price)) as avg_cost_price,
    ROUND(AVG((p.retail_price - p.cost_price) / p.retail_price * 100), 1) || '%' as avg_margin_percent
FROM techgear_products p
JOIN techgear_transactions t ON p.product_id = t.product_id
GROUP BY p.category
ORDER BY SUM(t.total_amount) DESC;

-- =====================================================
-- TOP PERFORMING PRODUCTS
-- =====================================================

-- Top 10 products by revenue
SELECT 
    product_name,
    product_category,
    COUNT(*) as times_sold,
    '$' || printf('%,.2f', SUM(total_amount)) as total_revenue,
    '$' || printf('%.2f', AVG(unit_price)) as avg_price,
    SUM(quantity) as total_units_sold
FROM techgear_transactions
GROUP BY product_name, product_category
ORDER BY SUM(total_amount) DESC
LIMIT 10;

-- Top 10 products by volume (units sold)
SELECT 
    product_name,
    product_category,
    SUM(quantity) as total_units_sold,
    COUNT(*) as total_orders,
    '$' || printf('%,.2f', SUM(total_amount)) as total_revenue,
    '$' || printf('%.2f', AVG(unit_price)) as avg_price
FROM techgear_transactions
GROUP BY product_name, product_category
ORDER BY SUM(quantity) DESC
LIMIT 10;

-- Most profitable products (by margin)
SELECT 
    t.product_name,
    t.product_category,
    COUNT(*) as times_sold,
    '$' || printf('%,.2f', SUM(t.total_amount)) as total_revenue,
    '$' || printf('%.2f', AVG(p.retail_price - p.cost_price)) as avg_profit_per_unit,
    '$' || printf('%,.2f', SUM((t.unit_price - p.cost_price) * t.quantity)) as estimated_total_profit,
    ROUND(AVG((p.retail_price - p.cost_price) / p.retail_price * 100), 1) || '%' as avg_margin_percent
FROM techgear_transactions t
JOIN techgear_products p ON t.product_id = p.product_id
GROUP BY t.product_name, t.product_category
ORDER BY SUM((t.unit_price - p.cost_price) * t.quantity) DESC
LIMIT 10;

-- =====================================================
-- PRODUCT LAUNCH ANALYSIS
-- =====================================================

-- Product performance by launch date
SELECT 
    strftime('%Y', p.launch_date) as launch_year,
    COUNT(DISTINCT p.product_id) as products_launched,
    COUNT(t.transaction_id) as total_orders,
    '$' || printf('%,.2f', SUM(t.total_amount)) as total_revenue,
    '$' || printf('%.2f', AVG(t.total_amount)) as avg_order_value
FROM techgear_products p
LEFT JOIN techgear_transactions t ON p.product_id = t.product_id
GROUP BY strftime('%Y', p.launch_date)
ORDER BY launch_year;

-- New vs established products performance
SELECT 
    CASE 
        WHEN julianday('2024-01-01') - julianday(p.launch_date) <= 365 THEN 'New Products (< 1 year)'
        WHEN julianday('2024-01-01') - julianday(p.launch_date) <= 730 THEN 'Recent Products (1-2 years)'
        ELSE 'Established Products (2+ years)'
    END as product_age_group,
    COUNT(DISTINCT p.product_id) as product_count,
    COUNT(t.transaction_id) as total_orders,
    '$' || printf('%,.2f', SUM(t.total_amount)) as total_revenue,
    '$' || printf('%.2f', AVG(t.total_amount)) as avg_order_value
FROM techgear_products p
LEFT JOIN techgear_transactions t ON p.product_id = t.product_id
GROUP BY product_age_group
ORDER BY SUM(t.total_amount) DESC;

-- =====================================================
-- PRODUCT PORTFOLIO ANALYSIS
-- =====================================================

-- Product performance distribution (80/20 analysis)
WITH product_revenue AS (
    SELECT 
        product_name,
        product_category,
        SUM(total_amount) as revenue,
        COUNT(*) as orders
    FROM techgear_transactions
    GROUP BY product_name, product_category
),
ranked_products AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY revenue DESC) as rank,
        SUM(revenue) OVER () as total_company_revenue,
        SUM(revenue) OVER (ORDER BY revenue DESC ROWS UNBOUNDED PRECEDING) as cumulative_revenue
    FROM product_revenue
)
SELECT 
    CASE 
        WHEN cumulative_revenue <= total_company_revenue * 0.8 THEN 'Top 80% Revenue Products'
        ELSE 'Bottom 20% Revenue Products'
    END as product_tier,
    COUNT(*) as product_count,
    '$' || printf('%,.2f', SUM(revenue)) as total_revenue,
    ROUND(SUM(revenue) * 100.0 / MAX(total_company_revenue), 1) || '%' as revenue_share
FROM ranked_products
GROUP BY 
    CASE 
        WHEN cumulative_revenue <= total_company_revenue * 0.8 THEN 'Top 80% Revenue Products'
        ELSE 'Bottom 20% Revenue Products'
    END;

-- Products with no sales (inventory optimization)
SELECT 
    p.product_name,
    p.category,
    p.retail_price,
    p.launch_date,
    julianday('now') - julianday(p.launch_date) as days_since_launch
FROM techgear_products p
LEFT JOIN techgear_transactions t ON p.product_id = t.product_id
WHERE t.product_id IS NULL
ORDER BY p.launch_date DESC;

-- =====================================================
-- CATEGORY TRENDS OVER TIME
-- =====================================================

-- Monthly category performance trends
SELECT 
    strftime('%Y-%m', order_date) as month,
    product_category,
    COUNT(*) as orders,
    '$' || printf('%,.2f', SUM(total_amount)) as revenue,
    '$' || printf('%.2f', AVG(total_amount)) as avg_order_value
FROM techgear_transactions
GROUP BY strftime('%Y-%m', order_date), product_category
ORDER BY month, product_category;