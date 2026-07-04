# Supabase Setup Instructions

## Step 1: Create Tables in Supabase

1. Go to your Supabase project dashboard: https://app.supabase.com/project/qtskmrkqfqxksigfkgqj/
2. Click on the **SQL Editor** (left sidebar)
3. Click **New query**
4. Copy and paste the entire contents of `sql/create_tables.sql`
5. Click **Run** to execute the SQL

This will create 6 tables:
- `customers` - Customer master data
- `products` - Product catalog
- `orders` - Order transactions
- `order_items` - Order line items
- `marketing` - Marketing campaign data
- `feedback` - Customer feedback and reviews

## Step 2: Run the ETL Pipeline

Once tables are created, run the application:

```bash
cd /home/codespace/blinkit-ai-business-decision-platform
source .venv/bin/activate
python src/main.py
```

The app will:
1. Load data from `data/raw/Blinkit - blinkit_customer_feedback.csv`
2. Clean and validate all datasets
3. Insert data into Supabase tables
4. Generate a data quality report in `reports/data_quality_report.csv`

## Step 3: Access Your Data

After the ETL completes successfully:

1. Go to Supabase: https://app.supabase.com/project/qtskmrkqfqxksigfkgqj/
2. Click **Table Editor** (left sidebar)
3. Select any table to view the loaded data

## Troubleshooting

**Issue**: "Could not find the table 'public.customers'"
- **Solution**: Make sure you've run the SQL in Step 1 to create the tables first

**Issue**: "Object of type Timestamp is not JSON serializable"
- **Solution**: Already fixed in the current code version (datetime columns are auto-converted to strings)

**Issue**: "Supabase connection failed"
- **Solution**: Verify `.env` file has correct credentials:
  ```
  SUPABASE_URL=https://qtskmrkqfqxksigfkgqj.supabase.co
  SUPABASE_KEY=sb_publishable_yo4gSBw7UI2IBJVqL494lA_zjkhwBCS
  ```

## Architecture

- **Data Source**: Excel file with 6 sheets
- **Processing**: Python ETL pipeline (data_loader → data_cleaner → validations → db_utils)
- **Database**: Supabase PostgreSQL (cloud-hosted)
- **UI Access**: Supabase dashboard provides browser-based table viewer
