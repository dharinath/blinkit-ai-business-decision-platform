-- Clear all data from Supabase tables (run in Supabase SQL Editor)
-- Disable foreign key constraints temporarily
ALTER TABLE feedback DISABLE TRIGGER ALL;
ALTER TABLE order_items DISABLE TRIGGER ALL;
ALTER TABLE orders DISABLE TRIGGER ALL;
ALTER TABLE customers DISABLE TRIGGER ALL;
ALTER TABLE products DISABLE TRIGGER ALL;
ALTER TABLE marketing DISABLE TRIGGER ALL;

-- Delete all rows
DELETE FROM feedback;
DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM customers;
DELETE FROM products;
DELETE FROM marketing;

-- Re-enable constraints
ALTER TABLE feedback ENABLE TRIGGER ALL;
ALTER TABLE order_items ENABLE TRIGGER ALL;
ALTER TABLE orders ENABLE TRIGGER ALL;
ALTER TABLE customers ENABLE TRIGGER ALL;
ALTER TABLE products ENABLE TRIGGER ALL;
ALTER TABLE marketing ENABLE TRIGGER ALL;

-- Reset auto-increment counters if needed
-- (Not necessary for this schema since we're using TEXT primary keys)
