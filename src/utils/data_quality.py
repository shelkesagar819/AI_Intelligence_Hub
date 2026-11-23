import pandas as pd
import os


class DataQualityChecker:

    def check_file(self, file_path):

        print("\n" + "=" * 50)
        print("         DATA QUALITY REPORT")
        print("=" * 50)

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        try:
            df = pd.read_csv(file_path)

            total_rows = len(df)
            total_columns = len(df.columns)
            duplicates = df.duplicated().sum()
            missing_values = df.isnull().sum().sum()

            print(f"File Name       : {os.path.basename(file_path)}")
            print(f"Total Rows      : {total_rows}")
            print(f"Total Columns   : {total_columns}")
            print(f"Duplicate Rows  : {duplicates}")
            print(f"Missing Values  : {missing_values}")

            print("\nMissing Values Per Column:")
            print(df.isnull().sum())

            print("\nDuplicate Records:")
            print(df[df.duplicated()].head(5))

            print("=" * 50)

        except Exception as error:
            print(f"Quality Check Failed: {error}")


if __name__ == "__main__":

    checker = DataQualityChecker()

    checker.check_file("data/raw/github_repositories.csv")
    checker.check_file("data/raw/ai_news.csv")
    checker.check_file("data/raw/ai_jobs.csv")
    checker.check_file("data/raw/ai_products.csv")