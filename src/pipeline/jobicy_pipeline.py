
from src.scrapers.jobicy_scraper import JobicyJobScraper
from src.database.jobs_storage import AIJobsStorage
from src.utils.logger import log_info, log_error


class JobicyPipeline:

    def __init__(self):
        self.scraper = JobicyJobScraper()
        self.storage = AIJobsStorage()

    def run(self, limit=20):

        log_info("Jobicy Jobs Pipeline Started")

        try:
            jobs = self.scraper.fetch_jobs(limit=limit)

            if not jobs:
                log_info(
                    "Jobicy Pipeline: No qualifying AI jobs "
                    "within the last 24 hours"
                )
                return 0

            saved_count = self.storage.save_jobs(jobs)

            log_info(
                f"Jobicy Pipeline Completed | "
                f"Collected: {len(jobs)} | "
                f"New Records Saved: {saved_count}"
            )

            return saved_count

        except Exception as error:
            log_error(f"Jobicy Pipeline Failed: {error}")
            raise


if __name__ == "__main__":
    pipeline = JobicyPipeline()
    pipeline.run(limit=20)
