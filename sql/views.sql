-- Placeholder SQL for database views
-- ==========================================================
-- Blinkit AI Business Decision Platform
-- Analytics Views
-- ==========================================================

DROP VIEW IF EXISTS vw_business_summary CASCADE;
DROP VIEW IF EXISTS vw_feedback_analysis CASCADE;
DROP VIEW IF EXISTS vw_marketing_performance CASCADE;
DROP VIEW IF EXISTS vw_customer_summary CASCADE;
DROP VIEW IF EXISTS vw_delivery_performance CASCADE;
DROP VIEW IF EXISTS vw_product_performance CASCADE;
DROP VIEW IF EXISTS vw_sales_summary CASCADE;

-- ==========================================================
-- 1. Sales Summary
-- ==========================================================

CREATE OR REPLACE VIEW vw_sales_summary AS
SELECT
    DATE(order_date) AS order_date,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(order_total) AS total_sales,
    AVG(order_total) AS average_order_value
FROM orders
GROUP BY DATE(order_date);

-- ==========================================================
-- 2. Product Performance
-- ==========================================================

CREATE OR REPLACE VIEW vw_product_performance AS
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.brand,

    SUM(oi.quantity) AS quantity_sold,

    SUM(oi.quantity * oi.unit_price) AS revenue,

    AVG(oi.unit_price) AS average_price

FROM products p
JOIN order_items oi
ON p.product_id = oi.product_id

GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.brand;

-- ==========================================================
-- 3. Customer Summary
-- ==========================================================

CREATE OR REPLACE VIEW vw_customer_summary AS

SELECT

    c.customer_id,
    c.customer_name,
    c.customer_segment,
    c.area,

    COUNT(o.order_id) AS total_orders,

    SUM(o.order_total) AS lifetime_value,

    AVG(o.order_total) AS average_order_value

FROM customers c

LEFT JOIN orders o
ON c.customer_id = o.customer_id

GROUP BY
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    c.area;

-- ==========================================================
-- 4. Delivery Performance
-- ==========================================================

CREATE OR REPLACE VIEW vw_delivery_performance AS

SELECT

    order_id,
    customer_id,

    order_date,

    promised_delivery_time,

    actual_delivery_time,

    delivery_status,

    order_total,

    ROUND(
        EXTRACT(EPOCH FROM
            (actual_delivery_time - promised_delivery_time)
        ) / 60,
        2
    ) AS delivery_delay_minutes,

    CASE
        WHEN actual_delivery_time > promised_delivery_time
        THEN TRUE
        ELSE FALSE
    END AS is_late

FROM orders;

-- ==========================================================
-- 5. Marketing Performance
-- ==========================================================

CREATE OR REPLACE VIEW vw_marketing_performance AS

SELECT

    campaign_id,

    campaign_name,

    date,

    channel,

    target_audience,

    impressions,

    clicks,

    conversions,

    spend,

    revenue_generated,

    CASE
        WHEN spend = 0 THEN NULL
        ELSE ROUND(revenue_generated / spend,2)
    END AS calculated_roas

FROM marketing;

-- ==========================================================
-- 6. Feedback Analysis
-- ==========================================================

CREATE OR REPLACE VIEW vw_feedback_analysis AS

SELECT

    feedback_date,

    sentiment,

    feedback_category,

    COUNT(*) AS feedback_count,

    AVG(rating) AS average_rating

FROM feedback

GROUP BY

    feedback_date,

    sentiment,

    feedback_category;

-- ==========================================================
-- 7. Executive Business Summary
-- ==========================================================

CREATE OR REPLACE VIEW vw_business_summary AS

SELECT

    s.order_date,

    s.total_orders,

    s.unique_customers,

    s.total_sales,

    s.average_order_value,

    COALESCE(m.spend,0) AS marketing_spend,

    COALESCE(m.revenue_generated,0) AS marketing_revenue,

    COALESCE(m.calculated_roas,0) AS roas

FROM vw_sales_summary s

LEFT JOIN
(
    SELECT

        date,

        SUM(spend) AS spend,

        SUM(revenue_generated) AS revenue_generated,

        CASE
            WHEN SUM(spend)=0 THEN NULL
            ELSE ROUND(
                    SUM(revenue_generated) /
                    SUM(spend),2)
        END AS calculated_roas

    FROM marketing

    GROUP BY date

) m

ON s.order_date = m.date;

-- ==========================================================
-- Verify Views
-- ==========================================================

SELECT * FROM vw_sales_summary LIMIT 10;

SELECT * FROM vw_product_performance LIMIT 10;

SELECT * FROM vw_customer_summary LIMIT 10;

SELECT * FROM vw_delivery_performance LIMIT 10;

SELECT * FROM vw_marketing_performance LIMIT 10;

SELECT * FROM vw_feedback_analysis LIMIT 10;

SELECT * FROM vw_business_summary LIMIT 10;