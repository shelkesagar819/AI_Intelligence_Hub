
from src.scrapers.news_scraper import AINewsScraper
from src.database.news_storage import AINewsStorage
from src.utils.logger import log_info, log_error


class AINewsPipeline:

    def __init__(self):
        self.scraper = AINewsScraper()
        self.storage = AINewsStorage()

    def run(self, limit=20):

        log_info("AI News Pipeline Started")

        try:
            news_data = self.scraper.fetch_news(limit=limit)

            if not news_data:
                log_info("AI News Pipeline: No news found")
                return 0

            saved_count = self.storage.save_news(news_data)

            log_info(
                f"AI News Pipeline Completed | "
                f"Fetched: {len(news_data)} | "
                f"New Records Saved: {saved_count}"
            )

            return saved_count

        except Exception as e:
            log_error(f"AI News Pipeline Failed: {e}")
            raise


if __name__ == "__main__":
    pipeline = AINewsPipeline()
    pipeline.run()
