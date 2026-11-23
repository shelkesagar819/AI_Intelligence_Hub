
import asyncio
import aiohttp
import feedparser
import trafilatura

from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime


class AINewsScraper:

    FEEDS = {
        "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "Google News AI": "https://news.google.com/rss/search?q=artificial+intelligence&hl=en-IN&gl=IN&ceid=IN:en",
        "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
        "MIT Technology Review AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
        "The Verge AI": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"
    }

    HEADERS = {
        "User-Agent": "AIIntelligenceHub/1.0 (RSS Research Aggregator)"
    }

    def normalize_date(self, published):

        if not published:
            return ""

        try:
            date = parsedate_to_datetime(published)

        except Exception:
            try:
                date = datetime.fromisoformat(
                    published.replace("Z", "+00:00")
                )
            except Exception:
                return ""

        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)

        return date.astimezone(timezone.utc).isoformat()

    def is_within_24_hours(self, published_date):

        if not published_date:
            return False

        try:
            published = datetime.fromisoformat(published_date)

            if published.tzinfo is None:
                published = published.replace(tzinfo=timezone.utc)

            now = datetime.now(timezone.utc)

            return now - timedelta(hours=24) <= published <= now

        except Exception:
            return False

    async def fetch_article_text(self, session, url, semaphore):

        if not url:
            return ""

        try:
            async with semaphore:

                async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=20),
                    allow_redirects=True
                ) as response:

                    response.raise_for_status()

                    content_type = response.headers.get(
                        "Content-Type", ""
                    ).lower()

                    if "html" not in content_type:
                        return ""

                    html = await response.text(errors="replace")

                    text = trafilatura.extract(
                        html,
                        include_comments=False,
                        include_tables=False,
                        favor_precision=True
                    )

                    return text or ""

        except Exception as error:
            print(f"Article extraction failed ({url}): {error}")
            return ""

    async def fetch_feed(self, session, source_name, feed_url):

        try:
            async with session.get(
                feed_url,
                timeout=aiohttp.ClientTimeout(total=25)
            ) as response:

                response.raise_for_status()

                content = await response.read()
                feed = feedparser.parse(content)

                news_items = []

                for entry in feed.entries:

                    published = (
                        entry.get("published")
                        or entry.get("updated")
                        or ""
                    )

                    published_date = self.normalize_date(published)

                    # Keep only news published within the last 24 hours
                    if not self.is_within_24_hours(published_date):
                        continue

                    news_items.append({
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", ""),
                        "full_text": "",
                        "news_url": entry.get("link", ""),
                        "published_date": published_date,
                        "source": source_name,
                        "collected_at": datetime.now(
                            timezone.utc
                        ).isoformat()
                    })

                return news_items

        except Exception as error:
            print(f"Feed error ({source_name}): {error}")
            return []

    async def fetch_news_async(self, limit=20):

        connector = aiohttp.TCPConnector(limit=5)

        async with aiohttp.ClientSession(
            headers=self.HEADERS,
            connector=connector
        ) as session:

            feed_tasks = [
                self.fetch_feed(session, source, url)
                for source, url in self.FEEDS.items()
            ]

            results = await asyncio.gather(
                *feed_tasks,
                return_exceptions=True
            )

            news_items = []

            for result in results:
                if isinstance(result, list):
                    news_items.extend(result)

            unique_news = {}

            for item in news_items:

                url = item.get("news_url", "").strip()

                if url:
                    unique_news[url] = item

            final_news = list(unique_news.values())

            final_news.sort(
                key=lambda item: item["published_date"],
                reverse=True
            )

            final_news = final_news[:limit]

            semaphore = asyncio.Semaphore(5)

            article_tasks = [
                self.fetch_article_text(
                    session,
                    item["news_url"],
                    semaphore
                )
                for item in final_news
            ]

            article_results = await asyncio.gather(
                *article_tasks,
                return_exceptions=True
            )

            for item, article_text in zip(
                final_news,
                article_results
            ):

                if isinstance(article_text, str):
                    item["full_text"] = article_text

        return final_news

    def fetch_news(self, limit=20):

        return asyncio.run(
            self.fetch_news_async(limit=limit)
        )


if __name__ == "__main__":

    scraper = AINewsScraper()

    print("Async News Scraper Ready")
    print("Configured Sources:", len(scraper.FEEDS))
