from data_loader import load_data
from data_cleaner import clean_all
from data_quality import DataQualityReport
from validations.data_validator import DataValidator
from db_utils import ensure_connection, save_dataframe


def main():
    ensure_connection()

    print("="*80)

    print("Blinkit AI Business Decision Platform - Layer 1: Data Extraction, Cleaning, and Quality Assessment")
    print("="*80)

    datasets = load_data()

    cleaned_data = clean_all(datasets)

# Validate each dataset
    datasets["customers"] = DataValidator.validate_customers(
        datasets["customers"]
    )
    save_dataframe(datasets["customers"], "customers")

    datasets["products"] = DataValidator.validate_products(
        datasets["products"]
    )
    save_dataframe(datasets["products"], "products")

    datasets["orders"] = DataValidator.validate_orders(
        datasets["orders"]
    )
    save_dataframe(datasets["orders"], "orders")

    datasets["order_items"] = DataValidator.validate_order_items(
        datasets["order_items"]
    )
    save_dataframe(datasets["order_items"], "order_items")

    datasets["marketing"] = DataValidator.validate_marketing(
        datasets["marketing"]
    )
    save_dataframe(datasets["marketing"], "marketing")

    datasets["feedback"] = DataValidator.validate_feedback(
        datasets["feedback"]
    )
    save_dataframe(datasets["feedback"], "feedback")

    print("\nAll business validations completed successfully.")

    DataQualityReport.generate(cleaned_data)

if __name__ == "__main__":
    main()