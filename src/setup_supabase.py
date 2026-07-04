#!/usr/bin/env python3
"""
Setup script to create tables in Supabase
Run this once to initialize the database schema
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def create_tables():
    """Create all required tables in Supabase"""
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # List of SQL commands to create tables
    sql_commands = [
        """
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
            avg_order_value NUMERIC
        )
        """,
        """
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
            max_stock_level INTEGER
        )
        """,
        """
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
            store_id TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS order_items (
            order_id TEXT,
            product_id TEXT,
            quantity INTEGER,
            unit_price NUMERIC,
            PRIMARY KEY (order_id, product_id)
        )
        """,
        """
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
            roas NUMERIC
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id TEXT PRIMARY KEY,
            order_id TEXT,
            customer_id TEXT,
            rating INTEGER,
            feedback_text TEXT,
            feedback_category TEXT,
            sentiment TEXT,
            feedback_date TEXT
        )
        """
    ]
    
    for idx, sql in enumerate(sql_commands, 1):
        try:
            result = client.rpc("sql_exec", {"sql": sql}).execute()
            print(f"✓ Created table {idx}/6")
        except Exception as exc:
            # Some endpoints may not support rpc, try alternative approach
            print(f"Note: Could not create table {idx} via RPC: {exc}")
            print("Please create tables manually in Supabase dashboard using the SQL commands in sql/create_tables.sql")
            break


if __name__ == "__main__":
    print("Initializing Supabase tables...")
    create_tables()
    print("✓ Setup complete!")
