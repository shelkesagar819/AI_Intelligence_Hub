import os

from src.utils.data_cleaner import DataCleaner
from src.utils.data_validator import DataValidator
from src.utils.logger import log_info, log_error


class DataProcessingPipeline:

    def __init__(self):
        self.cleaner = DataCleaner()
        self.validator = DataValidator()

        self.input_folder = "data/raw"
        self.output_folder = "data/processed"

        os.makedirs(self.output_folder, exist_ok=True)

    def process_file(self, file_name, required_columns=None):

        input_path = os.path.join(
            self.input_folder,
            file_name
        )

        output_path = os.path.join(
            self.output_folder,
            file_name.replace(".csv", "_cleaned.csv")
        )

        log_info(f"Processing started: {file_name}")

        try:
            cleaned_data = self.cleaner.clean_file(
                input_path,
                output_path
            )

            if cleaned_data is None:
                log_error(f"Cleaning failed: {file_name}")
                return

            self.validator.validate_csv(
                output_path,
                required_columns=required_columns
            )

            log_info(f"Processing completed: {file_name}")

        except Exception as error:
            log_error(f"Processing error: {file_name} | {error}")

    def run(self):

        print("\nAI INTELLIGENCE HUB - DATA PROCESSING")
        print("=" * 50)

        files = {
            "github_repositories.csv": [
                "repo_name", "repo_url", "stars"
            ],
            "ai_news.csv": [
                "title", "news_url", "source"
            ],
            "ai_jobs.csv": [
                "company", "job_title", "job_url"
            ],
            "ai_products.csv": [
                "product_name", "source_url"
            ]
        }

        for file_name, required_columns in files.items():

            self.process_file(
                file_name,
                required_columns=required_columns
            )

        print("\nDATA PROCESSING COMPLETED")
        print("=" * 50)


if __name__ == "__main__":

    pipeline = DataProcessingPipeline()
    pipeline.run()