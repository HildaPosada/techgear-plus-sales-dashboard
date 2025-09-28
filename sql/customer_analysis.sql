-- TechGear Plus Customer Analytics
-- Customer acquisition, lifetime value, and segmentation analysis

-- Customer acquisition channel performance (your great LTV/CAC analysis)
SELECT 
    acquisition_channel,
    COUNT(DISTINCT c.customer_id) as customers_acquired,
    '$' || printf('%.2f', AVG(c.total_spent)) as avg_ltv,
    CASE acquisition_channel
        WHEN 'Organic Search' THEN '$45'
        WHEN 'Paid Search' THEN '$75'
        WHEN 'Social Media' THEN '$65'
        WHEN 'Email Marketing' THEN '$25'
        WHEN 'Referral' THEN '$35'
        WHEN 'Direct' THEN '$20'
        ELSE '$50'
    END as estimated_cac,
    ROUND(AVG(c.total_spent) / 
        CASE acquisition_channel
            WHEN 'Organic Search' THEN 45
            WHEN 'Paid Search' THEN 75
            WHEN 'Social Media' THEN 65
            WHEN 'Email Marketing' THEN 25
            WHEN 'Referral' THEN 35
            WHEN 'Direct' THEN 20
            ELSE 50
        END, 2
    ) as ltv_cac_ratio
FROM techgear_customers c
WHERE c.total_orders > 0
GROUP BY acquisition_channel
ORDER BY ltv_cac_ratio DESC;