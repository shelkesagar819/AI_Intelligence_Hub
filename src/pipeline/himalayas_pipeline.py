from src.scrapers.himalayas_scraper import HimalayasJobScraper
from src.database.jobs_storage import AIJobsStorage
from src.utils.logger import log_info, log_error


class HimalayasPipeline:

    def __init__(self):

        self.scraper = HimalayasJobScraper()
        self.storage = AIJobsStorage()

    def run(self, limit=20):

        log_info("Himalayas Jobs Pipeline Started")

        try:

            jobs = self.scraper.fetch_jobs(limit=limit)

            if not jobs:

                log_info(
                    "Himalayas Pipeline: "
                    "No qualifying AI jobs within the last 24 hours"
                )

                return 0

            saved_count = self.storage.save_jobs(jobs)

            log_info(
                f"Himalayas Pipeline Completed | "
                f"Collected: {len(jobs)} | "
                f"New Records Saved: {saved_count}"
            )

            return saved_count

        except Exception as error:

            log_error(
                f"Himalayas Pipeline Failed: {error}"
            )

            raise


if __name__ == "__main__":

    pipeline = HimalayasPipeline()
    pipeline.run(limit=20)