import pandas as pd
import os


class DataValidator:

    def validate_csv(self, file_path, required_columns=None):

        print("\n" + "=" * 50)
        print("          DATA VALIDATION REPORT")
        print("=" * 50)

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        try:
            df = pd.read_csv(file_path)

            # Check empty file
            if df.empty:
                print("ERROR: CSV file is empty.")
                return

            print(f"File: {file_path}")
            print(f"Total Records: {len(df)}")

            # Validate required columns
            if required_columns:

                missing_columns = [
                    col for col in required_columns
                    if col not in df.columns
                ]

                if missing_columns:
                    print("\nMissing Required Columns:")
                    for col in missing_columns:
                        print(f"- {col}")
                else:
                    print("\nAll required columns are present.")

            # Check duplicate records
            duplicates = df.duplicated().sum()
            print(f"Duplicate Records: {duplicates}")

            # Check URL columns
            url_columns = [
                col for col in df.columns
                if "url" in col.lower()
            ]

            for column in url_columns:

                invalid_urls = df[column].dropna().astype(str).apply(
                    lambda value: not value.startswith(("http://", "https://"))
                ).sum()

                print(f"Invalid URLs in {column}: {invalid_urls}")

            print("\nValidation completed.")
            print("=" * 50)

        except Exception as error:
            print(f"Validation Failed: {error}")


if __name__ == "__main__":

    validator = DataValidator()

    validator.validate_csv(
        "data/processed/github_repositories_cleaned.csv",
        required_columns=["repo_name", "repo_url", "stars"]
    )

    validator.validate_csv(
        "data/processed/ai_news_cleaned.csv",
        required_columns=["title", "news_url", "source"]
    )

    validator.validate_csv(
        "data/processed/ai_jobs_cleaned.csv",
        required_columns=["company", "job_title", "job_url"]
    )

    validator.validate_csv(
        "data/processed/ai_products_cleaned.csv",
        required_columns=["product_name", "source_url"]
    )