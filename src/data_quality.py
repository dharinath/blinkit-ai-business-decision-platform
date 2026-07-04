import pandas as pd
import os


class DataQualityReport:

    @staticmethod
    def generate(cleaned_data):

        report = []

        for dataset_name, df in cleaned_data.items():

            report.append({
                "Dataset": dataset_name,
                "Rows": len(df),
                "Columns": len(df.columns),
                "Duplicate Rows": df.duplicated().sum(),
                "Total Null Values": int(df.isnull().sum().sum()),
                "Memory Usage (KB)": round(df.memory_usage(deep=True).sum()/1024,2)
            })

        report_df = pd.DataFrame(report)

        os.makedirs("reports", exist_ok=True)

        report_path = "reports/data_quality_report.csv"

        report_df.to_csv(report_path,index=False)

        print("\n")
        print("="*80)
        print("DATA QUALITY REPORT")
        print("="*80)

        print(report_df)

        print(f"\nReport saved to : {report_path}")

        return report_df