
import requests
from datetime import datetime, timezone, timedelta


class JobicyJobScraper:

    BASE_URL = "https://jobicy.com/api/v2/remote-jobs"

    AI_KEYWORDS = [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "data scientist",
        "data science",
        "generative ai",
        "llm",
        "nlp",
        "computer vision",
        "ai engineer",
        "ai developer",
        "ml engineer",
        "python developer"
    ]

    def normalize_date(self, value):

        if not value:
            return ""

        try:
            date_value = datetime.fromisoformat(
                str(value).replace("Z", "+00:00")
            )

            if date_value.tzinfo is None:
                date_value = date_value.replace(
                    tzinfo=timezone.utc
                )

            return date_value.astimezone(
                timezone.utc
            ).isoformat()

        except (ValueError, TypeError):
            return ""

    def is_within_24_hours(self, published_date):

        if not published_date:
            return False

        try:
            published = datetime.fromisoformat(
                published_date.replace("Z", "+00:00")
            )

            if published.tzinfo is None:
                published = published.replace(
                    tzinfo=timezone.utc
                )

            now = datetime.now(timezone.utc)

            return (
                now - timedelta(hours=24)
                <= published <= now
            )

        except (ValueError, TypeError):
            return False

    def fetch_jobs(self, limit=20):

        headers = {
            "User-Agent": "AIIntelligenceHub/1.0"
        }

        params = {
            "count": min(limit, 50)
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()
        jobs_data = data.get("jobs", [])

        jobs = []
        seen_urls = set()

        for job in jobs_data:

            title = str(
                job.get("jobTitle") or ""
            ).strip()

            title_lower = title.lower()

            # Strict AI/ML title matching
            if not any(
                keyword in title_lower
                for keyword in self.AI_KEYWORDS
            ):
                continue

            job_url = str(
                job.get("url") or ""
            ).strip()

            if not job_url or job_url in seen_urls:
                continue

            published_date = self.normalize_date(
                job.get("pubDate")
            )

            if not self.is_within_24_hours(
                published_date
            ):
                continue

            tags = job.get("jobIndustry") or []

            if isinstance(tags, str):
                tags_text = tags
            else:
                tags_text = " ".join(
                    map(str, tags)
                )

            seen_urls.add(job_url)

            jobs.append({
                "company": job.get("companyName") or "",
                "job_title": title,
                "location": job.get("jobGeo") or "Remote",
                "is_remote": True,
                "job_url": job_url,
                "job_type": job.get("jobType") or "",
                "tags": tags_text,
                "published_date": published_date,
                "source": "Jobicy",
                "collected_at": datetime.now(
                    timezone.utc
                ).isoformat()
            })

            if len(jobs) >= limit:
                break

        return jobs
