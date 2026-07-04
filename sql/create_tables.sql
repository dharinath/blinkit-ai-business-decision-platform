-- Create tables for Blinkit AI Business Decision Platform
-- Run this in Supabase SQL Editor: https://app.supabase.com/project/qtskmrkqfqxksigfkgqj/sql

CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    area TEXT,
    pincode TEXT,
    registration_date TEXT,
    customer_segment TEXT,
    total_orders INTEGER,
    avg_order_value NUMERIC,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    brand TEXT,
    price NUMERIC,
    mrp NUMERIC,
    margin_percentage NUMERIC,
    shelf_life_days INTEGER,
    min_stock_level INTEGER,
    max_stock_level INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    order_date TEXT,
    promised_delivery_time TEXT,
    actual_delivery_time TEXT,
    delivery_status TEXT,
    order_total NUMERIC,
    payment_method TEXT,
    delivery_partner_id TEXT,
    store_id TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id TEXT,
    product_id TEXT,
    quantity INTEGER,
    unit_price NUMERIC,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE IF NOT EXISTS marketing (
    campaign_id TEXT PRIMARY KEY,
    campaign_name TEXT,
    date TEXT,
    target_audience TEXT,
    channel TEXT,
    impressions INTEGER,
    clicks INTEGER,
    conversions INTEGER,
    spend NUMERIC,
    revenue_generated NUMERIC,
    roas NUMERIC,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS feedback (
    feedback_id TEXT PRIMARY KEY,
    order_id TEXT,
    customer_id TEXT,
    rating INTEGER,
    feedback_text TEXT,
    feedback_category TEXT,
    sentiment TEXT,
    feedback_date TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

