import pandas as pd
import os


class DataCleaner:

    def clean_file(self, file_path, output_path=None):

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None

        try:
            df = pd.read_csv(file_path)

            original_rows = len(df)

            # Remove duplicate records
            df = df.drop_duplicates()

            # Clean text columns
            for column in df.select_dtypes(include="object").columns:
                df[column] = df[column].astype("string").str.strip()

                df[column] = df[column].replace(
                    ["", "nan", "None", "null"],
                    pd.NA
                )

            # Remove completely empty rows
            df = df.dropna(how="all")

            # Remove completely empty columns
            df = df.dropna(axis=1, how="all")

            cleaned_rows = len(df)

            if output_path is None:
                output_path = file_path.replace(
                    ".csv", "_cleaned.csv"
                )

            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

            df.to_csv(output_path, index=False)

            print("\n" + "=" * 45)
            print("       DATA CLEANING REPORT")
            print("=" * 45)

            print(f"Original Rows : {original_rows}")
            print(f"Cleaned Rows : {cleaned_rows}")
            print(f"Removed Rows : {original_rows - cleaned_rows}")
            print(f"Saved File   : {output_path}")

            print("=" * 45)

            return df

        except Exception as error:
            print(f"Data Cleaning Failed: {error}")
            return None


if __name__ == "__main__":

    cleaner = DataCleaner()

    cleaner.clean_file(
        "data/raw/github_repositories.csv",
        "data/processed/github_repositories_cleaned.csv"
    )

    cleaner.clean_file(
        "data/raw/ai_news.csv",
        "data/processed/ai_news_cleaned.csv"
    )

    cleaner.clean_file(
        "data/raw/ai_jobs.csv",
        "data/processed/ai_jobs_cleaned.csv"
    )

    cleaner.clean_file(
        "data/raw/ai_products.csv",
        "data/processed/ai_products_cleaned.csv"
    )