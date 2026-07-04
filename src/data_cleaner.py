import pandas as pd

class DataCleaner:

    @staticmethod
    def clean_dataframe(df, dataset_name, parent_keys=None):
        """
        Clean a single dataset and log all invalid rows (duplicates, PK issues, FK issues)
        into one error file per dataset. Also coerces schema types.
        - parent_keys: dict of {column_name: valid_keys_set} for FK validation
        """

        print(f"\n{'='*80}")
        print(f"Cleaning Dataset : {dataset_name}")
        print(f"{'='*80}")

        report = {}
        error_file = f"data_errors_{dataset_name}.csv"
        error_rows = pd.DataFrame()

        # 1. Standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        # 2. Remove completely empty rows
        empty_rows = df.isnull().all(axis=1).sum()
        df.dropna(how="all", inplace=True)
        report["Empty Rows Removed"] = empty_rows

        # 3. Handle duplicate rows
        duplicate_rows = df.duplicated().sum()
        if duplicate_rows > 0:
            error_rows = pd.concat([error_rows, df[df.duplicated(keep=False)]])
        df.drop_duplicates(inplace=True)
        report["Duplicate Rows Removed"] = duplicate_rows

        # 4. Trim spaces from text columns
        for col in df.select_dtypes(include=["object", "string"]).columns:
            df[col] = df[col].astype("string").str.strip()

        # 5. Convert date/time columns (basic)
        date_columns = [
            col for col in df.columns
            if col.endswith("date") or col.endswith("time") or col in {"date","timestamp","created_at","updated_at"}
        ]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

        # 6. Convert numeric columns (basic)
        numeric_columns = ["price","amount","order_total","quantity","spend","rating","impressions"]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # 7. Null values report
        report["Null Values"] = df.isnull().sum()

        # 8. Validate primary keys
        primary_keys = {
            "orders": "order_id",
            "customers": "customer_id",
            "products": "product_id",
            "marketing": "campaign_id",
            "feedback": "feedback_id",
            "order_items": "order_item_id"
        }
        pk = primary_keys.get(dataset_name)
        if pk and pk in df.columns:
            duplicate_pk = df[pk].duplicated().sum()
            null_pk = df[pk].isnull().sum()
            report["Duplicate Primary Keys"] = duplicate_pk
            report["Null Primary Keys"] = null_pk

            invalid_pk_rows = df[df[pk].isnull() | df[pk].duplicated(keep=False)]
            if not invalid_pk_rows.empty:
                error_rows = pd.concat([error_rows, invalid_pk_rows])

            df = df[df[pk].notna()]
            df = df.drop_duplicates(subset=[pk])

        # 9. Foreign key validation
        if parent_keys:
            for fk_col, valid_keys in parent_keys.items():
                if fk_col in df.columns:
                    invalid_fk_mask = ~df[fk_col].isin(valid_keys)
                    invalid_fk_rows = df[invalid_fk_mask]
                    if not invalid_fk_rows.empty:
                        error_rows = pd.concat([error_rows, invalid_fk_rows])
                        print(f"Invalid FK in {fk_col}: {len(invalid_fk_rows)} rows")
                        report[f"Invalid FK in {fk_col}"] = len(invalid_fk_rows)
                    df = df[~invalid_fk_mask]

        # 10. Standardize sentiment
        if "sentiment" in df.columns:
            df["sentiment"] = df["sentiment"].str.strip().str.capitalize()
            sentiment_map = {
                "Pos":"Positive","Positive":"Positive",
                "Neg":"Negative","Negative":"Negative",
                "Neutral":"Neutral"
            }
            df["sentiment"] = df["sentiment"].replace(sentiment_map)

        # 11. Standardize location fields
        for col in ["region","city","state"]:
            if col in df.columns:
                df[col] = df[col].str.strip().str.title()

        # 12. Schema coercion (full lists)
        INT_COLS = [
            "order_id","customer_id","delivery_partner_id","store_id","pincode",
            "total_orders","campaign_id","impressions","clicks","conversions",
            "product_id","quantity","margin_percentage","shelf_life_days",
            "min_stock_level","max_stock_level","order_item_id","feedback_id"
        ]
        DT_COLS = [
            "order_date","promised_delivery_time","actual_delivery_time",
            "registration_date","date","created_at","updated_at"
        ]
        FLOAT_COLS = [
            "order_total","avg_order_value","price","mrp","spend","revenue_generated","roas","amount","rating"
        ]

        df = coerce_to_schema(df, dataset_name, int_cols=INT_COLS, dt_cols=DT_COLS, float_cols=FLOAT_COLS)

        # Save all invalid rows into one file
        if not error_rows.empty:
            error_rows.to_csv(error_file, index=False)
            print(f"Invalid rows saved to {error_file}: {len(error_rows)}")

        # Summary
        print(f"Rows                : {len(df)}")
        for key, value in report.items():
            if key != "Null Values":
                print(f"{key:<25}: {value}")
        print("\nNull Value Report")
        print(report["Null Values"])

        return df


def coerce_to_schema(df, dataset_name, int_cols=None, dt_cols=None, float_cols=None):
    """
    Force columns into the desired format:
    - Integers → Int64 (nullable integer)
    - Floats   → float64
    - Datetime → datetime64[ns]
    Invalid values are coerced to NaN and logged.
    """
    error_file = f"data_errors_{dataset_name}_schema.csv"
    error_rows = pd.DataFrame()

    # Integers
    if int_cols:
        for col in int_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                df[col] = df[col].apply(lambda x: int(x) if pd.notna(x) and float(x).is_integer() else x)
                df[col] = df[col].astype("Int64")
                invalid_mask = df[col].isna()
                if invalid_mask.sum() > 0:
                    print(f"Invalid integer values in {dataset_name}.{col}: {df.loc[invalid_mask, col]}")
                    error_rows = pd.concat([error_rows, df[invalid_mask]])

    # Floats
    if float_cols:
        for col in float_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")
                invalid_mask = df[col].isna()
                if invalid_mask.sum() > 0:
                    print(f"Invalid float values in {dataset_name}.{col}: {df.loc[invalid_mask, col]}")
                    error_rows = pd.concat([error_rows, df[invalid_mask]])

    # Datetimes
    if dt_cols:
        for col in dt_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                invalid_mask = df[col].isna()
                if invalid_mask.sum() > 0:
                    print(f"Invalid datetime values in {dataset_name}.{col}: {df.loc[invalid_mask, col]}")
                    error_rows = pd.concat([error_rows, df[invalid_mask]])

    if not error_rows.empty:
        error_rows.to_csv(error_file, index=False)
        print(f"Invalid schema rows saved to {error_file}: {len(error_rows)}")

    return df


def clean_all(datasets):
    """
    Run cleaning across all datasets with PK/FK validation and schema coercion.
    Returns a dictionary of cleaned DataFrames.
    """
    cleaned = {}

    # Parent tables first
    cleaned["customers"] = DataCleaner.clean_dataframe(datasets["customers"], "customers")
    cleaned["products"]  = DataCleaner.clean_dataframe(datasets["products"], "products")
    cleaned["orders"]    = DataCleaner.clean_dataframe(datasets["orders"], "orders")

    # Child tables with FK validation
    cleaned["order_items"] = DataCleaner.clean_dataframe(
        datasets["order_items"], "order_items",
        parent_keys={
            "order_id": set(cleaned["orders"]["order_id"]),
            "product_id": set(cleaned["products"]["product_id"])
        }
    )

    cleaned["marketing"] = DataCleaner.clean_dataframe(datasets["marketing"], "marketing")

    cleaned["feedback"] = DataCleaner.clean_dataframe(
        datasets["feedback"], "feedback",
        parent_keys={
            "order_id": set(cleaned["orders"]["order_id"]),
            "customer_id": set(cleaned["customers"]["customer_id"])
        }
    )

    return cleaned
