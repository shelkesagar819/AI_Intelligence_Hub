from src.scrapers.github_scraper import GitHubRepositoryScraper
from src.database.github_storage import GitHubRepositoryStorage
from src.utils.logger import log_info, log_error


class GitHubPipeline:

    def __init__(self):
        self.scraper = GitHubRepositoryScraper()
        self.storage = GitHubRepositoryStorage()

    def run(self, query="generative AI", limit=10):

        log_info("GitHub Pipeline Started")

        try:
            repositories = self.scraper.search_repositories(
                query=query,
                limit=limit
            )

            if repositories:
                self.storage.save_repositories(repositories)
                log_info(
                    f"GitHub Pipeline Success: {len(repositories)} repositories collected"
                )
            else:
                log_info("GitHub Pipeline: No repositories found")

        except Exception as e:
            log_error(f"GitHub Pipeline Failed: {e}")
            raise


if __name__ == "__main__":
    pipeline = GitHubPipeline()
    pipeline.run()