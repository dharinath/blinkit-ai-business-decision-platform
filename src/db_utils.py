import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase_client: Client | None = None


def get_client() -> Client:
    global supabase_client
    if supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise RuntimeError(
                "Supabase credentials are missing. Set SUPABASE_URL and SUPABASE_KEY in your environment."
            )
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase_client


def ensure_connection():
    try:
        client = get_client()
        client.auth.get_session()
    except Exception as exc:
        raise RuntimeError(f"Supabase connection failed: {exc}") from exc


def get_table_columns(table_name: str) -> set[str]:
    """
    Fetch valid column names for a table dynamically using the Postgres function get_table_columns.
    """
    client = get_client()
    try:
        response = client.rpc("get_table_columns", {"tablename": table_name}).execute()
        if response.data:
            return {row["column_name"] for row in response.data}
        else:
            print(f"No schema info returned for {table_name}")
            return set()
    except Exception as exc:
        print(f"Error fetching schema for {table_name}: {exc}")
        return set()


def save_dataframe(df, table_name):
    client = get_client()

    try:
        df_copy = df.copy()

        # 0. Drop computed/feature engineering columns (not part of schema)
        computed_cols = {"delivery_delay_minutes", "is_late"}
        df_copy = df_copy.drop(columns=[col for col in computed_cols if col in df_copy.columns])

        # 1. Convert datetime/timestamp columns to ISO 8601 strings
        for col in df_copy.columns:
            if pd.api.types.is_datetime64_any_dtype(df_copy[col]):
                df_copy[col] = df_copy[col].astype(str)

        # 2. Convert integer columns (remove decimals)
        int_cols = {
            "customer_id", "order_id", "product_id", "campaign_id",
            "feedback_id", "order_item_id", "store_id", "delivery_partner_id",
            "pincode", "total_orders", "quantity", "impressions", "clicks",
            "conversions", "margin_percentage", "shelf_life_days",
            "min_stock_level", "max_stock_level", "rating"
        }
        for col in df_copy.columns:
            if col in int_cols and col in df_copy.columns:
                # Convert to numeric first, then to int (removes decimals)
                df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")
                # Round to nearest integer and convert
                df_copy[col] = df_copy[col].round().astype("Int64")

        # 3. Drop columns not in DB schema (dynamic via RPC)
        valid_cols = get_table_columns(table_name)
        if valid_cols:
            dropped = [col for col in df_copy.columns if col not in valid_cols]
            if dropped:
                print(f"Dropping columns not in {table_name}: {dropped}")
            df_copy = df_copy[[col for col in df_copy.columns if col in valid_cols]]
        else:
            print(f"Warning: could not fetch schema for {table_name}, inserting all columns")

        # 4. Convert to records and insert
        records = df_copy.to_dict(orient="records")
        if records:  # avoid empty insert
            response = client.table(table_name).insert(records).execute()
            if getattr(response, "error", None):
                print(f"Error saving dataframe to Supabase: {response.error}")
                return False
        else:
            print(f"No valid records to insert for {table_name}.")
        return True

    except Exception as exc:
        print(f"Error saving dataframe to Supabase: {exc}")
        return False
