
import requests
from datetime import datetime, timezone, timedelta


class AIJobsScraper:

    BASE_URL = "https://www.arbeitnow.com/api/job-board-api"

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

        if value is None or value == "":
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
        page = 1

        try:

            while len(jobs) < limit:

                response = requests.get(
                    self.BASE_URL,
                    params={"page": page},
                    headers={
                        "User-Agent": "AIIntelligenceHub/1.0"
                    },
                    timeout=30
                )

                response.raise_for_status()
                data = response.json()

                if not isinstance(data, dict):
                    break

                job_list = data.get("data", [])

                if not isinstance(job_list, list) or not job_list:
                    break

                for job in job_list:

                    if not isinstance(job, dict):
                        continue

                    title = str(job.get("title") or "").strip()
                    description = str(job.get("description") or "")
                    tags = job.get("tags") or []

                    if not isinstance(tags, list):
                        tags = []

                    searchable_text = (
                        f"{title} {description} {' '.join(map(str, tags))}"
                    ).lower()

                    is_ai_job = any(
                        keyword in searchable_text
                        for keyword in self.AI_KEYWORDS
                    )

                    if not is_ai_job:
                        continue

                    job_url = str(job.get("url") or "").strip()

                    if not title or not job_url:
                        continue

                    if job_url in seen_urls:
                        continue

                    published_date = self.normalize_date(
                        job.get("created_at")
                    )

                    # Keep only jobs published within the last 24 hours.
                    if not self.is_within_24_hours(published_date):
                        continue

                    seen_urls.add(job_url)

                    job_types = job.get("job_types") or []

                    if not isinstance(job_types, list):
                        job_types = [job_types]

                    jobs.append({

                        "company": job.get("company_name") or "",
                        "job_title": title,
                        "location": job.get("location") or "",
                        "is_remote": bool(job.get("remote", False)),
                        "job_url": job_url,
                        "job_type": ", ".join(map(str, job_types)),
                        "tags": ", ".join(map(str, tags)),
                        "published_date": published_date,
                        "source": "Arbeitnow",
                        "collected_at": datetime.now(
                            timezone.utc
                        ).isoformat()

                    })

                    if len(jobs) >= limit:
                        break

                if not data.get("links", {}).get("next"):
                    break

                page += 1

            return jobs[:limit]

        except requests.RequestException as error:
            print(f"Jobs API error: {error}")
            return []

        except (ValueError, TypeError, KeyError) as error:
            print(f"Jobs data processing error: {error}")
            return []


if __name__ == "__main__":

    scraper = AIJobsScraper()
    jobs = scraper.fetch_jobs(limit=10)

    print(f"\nAI Jobs Found (Last 24 Hours): {len(jobs)}\n")

    for job in jobs[:5]:
        print("-" * 50)
        print("Company:", job["company"])
        print("Role:", job["job_title"])
        print("Published:", job["published_date"])
