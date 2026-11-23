
import csv
import os
import tempfile


class AINewsStorage:

    def __init__(self):

        self.file_path = "data/raw/ai_news.csv"

        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True
        )

        self.fieldnames = [
            "title",
            "summary",
            "full_text",
            "news_url",
            "published_date",
            "source",
            "collected_at"
        ]

        self.migrate_schema()

    def migrate_schema(self):

        if not os.path.exists(self.file_path):
            return

        if os.path.getsize(self.file_path) == 0:
            return

        with open(
            self.file_path,
            "r",
            encoding="utf-8",
            newline=""
        ) as file:

            reader = csv.DictReader(file)
            old_fields = reader.fieldnames or []

            if old_fields == self.fieldnames:
                return

            rows = list(reader)

        directory = os.path.dirname(self.file_path)

        fd, temp_path = tempfile.mkstemp(
            dir=directory,
            suffix=".tmp"
        )

        try:

            with os.fdopen(
                fd,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=self.fieldnames,
                    extrasaction="ignore"
                )

                writer.writeheader()

                for row in rows:

                    row.setdefault("full_text", "")

                    writer.writerow(row)

            os.replace(temp_path, self.file_path)

            print("News CSV schema migration completed.")

        except Exception:

            if os.path.exists(temp_path):
                os.remove(temp_path)

            raise

    def save_news(self, news_items):

        if not news_items:
            print("No news to save.")
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

                    url = (row.get("news_url") or "").strip()

                    if url:
                        existing_urls.add(url)

        new_news = []

        for item in news_items:

            news_url = (item.get("news_url") or "").strip()

            if not news_url or news_url in existing_urls:
                continue

            existing_urls.add(news_url)
            new_news.append(item)

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

            writer.writerows(new_news)

        print(f"News received: {len(news_items)}")
        print(f"New news saved: {len(new_news)}")
        print(
            f"Duplicates skipped: "
            f"{len(news_items) - len(new_news)}"
        )

        return len(new_news)


if __name__ == "__main__":

    storage = AINewsStorage()

    print("News Storage Ready")
    print("Columns:", storage.fieldnames)
