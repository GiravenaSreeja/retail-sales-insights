-- Retail sales analysis queries
-- Assumes a table called sales with the same columns as sample_sales.csv
-- (I ran these in MySQL while doing the EDA to double-check the pandas numbers)

-- 1. overall KPIs
SELECT
    COUNT(*) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 1) AS margin_pct
FROM sales;

-- 2. sales and margin by category
SELECT
    category,
    COUNT(*) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 1) AS margin_pct
FROM sales
GROUP BY category
ORDER BY total_sales DESC;

-- 3. profit by region - which region pulls its weight?
SELECT
    region,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY region
ORDER BY total_profit DESC;

-- 4. monthly trend
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    ROUND(SUM(sales), 2) AS monthly_sales,
    ROUND(SUM(profit), 2) AS monthly_profit
FROM sales
GROUP BY month
ORDER BY month;

-- 5. discount buckets - where the margin actually dies
SELECT
    CASE
        WHEN discount = 0 THEN '0%'
        WHEN discount <= 0.1 THEN '0-10%'
        WHEN discount <= 0.2 THEN '10-20%'
        ELSE '20%+'
    END AS discount_bucket,
    COUNT(*) AS orders,
    ROUND(AVG(profit / sales) * 100, 1) AS avg_margin_pct
FROM sales
GROUP BY discount_bucket
ORDER BY discount_bucket;

-- 6. top 10 products by profit
SELECT
    product_name,
    category,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY product_name, category
ORDER BY total_profit DESC
LIMIT 10;

-- 7. loss-making orders - worth a look before the next promo
SELECT order_id, order_date, region, category, product_name, sales, profit, discount
FROM sales
WHERE profit < 0
ORDER BY profit ASC
LIMIT 20;

-- 8. best customer segments
SELECT
    customer_segment,
    COUNT(*) AS orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS avg_order_value
FROM sales
GROUP BY customer_segment
ORDER BY total_sales DESC;
