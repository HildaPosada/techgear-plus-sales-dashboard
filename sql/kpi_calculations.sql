-- TechGear Plus Key Performance Indicators
-- Main business metrics for executive dashboard
-- Works with: techgear_customers, techgear_products, techgear_transactions

-- =====================================================
-- DATA VALIDATION
-- =====================================================

-- Verify data exists in all tables
SELECT 'techgear_customers' as table_name, COUNT(*) as records FROM techgear_customers
UNION ALL
SELECT 'techgear_products', COUNT(*) FROM techgear_products  
UNION ALL
SELECT 'techgear_transactions', COUNT(*) FROM techgear_transactions;

-- =====================================================
-- EXECUTIVE SUMMARY KPIs
-- =====================================================

-- Overall business KPIs
SELECT 
    'Total Revenue' as metric,
    '$' || printf('%,.2f', SUM(total_amount)) as value
FROM techgear_transactions
UNION ALL
SELECT 
    'Total Orders',
    printf('%,d', COUNT(*))
FROM techgear_transactions
UNION ALL
SELECT 
    'Average Order Value',
    '$' || printf('%.2f', AVG(total_amount))
FROM techgear_transactions
UNION ALL
SELECT 
    'Total Customers',
    printf('%,d', COUNT(DISTINCT customer_id))
FROM techgear_transactions
UNION ALL
SELECT 
    'Active Customers',
    printf('%,d', COUNT(DISTINCT customer_id))
FROM techgear_customers
WHERE total_orders > 0;

-- =====================================================
-- GROWTH ANALYSIS
-- =====================================================

-- Year-over-year growth analysis
WITH yearly_revenue AS (
    SELECT 
        strftime('%Y', order_date) as year,
        SUM(total_amount) as revenue
    FROM techgear_transactions
    GROUP BY strftime('%Y', order_date)
)
SELECT 
    year,
    '$' || printf('%,.2f', revenue) as revenue,
    CASE 
        WHEN LAG(revenue) OVER (ORDER BY year) IS NOT NULL 
        THEN printf('%.1f%%', 
            ((revenue - LAG(revenue) OVER (ORDER BY year)) / 
             LAG(revenue) OVER (ORDER BY year)) * 100
        )
        ELSE 'N/A'
    END as yoy_growth
FROM yearly_revenue
ORDER BY year;

-- Monthly revenue trends
SELECT 
    strftime('%Y-%m', order_date) as month,
    COUNT(*) as total_orders,
    '$' || printf('%,.2f', SUM(total_amount)) as total_revenue,
    '$' || printf('%.2f', AVG(total_amount)) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM techgear_transactions
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;

-- =====================================================
-- SALES CHANNEL PERFORMANCE
-- =====================================================

-- Channel revenue analysis
SELECT 
    sales_channel,
    COUNT(*) as total_orders,
    '$' || printf('%,.2f', SUM(total_amount)) as total_revenue,
    ROUND(SUM(total_amount) * 100.0 / (SELECT SUM(total_amount) FROM techgear_transactions), 1) || '%' as revenue_share,
    '$' || printf('%.2f', AVG(total_amount)) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers,
    '$' || printf('%.2f', SUM(total_amount) / COUNT(DISTINCT customer_id)) as revenue_per_customer
FROM techgear_transactions
GROUP BY sales_channel
ORDER BY SUM(total_amount) DESC;

-- =====================================================
-- GEOGRAPHIC PERFORMANCE
-- =====================================================

-- Regional sales breakdown
SELECT 
    region,
    COUNT(*) as total_orders,
    '$' || printf('%,.2f', SUM(total_amount)) as total_revenue,
    ROUND(SUM(total_amount) * 100.0 / (SELECT SUM(total_amount) FROM techgear_transactions), 1) || '%' as revenue_share,
    '$' || printf('%.2f', AVG(total_amount)) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM techgear_transactions
GROUP BY region
ORDER BY SUM(total_amount) DESC;

-- =====================================================
-- SEASONAL ANALYSIS
-- =====================================================

-- Seasonal trends (by month)
SELECT 
    strftime('%m', order_date) as month_num,
    CASE strftime('%m', order_date)
        WHEN '01' THEN 'January'
        WHEN '02' THEN 'February'  
        WHEN '03' THEN 'March'
        WHEN '04' THEN 'April'
        WHEN '05' THEN 'May'
        WHEN '06' THEN 'June'
        WHEN '07' THEN 'July'
        WHEN '08' THEN 'August'
        WHEN '09' THEN 'September'
        WHEN '10' THEN 'October'
        WHEN '11' THEN 'November'
        WHEN '12' THEN 'December'
    END as month_name,
    COUNT(*) as total_orders,
    '$' || printf('%,.2f', SUM(total_amount)) as total_revenue,
    '$' || printf('%.2f', AVG(total_amount)) as avg_order_value
FROM techgear_transactions
GROUP BY strftime('%m', order_date)
ORDER BY SUM(total_amount) DESC;

-- =====================================================
-- TABLEAU-READY EXECUTIVE SUMMARY
-- =====================================================

-- Complete executive summary for dashboard
SELECT 
    (SELECT COUNT(*) FROM techgear_transactions) as total_transactions,
    (SELECT COUNT(DISTINCT customer_id) FROM techgear_transactions) as active_customers,
    (SELECT COUNT(*) FROM techgear_products) as total_products,
    (SELECT printf('$%,.2f', SUM(total_amount)) FROM techgear_transactions) as total_revenue,
    (SELECT printf('$%.2f', AVG(total_amount)) FROM techgear_transactions) as avg_order_value,
    (SELECT MIN(order_date) FROM techgear_transactions) as first_order_date,
    (SELECT MAX(order_date) FROM techgear_transactions) as last_order_date;