
from src.scrapers.remoteok_scraper import RemoteOKJobScraper
from src.database.jobs_storage import AIJobsStorage
from src.utils.logger import log_info, log_error


class RemoteOKPipeline:

    def __init__(self):
        self.scraper = RemoteOKJobScraper()
        self.storage = AIJobsStorage()

    def run(self, limit=20):

        log_info("RemoteOK Jobs Pipeline Started")

        try:
            jobs = self.scraper.fetch_jobs(limit=limit)

            if not jobs:
                log_info(
                    "RemoteOK Pipeline: No qualifying jobs "
                    "within the last 24 hours"
                )
                return 0

            saved_count = self.storage.save_jobs(jobs)

            log_info(
                f"RemoteOK Pipeline Completed | "
                f"Collected: {len(jobs)} | "
                f"New Records Saved: {saved_count}"
            )

            return saved_count

        except Exception as error:
            log_error(f"RemoteOK Pipeline Failed: {error}")
            raise


if __name__ == "__main__":
    pipeline = RemoteOKPipeline()
    pipeline.run(limit=20)
