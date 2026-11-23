
import csv
import os
import logging

from src.scrapers.startup_scraper import StartupScraper
from src.database.csv_storage import CSVStorage
from src.entity_resolution.deduplicator import StartupDeduplicator


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


class StartupPipeline:

    def __init__(self):

        self.scraper = StartupScraper()
        self.storage = CSVStorage()
        self.deduplicator = StartupDeduplicator()

        self.file_path = "data/raw/startups.csv"

    def get_existing_data(self):

        if not os.path.exists(self.file_path):
            return []

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8-sig",
                newline=""
            ) as file:

                return list(csv.DictReader(file))

        except Exception as error:

            logging.error(
                "Error reading startup CSV: %s",
                error
            )

            return []

    def run(self, website_urls):

        logging.info("Startup Pipeline Started")

        if isinstance(website_urls, str):
            website_urls = [website_urls]

        if not website_urls:
            logging.warning("No startup URLs provided.")
            return 0

        existing_data = self.get_existing_data()

        saved_count = 0
        duplicate_count = 0
        failed_count = 0

        for website_url in website_urls:

            try:

                logging.info(
                    "Processing startup URL: %s",
                    website_url
                )

                startup = self.scraper.scrape_website(
                    website_url
                )

                if not startup:

                    failed_count += 1

                    logging.warning(
                        "Scraping failed: %s",
                        website_url
                    )

                    continue

                if self.deduplicator.is_duplicate(
                    startup,
                    existing_data
                ):

                    duplicate_count += 1

                    logging.info(
                        "Duplicate skipped: %s",
                        startup.get("startup_name")
                    )

                    continue

                save_result = self.storage.save_startup(
                    startup
                )

                if save_result:

                    existing_data.append(startup)
                    saved_count += 1

                    logging.info(
                        "Startup saved: %s",
                        startup.get("startup_name")
                    )

                else:

                    failed_count += 1

                    logging.error(
                        "Startup save failed: %s",
                        startup.get("startup_name")
                    )

            except Exception as error:

                failed_count += 1

                logging.exception(
                    "Startup processing failed for %s: %s",
                    website_url,
                    error
                )

        logging.info("------------------------------")
        logging.info("Total URLs: %s", len(website_urls))
        logging.info("New startups saved: %s", saved_count)
        logging.info("Duplicates skipped: %s", duplicate_count)
        logging.info("Failed records: %s", failed_count)
        logging.info("Startup Pipeline Completed")
        logging.info("------------------------------")

        return saved_count


if __name__ == "__main__":

    pipeline = StartupPipeline()

    startup_urls = [
        "https://openai.com",
        "https://www.anthropic.com",
        "https://deepmind.google"
    ]

    pipeline.run(startup_urls)
