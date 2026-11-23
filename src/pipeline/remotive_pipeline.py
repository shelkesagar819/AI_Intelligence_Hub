
from src.scrapers.remotive_scraper import RemotiveJobScraper
from src.database.jobs_storage import AIJobsStorage
from src.utils.logger import log_info, log_error


class RemotivePipeline:

    def __init__(self):

        self.scraper = RemotiveJobScraper()
        self.storage = AIJobsStorage()

    def run(self, limit=20):

        log_info("Remotive Jobs Pipeline Started")

        try:

            jobs = self.scraper.fetch_jobs(limit=limit)

            if not jobs:
                log_info(
                    "Remotive Pipeline: No qualifying jobs found "
                    "within the last 24 hours"
                )
                return 0

            log_info(f"Remotive Jobs Collected: {len(jobs)}")

            saved_count = self.storage.save_jobs(jobs)

            log_info(
                f"Remotive Pipeline Completed | "
                f"Collected: {len(jobs)} | "
                f"New Records Saved: {saved_count}"
            )

            return saved_count

        except Exception as error:

            log_error(f"Remotive Pipeline Failed: {error}")
            raise


if __name__ == "__main__":

    pipeline = RemotivePipeline()
    pipeline.run(limit=20)
