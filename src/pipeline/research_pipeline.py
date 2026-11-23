
import logging

from src.scrapers.research_scraper import ResearchPaperScraper
from src.scrapers.github_scraper import GitHubRepositoryScraper
from src.database.research_storage import ResearchPaperStorage


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


class ResearchPipeline:

    def __init__(self):

        self.scraper = ResearchPaperScraper()
        self.github_scraper = GitHubRepositoryScraper()
        self.storage = ResearchPaperStorage()

    def run(self, query="artificial intelligence", max_results=10, start=0):

        logging.info("Research Pipeline Started")

        try:

            papers = self.scraper.fetch_papers(
                search_query=query,
                max_results=max_results,
                start=start
            )

            if not papers:
                logging.warning(
                    "No papers collected. API may be rate-limited."
                )
                return 0

            logging.info("Papers received: %s", len(papers))

            # GitHub repository linking
            for paper in papers:

                paper["github_url"] = ""
                paper["github_stars"] = 0

                title = paper.get("title", "")

                if not title:
                    continue

                logging.info("Searching GitHub for: %s", title[:80])

                repositories = self.github_scraper.search_paper_repository(
                    paper_title=title,
                    limit=5
                )

                if repositories:

                    best_repo = repositories[0]

                    paper["github_url"] = best_repo.get("repo_url", "")
                    paper["github_stars"] = best_repo.get("stars", 0)

                    logging.info(
                        "GitHub repository matched: %s",
                        best_repo.get("repo_name")
                    )

                else:

                    logging.info(
                        "No GitHub repository found for paper."
                    )

            # Save collected papers
            saved_count = self.storage.save_papers(papers)

            logging.info(
                "New research papers stored: %s",
                saved_count
            )

            logging.info("Research Pipeline Completed Successfully")

            return saved_count

        except Exception as error:

            logging.exception(
                "Research Pipeline Failed: %s",
                error
            )

            return 0


if __name__ == "__main__":

    pipeline = ResearchPipeline()

    pipeline.run(
        query="artificial intelligence",
        max_results=5,
        start=0
    )
