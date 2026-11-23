
import requests
from datetime import datetime, timezone, timedelta


class RemoteOKJobScraper:

    BASE_URL = "https://remoteok.com/api"

    AI_KEYWORDS = [
        "ai",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "data scientist",
        "data science",
        "llm",
        "generative ai",
        "nlp",
        "python developer"
    ]

    def normalize_date(self, value):

        if not value:
            return ""

        try:
            if isinstance(value, (int, float)):
                date = datetime.fromtimestamp(
                    value,
                    tz=timezone.utc
                )
            else:
                text = str(value).strip()

                try:
                    date = datetime.fromtimestamp(
                        float(text),
                        tz=timezone.utc
                    )
                except ValueError:
                    date = datetime.fromisoformat(
                        text.replace("Z", "+00:00")
                    )

                    if date.tzinfo is None:
                        date = date.replace(tzinfo=timezone.utc)

            return date.astimezone(timezone.utc).isoformat()

        except (ValueError, TypeError, OverflowError, OSError):
            return ""

    def is_within_24_hours(self, published_date):

        if not published_date:
            return False

        try:
            date = datetime.fromisoformat(
                published_date.replace("Z", "+00:00")
            )

            if date.tzinfo is None:
                date = date.replace(tzinfo=timezone.utc)

            now = datetime.now(timezone.utc)

            return (
                now - timedelta(hours=24)
                <= date
                <= now
            )

        except (ValueError, TypeError, AttributeError):
            return False

    def fetch_jobs(self, limit=20):

        jobs = []
        seen_urls = set()

        try:

            response = requests.get(
                self.BASE_URL,
                headers={
                    "User-Agent": "AIIntelligenceHub/1.0"
                },
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            if not isinstance(data, list):
                return jobs

            for job in data:

                if not isinstance(job, dict):
                    continue

                title = str(job.get("position") or "").strip()
                description = str(job.get("description") or "")
                tags = job.get("tags") or []

                if not isinstance(tags, list):
                    tags = []

                searchable_text = (
                    f"{title} {description} {' '.join(map(str, tags))}"
                ).lower()

                if not any(
                    keyword in searchable_text
                    for keyword in self.AI_KEYWORDS
                ):
                    continue

                job_url = (
                    str(job.get("apply_url") or "").strip()
                    or str(job.get("url") or "").strip()
                )

                if not title or not job_url:
                    continue

                if job_url in seen_urls:
                    continue

                published_date = self.normalize_date(
                    job.get("epoch") or job.get("date")
                )

                if not self.is_within_24_hours(published_date):
                    continue

                seen_urls.add(job_url)

                jobs.append({

                    "company": job.get("company") or "",
                    "job_title": title,
                    "location": job.get("location") or "Remote",
                    "is_remote": True,
                    "job_url": job_url,
                    "job_type": "",
                    "tags": ", ".join(map(str, tags)),
                    "published_date": published_date,
                    "source": "RemoteOK",
                    "collected_at": datetime.now(
                        timezone.utc
                    ).isoformat()

                })

                if len(jobs) >= limit:
                    break

            return jobs

        except requests.RequestException as error:
            print(f"RemoteOK API Error: {error}")
            return []

        except (ValueError, TypeError, KeyError) as error:
            print(f"RemoteOK Data Error: {error}")
            return []


if __name__ == "__main__":

    scraper = RemoteOKJobScraper()
    jobs = scraper.fetch_jobs(limit=20)

    print("RemoteOK AI Jobs (Last 24 Hours):", len(jobs))

    for job in jobs[:5]:
        print(
            job["company"],
            "|",
            job["job_title"],
            "|",
            job["published_date"]
        )
