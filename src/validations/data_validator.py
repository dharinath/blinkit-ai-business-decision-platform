import pandas as pd


class DataValidator:

    @staticmethod
    def validate_orders(orders_df):

        print("\nValidating Orders...")

        # Remove duplicate orders
        orders_df = orders_df.drop_duplicates(subset=["order_id"])

        # Remove completely empty rows
        orders_df = orders_df.dropna(how="all")

        # Trim text columns
        for col in orders_df.select_dtypes(include="object").columns:
            orders_df[col] = orders_df[col].str.strip()

        # Convert datetime columns
        datetime_columns = [
            "order_date",
            "promised_delivery_time",
            "actual_delivery_time"
        ]

        for col in datetime_columns:
            orders_df[col] = pd.to_datetime(
                orders_df[col],
                errors="coerce"
            )

        # Convert order total
        orders_df["order_total"] = pd.to_numeric(
            orders_df["order_total"],
            errors="coerce"
        )

        # Business Validation 1
        invalid_order_total = orders_df["order_total"] <= 0

        # Business Validation 2
        invalid_promised_time = (
            orders_df["promised_delivery_time"]
            < orders_df["order_date"]
        )

        # Business Validation 3
        invalid_actual_time = (
            orders_df["actual_delivery_time"]
            < orders_df["order_date"]
        )

        # Feature Engineering
        orders_df["delivery_delay_minutes"] = (
            orders_df["actual_delivery_time"]
            - orders_df["promised_delivery_time"]
        ).dt.total_seconds() / 60

        orders_df["is_late"] = (
            orders_df["delivery_delay_minutes"] > 0
        ).astype(int)

        print(f"Invalid Order Total : {invalid_order_total.sum()}")
        print(f"Invalid Promised Time : {invalid_promised_time.sum()}")
        print(f"Invalid Actual Time : {invalid_actual_time.sum()}")

        return orders_df

    @staticmethod
    def validate_marketing(marketing_df):

        print("\nValidating Marketing...")

        marketing_df = marketing_df.drop_duplicates(
            subset=["campaign_id"]
        )

        marketing_df = marketing_df.dropna(how="all")

        for col in marketing_df.select_dtypes(include="object").columns:
            marketing_df[col] = marketing_df[col].str.strip()

        marketing_df["date"] = pd.to_datetime(
            marketing_df["date"],
            errors="coerce"
        )

        numeric_columns = [
            "spend",
            "revenue_generated",
            "impressions",
            "clicks",
            "conversions",
            "roas"
        ]

        for col in numeric_columns:
            marketing_df[col] = pd.to_numeric(
                marketing_df[col],
                errors="coerce"
            )

        # Business Validation 1
        negative_spend = marketing_df["spend"] < 0

        # Business Validation 2
        invalid_clicks = (
            marketing_df["clicks"]
            > marketing_df["impressions"]
        )

        # Business Validation 3
        invalid_conversion = (
            marketing_df["conversions"]
            > marketing_df["clicks"]
        )

        print(f"Negative Spend : {negative_spend.sum()}")
        print(f"Clicks > Impressions : {invalid_clicks.sum()}")
        print(f"Conversions > Clicks : {invalid_conversion.sum()}")

        return marketing_df

    @staticmethod
    def validate_feedback(feedback_df):

        print("\nValidating Customer Feedback...")

        feedback_df = feedback_df.drop_duplicates(
            subset=["feedback_id"]
        )

        feedback_df = feedback_df.dropna(how="all")

        for col in feedback_df.select_dtypes(include="object").columns:
            feedback_df[col] = feedback_df[col].str.strip()

        feedback_df["feedback_date"] = pd.to_datetime(
            feedback_df["feedback_date"],
            errors="coerce"
        )

        feedback_df["rating"] = pd.to_numeric(
            feedback_df["rating"],
            errors="coerce"
        )

        # Business Validation 1
        invalid_rating = (
            (feedback_df["rating"] < 1)
            | (feedback_df["rating"] > 5)
        )

        # Business Validation 2
        feedback_df["sentiment"] = (
            feedback_df["sentiment"]
            .str.capitalize()
        )

        valid_sentiment = [
            "Positive",
            "Negative",
            "Neutral"
        ]

        invalid_sentiment = ~feedback_df["sentiment"].isin(
            valid_sentiment
        )

        print(f"Invalid Rating : {invalid_rating.sum()}")
        print(f"Invalid Sentiment : {invalid_sentiment.sum()}")

        return feedback_df

    @staticmethod
    def validate_products(products_df):

        print("\nValidating Products...")

        products_df = products_df.drop_duplicates(
            subset=["product_id"]
        )

        products_df = products_df.dropna(how="all")

        for col in products_df.select_dtypes(include="object").columns:
            products_df[col] = products_df[col].str.strip()

        numeric_columns = [
            "price",
            "mrp",
            "margin_percentage",
            "min_stock_level",
            "max_stock_level"
        ]

        for col in numeric_columns:
            products_df[col] = pd.to_numeric(
                products_df[col],
                errors="coerce"
            )

        invalid_price = products_df["price"] <= 0

        invalid_mrp = (
            products_df["mrp"]
            < products_df["price"]
        )

        invalid_margin = (
            (products_df["margin_percentage"] < 0)
            | (products_df["margin_percentage"] > 100)
        )

        print(f"Invalid Price : {invalid_price.sum()}")
        print(f"MRP < Price : {invalid_mrp.sum()}")
        print(f"Invalid Margin : {invalid_margin.sum()}")

        return products_df

    @staticmethod
    def validate_customers(customers_df):

        print("\nValidating Customers...")

        customers_df = customers_df.drop_duplicates(
            subset=["customer_id"]
        )

        customers_df = customers_df.dropna(how="all")

        for col in customers_df.select_dtypes(include="object").columns:
            customers_df[col] = customers_df[col].str.strip()

        if "registration_date" in customers_df.columns:
            customers_df["registration_date"] = pd.to_datetime(
                customers_df["registration_date"],
                errors="coerce"
            )

        numeric_columns = [
            "total_orders",
            "avg_order_value"
        ]

        for col in numeric_columns:
            if col in customers_df.columns:
                customers_df[col] = pd.to_numeric(
                    customers_df[col],
                    errors="coerce"
                )

        invalid_total_orders = pd.Series(False, index=customers_df.index)
        invalid_avg_order_value = pd.Series(False, index=customers_df.index)

        if "total_orders" in customers_df.columns:
            invalid_total_orders = customers_df["total_orders"] < 0

        if "avg_order_value" in customers_df.columns:
            invalid_avg_order_value = customers_df["avg_order_value"] < 0

        print(f"Invalid Total Orders : {invalid_total_orders.sum()}")
        print(f"Invalid Avg Order Value : {invalid_avg_order_value.sum()}")

        return customers_df

    @staticmethod
    def validate_order_items(order_items_df):

        print("\nValidating Order Items...")

        if {"order_id", "product_id"}.issubset(order_items_df.columns):
            order_items_df = order_items_df.drop_duplicates(
                subset=["order_id", "product_id"]
            )
        else:
            order_items_df = order_items_df.drop_duplicates()

        order_items_df = order_items_df.dropna(how="all")

        for col in order_items_df.select_dtypes(include="object").columns:
            order_items_df[col] = order_items_df[col].str.strip()

        if "quantity" in order_items_df.columns:
            order_items_df["quantity"] = pd.to_numeric(
                order_items_df["quantity"],
                errors="coerce"
            )

        if "unit_price" in order_items_df.columns:
            order_items_df["unit_price"] = pd.to_numeric(
                order_items_df["unit_price"],
                errors="coerce"
            )

        invalid_quantity = pd.Series(False, index=order_items_df.index)
        invalid_unit_price = pd.Series(False, index=order_items_df.index)

        if "quantity" in order_items_df.columns:
            invalid_quantity = order_items_df["quantity"] <= 0

        if "unit_price" in order_items_df.columns:
            invalid_unit_price = order_items_df["unit_price"] < 0

        print(f"Invalid Quantity : {invalid_quantity.sum()}")
        print(f"Invalid Unit Price : {invalid_unit_price.sum()}")

        return order_items_df