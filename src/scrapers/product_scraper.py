
import feedparser
from datetime import datetime, timezone


class AIProductScraper:

    FEED_URL = (
        "https://news.google.com/rss/search?"
        "q=AI+tools+OR+AI+products+OR+AI+software&hl=en-US&gl=US&ceid=US:en"
    )

    def fetch_products(self, limit=20):

        feed = feedparser.parse(self.FEED_URL)

        products = []
        seen_urls = set()

        for entry in feed.entries:

            url = entry.get("link", "")

            if not url or url in seen_urls:
                continue

            seen_urls.add(url)

            products.append({
                "product_name": entry.get("title", ""),
                "company": "Unknown",
                "website": url,
                "category": "AI Product",
                "description": entry.get("summary", ""),
                "pricing_model": "Unknown",
                "source_url": url,
                "published_date": entry.get("published", ""),
                "source": "Google News RSS",
                "collected_at": datetime.now(timezone.utc).isoformat()
            })

            if len(products) >= limit:
                break

        return products


if __name__ == "__main__":

    scraper = AIProductScraper()

    products = scraper.fetch_products(limit=10)

    print(f"\nProduct Discovery Leads: {len(products)}\n")

    for product in products[:5]:
        print("-" * 50)
        print("Title:", product["product_name"])
        print("Company:", product["company"])
        print("Category:", product["category"])
        print("Pricing:", product["pricing_model"])
        print("Source:", product["source_url"])
