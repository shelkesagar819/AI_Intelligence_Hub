
import requests
import json
import time
import logging

from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urlparse


class StartupScraper:

    def __init__(self):

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (compatible; "
                "AIIntelligenceHub/1.0; "
                "+https://example.com/bot)"
            )
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def extract_json_ld(self, soup):

        employee_count = "Unknown"
        organization_name = ""

        for script in soup.find_all(
            "script",
            type="application/ld+json"
        ):

            try:

                json_data = json.loads(
                    script.string or script.get_text()
                )

                if isinstance(json_data, list):
                    items = json_data

                elif isinstance(json_data, dict):
                    items = json_data.get(
                        "@graph", [json_data]
                    )

                else:
                    continue

                for item in items:

                    if not isinstance(item, dict):
                        continue

                    item_type = item.get("@type", "")

                    if isinstance(item_type, list):
                        item_type = " ".join(item_type)

                    if any(
                        word in item_type.lower()
                        for word in ["organization", "corporation"]
                    ):

                        organization_name = item.get(
                            "name", organization_name
                        )

                    employee_data = item.get(
                        "numberOfEmployees"
                    )

                    if isinstance(employee_data, dict):
                        employee_count = employee_data.get(
                            "value", "Unknown"
                        )

                    elif employee_data is not None:
                        employee_count = employee_data

            except (json.JSONDecodeError, TypeError):
                continue

        return organization_name, employee_count

    def scrape_website(self, url):

        try:

            response = self.session.get(
                url,
                timeout=20
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            title = (
                soup.title.get_text(" ", strip=True)
                if soup.title
                else ""
            )

            # Open Graph company/site name
            og_name = soup.find(
                "meta",
                property="og:site_name"
            )

            og_name = (
                og_name.get("content", "").strip()
                if og_name
                else ""
            )

            # Meta description
            meta_description = soup.find(
                "meta",
                attrs={"name": "description"}
            )

            description = (
                meta_description.get("content", "").strip()
                if meta_description
                else ""
            )

            # Meta keywords
            meta_keywords = soup.find(
                "meta",
                attrs={"name": "keywords"}
            )

            industry = (
                meta_keywords.get("content", "").strip()
                if meta_keywords
                else "Unknown"
            )

            organization_name, employee_count = (
                self.extract_json_ld(soup)
            )

            parsed_url = urlparse(url)

            startup_name = (
                organization_name
                or og_name
                or title
                or parsed_url.netloc
            )

            startup_data = {

                "startup_name": startup_name,

                "description": description,

                "website": url,

                "industry": industry,

                "employee_count": employee_count,

                "source": parsed_url.netloc,

                "source_url": url,

                "collected_at": datetime.now(
                    timezone.utc
                ).isoformat()

            }

            return startup_data

        except requests.RequestException as error:

            logging.error(
                "Startup scraping failed for %s: %s",
                url,
                error
            )

            return None

        except Exception as error:

            logging.exception(
                "Unexpected scraping error: %s",
                error
            )

            return None

    def scrape_multiple(self, urls, delay=1):

        startups = []
        seen_urls = set()

        for url in urls:

            if not isinstance(url, str) or not url.strip():
                continue

            normalized_url = (
                url.strip().rstrip("/").lower()
            )

            if normalized_url in seen_urls:
                continue

            seen_urls.add(normalized_url)

            logging.info("Scraping: %s", url)

            data = self.scrape_website(url)

            if data:
                startups.append(data)

            time.sleep(max(0, delay))

        logging.info(
            "Total startups collected: %s",
            len(startups)
        )

        return startups


if __name__ == "__main__":

    scraper = StartupScraper()

    print("Startup Scraper Ready")
