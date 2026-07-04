import pandas as pd


class DataCleaner:

    @staticmethod
    def clean_dataframe(df, dataset_name):

        print(f"\n{'='*80}")
        print(f"Cleaning Dataset : {dataset_name}")
        print(f"{'='*80}")

        report = {}

        # -------------------------------------------------------
        # 1. Remove leading/trailing spaces from column names
        # -------------------------------------------------------
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        # -------------------------------------------------------
        # 2. Remove completely empty rows
        # -------------------------------------------------------
        empty_rows = df.isnull().all(axis=1).sum()
        df.dropna(how="all", inplace=True)
        report["Empty Rows Removed"] = empty_rows

        # -------------------------------------------------------
        # 3. Remove duplicate rows
        # -------------------------------------------------------
        duplicate_rows = df.duplicated().sum()
        df.drop_duplicates(inplace=True)
        report["Duplicate Rows Removed"] = duplicate_rows

        # -------------------------------------------------------
        # 4. Trim spaces from text columns
        # -------------------------------------------------------
        text_columns = df.select_dtypes(include=["object", "string"]).columns

        for col in text_columns:
            df[col] = df[col].astype("string").str.strip()

        # -------------------------------------------------------
        # 5. Convert Date columns
        # -------------------------------------------------------
        date_columns = [
            col for col in df.columns
            if col.endswith("date") or col.endswith("time") or col in {
                "date",
                "timestamp",
                "created_at",
                "updated_at"
            }
        ]

        for col in date_columns:

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

        # -------------------------------------------------------
        # 6. Convert Numeric Columns
        # -------------------------------------------------------
        numeric_columns = [
            "price",
            "amount",
            "order_total",
            "quantity",
            "spend",
            "rating",
            "impressions"
        ]

        for col in numeric_columns:

            if col in df.columns:

                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )

        # -------------------------------------------------------
        # 7. Check NULL values
        # -------------------------------------------------------
        report["Null Values"] = df.isnull().sum()

        # -------------------------------------------------------
        # 8. Validate Primary Keys
        # -------------------------------------------------------

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

            # Remove records with NULL PK
            df = df[df[pk].notna()]

            # Keep first occurrence of duplicate PK
            df = df.drop_duplicates(subset=[pk])

        # -------------------------------------------------------
        # 9. Standardize Sentiment
        # -------------------------------------------------------
        if "sentiment" in df.columns:

            df["sentiment"] = (
                df["sentiment"]
                .str.strip()
                .str.capitalize()
            )

            sentiment_map = {
                "Pos": "Positive",
                "Positive": "Positive",
                "Neg": "Negative",
                "Negative": "Negative",
                "Neutral": "Neutral"
            }

            df["sentiment"] = df["sentiment"].replace(sentiment_map)

        # -------------------------------------------------------
        # 10. Standardize Region / City
        # -------------------------------------------------------

        location_columns = [
            "region",
            "city",
            "state"
        ]

        for col in location_columns:

            if col in df.columns:

                df[col] = (
                    df[col]
                    .str.strip()
                    .str.title()
                )

        # -------------------------------------------------------
        # Summary
        # -------------------------------------------------------

        print(f"Rows                : {len(df)}")

        for key, value in report.items():

            if key != "Null Values":

                print(f"{key:<25}: {value}")

        print("\nNull Value Report")

        print(report["Null Values"])

        return df


def clean_all(datasets):

    cleaned = {}

    for name, df in datasets.items():

        cleaned[name] = DataCleaner.clean_dataframe(
            df,
            name
        )

    return cleaned