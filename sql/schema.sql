-- TechGear Plus Database Schema
-- Table structures and initial setup

-- Data validation queries
SELECT 'techgear_customers' as table_name, COUNT(*) as records FROM techgear_customers
UNION ALL
SELECT 'techgear_products', COUNT(*) FROM techgear_products  
UNION ALL
SELECT 'techgear_transactions', COUNT(*) FROM techgear_transactions;