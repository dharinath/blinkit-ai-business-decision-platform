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


def save_dataframe(df, table_name):
    client = get_client()

    try:
        # Convert datetime/timestamp columns to ISO 8601 strings for JSON serialization
        df_copy = df.copy()
        for col in df_copy.columns:
            if pd.api.types.is_datetime64_any_dtype(df_copy[col]):
                df_copy[col] = df_copy[col].astype(str)
        
        records = df_copy.to_dict(orient="records")
        response = client.table(table_name).insert(records).execute()
        if getattr(response, "error", None):
            print(f"Error saving dataframe to Supabase: {response.error}")
            return False
        return True
    except Exception as exc:
        print(f"Error saving dataframe to Supabase: {exc}")
        return False