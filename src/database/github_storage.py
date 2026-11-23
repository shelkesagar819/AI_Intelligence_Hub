
import csv
import os


class GitHubRepositoryStorage:

    def __init__(self):

        self.file_path = "data/raw/github_repositories.csv"

        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True
        )

        self.fieldnames = [
            "repo_name",
            "repo_url",
            "description",
            "stars",
            "language",
            "owner",
            "last_updated",
            "source"
        ]

    def save_repositories(self, repositories):

        if not repositories:
            print("No repositories to save.")
            return 0

        existing_urls = set()

        if os.path.exists(self.file_path):

            with open(
                self.file_path,
                "r",
                encoding="utf-8",
                newline=""
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:
                    url = row.get("repo_url", "")

                    if url:
                        existing_urls.add(url.strip())

        new_repositories = []

        for repo in repositories:

            repo_url = (repo.get("repo_url") or "").strip()

            if not repo_url:
                continue

            if repo_url in existing_urls:
                continue

            existing_urls.add(repo_url)

            new_repositories.append(repo)

        file_exists = (
            os.path.exists(self.file_path)
            and os.path.getsize(self.file_path) > 0
        )

        with open(
            self.file_path,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.fieldnames,
                extrasaction="ignore"
            )

            if not file_exists:
                writer.writeheader()

            writer.writerows(new_repositories)

        print(f"Repositories received: {len(repositories)}")
        print(f"New repositories saved: {len(new_repositories)}")
        print(
            f"Duplicates skipped: "
            f"{len(repositories) - len(new_repositories)}"
        )

        return len(new_repositories)
