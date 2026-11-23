
import os
import requests

from dotenv import load_dotenv


load_dotenv()


class GitHubRepositoryScraper:

    def __init__(self):

        self.base_url = "https://api.github.com/search/repositories"

        self.token = os.getenv("GITHUB_TOKEN")

        self.headers = {
            "Accept": "application/vnd.github+json"
        }

        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def search_repositories(self, query="generative AI", limit=10):

        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": min(limit, 100)
        }

        try:

            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=30
            )

            if response.status_code == 403:
                print("GitHub API rate limit reached.")
                print("Check your token or wait for the rate limit reset.")
                return []

            response.raise_for_status()

            data = response.json()

            repositories = []

            for repo in data.get("items", []):

                repositories.append({
                    "repo_name": repo.get("full_name"),
                    "repo_url": repo.get("html_url"),
                    "description": repo.get("description"),
                    "stars": repo.get("stargazers_count"),
                    "language": repo.get("language"),
                    "owner": repo.get("owner", {}).get("login"),
                    "last_updated": repo.get("updated_at"),
                    "source": "GitHub"
                })

            print(f"Repositories collected: {len(repositories)}")

            return repositories

        except requests.exceptions.RequestException as error:

            print(f"GitHub API Error: {error}")
            return []

        except Exception as error:

            print(f"Unexpected error: {error}")
            return []

    def search_paper_repository(self, paper_title, limit=5):

        if not paper_title:
            return []

        params = {
            "q": f'"{paper_title}"',
            "sort": "stars",
            "order": "desc",
            "per_page": min(limit, 100)
        }

        try:

            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=30
            )

            if response.status_code == 403:
                print("GitHub API rate limit reached.")
                return []

            response.raise_for_status()

            data = response.json()

            repositories = []

            for repo in data.get("items", []):

                repositories.append({
                    "repo_name": repo.get("full_name"),
                    "repo_url": repo.get("html_url"),
                    "description": repo.get("description"),
                    "stars": repo.get("stargazers_count"),
                    "language": repo.get("language"),
                    "owner": repo.get("owner", {}).get("login"),
                    "last_updated": repo.get("updated_at"),
                    "source": "GitHub"
                })

            print(
                f"Repositories found for paper: "
                f"{len(repositories)}"
            )

            return repositories

        except requests.exceptions.RequestException as error:

            print(f"Paper repository search error: {error}")
            return []

        except Exception as error:

            print(f"Unexpected error: {error}")
            return []


if __name__ == "__main__":

    scraper = GitHubRepositoryScraper()

    print("GitHub Repository Scraper Ready.")
