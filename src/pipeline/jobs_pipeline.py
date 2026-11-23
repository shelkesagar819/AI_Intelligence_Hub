
from src.scrapers.jobs_scraper import AIJobsScraper
from src.database.jobs_storage import AIJobsStorage
from src.utils.logger import log_info, log_error


class AIJobsPipeline:

    def __init__(self):
        self.scraper = AIJobsScraper()
        self.storage = AIJobsStorage()

    def run(self, limit=20):

        log_info("AI Jobs Pipeline Started")

        try:

            jobs = self.scraper.fetch_jobs(limit=limit)

            if not jobs:
                log_info("AI Jobs Pipeline: No jobs collected")
                return 0

            log_info(f"Jobs collected: {len(jobs)}")

            saved_count = self.storage.save_jobs(jobs)

            log_info(
                f"AI Jobs Pipeline Completed | "
                f"Collected: {len(jobs)} | "
                f"New Records Saved: {saved_count}"
            )

            return saved_count

        except Exception as error:

            log_error(f"AI Jobs Pipeline Failed: {error}")
            raise


if __name__ == "__main__":

    pipeline = AIJobsPipeline()
    pipeline.run(limit=20)
