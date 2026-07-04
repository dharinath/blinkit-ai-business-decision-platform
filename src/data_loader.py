# This Program is to load the data from the Excel file and return the data in the form of data frames.
import pandas as pd


File_path = "/home/codespace/blinkit-ai-business-decision-platform/data/raw/Blinkit.xlsx"

def load_data():
    """
    This function loads the data from the Excel file and returns it as a dict of pandas DataFrames.
    
    Returns:
        dict[str, pd.DataFrame]: The data loaded from the Excel file.
    """
    sheets = pd.read_excel(File_path, sheet_name=None)

    print("Loaded Excel sheets:", list(sheets.keys()))

    orders_df = sheets["blinkit_orders"]
    customers_df = sheets["blinkit_customers"]
    products_df = sheets["blinkit_products"]
    marketing_df = sheets["blinkit_marketing_performance"]
    feedback_df = sheets["blinkit_customer_feedback"]
    order_items_df = sheets["blinkit_order_items"]

    return {
        "orders": orders_df,
        "customers": customers_df,
        "products": products_df,
        "marketing": marketing_df,
        "feedback": feedback_df,
        "order_items": order_items_df
    }

if __name__ == "__main__":
    data = load_data()
    for key, df in data.items():
        print(f"{key} DataFrame:")
        print(df.head())
        print("\n")
