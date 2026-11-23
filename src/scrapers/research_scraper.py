
import requests
import xml.etree.ElementTree as ET
import time
import random
from datetime import datetime


class ResearchPaperScraper:

    BASE_URL = "https://export.arxiv.org/api/query"

    NAMESPACE = {
        "atom": "http://www.w3.org/2005/Atom"
    }

    def __init__(self, max_retries=3, base_delay=15):
        self.max_retries = max_retries
        self.base_delay = base_delay

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "AIIntelligenceHub/1.0 (research data collection)"
        })

    def fetch_papers(
        self,
        search_query="artificial intelligence",
        max_results=10,
        start=0
    ):

        # Build query dynamically
        if ":" in search_query:
            query = search_query
        else:
            query = f'all:"{search_query}"'

        params = {
            "search_query": query,
            "start": start,
            "max_results": min(max_results, 100),
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }

        for attempt in range(self.max_retries):

            try:
                response = self.session.get(
                    self.BASE_URL,
                    params=params,
                    timeout=30
                )

                # Rate limit handling
                if response.status_code == 429:

                    retry_after = response.headers.get("Retry-After")

                    if retry_after and retry_after.isdigit():
                        delay = int(retry_after)
                    else:
                        delay = self.base_delay * (2 ** attempt)

                    delay += random.uniform(1, 3)

                    print(f"ArXiv rate limit reached (429).")
                    print(f"Retrying after {delay:.1f} seconds...")

                    if attempt < self.max_retries - 1:
                        time.sleep(delay)
                        continue

                    return []

                response.raise_for_status()

                root = ET.fromstring(response.content)

                papers = []
                seen_ids = set()

                for entry in root.findall(
                    "atom:entry", self.NAMESPACE
                ):

                    def get_text(tag):
                        element = entry.find(tag, self.NAMESPACE)

                        if element is not None and element.text:
                            return element.text.strip()

                        return ""

                    title = get_text("atom:title")
                    abstract = get_text("atom:summary")
                    paper_url = get_text("atom:id")
                    published = get_text("atom:published")
                    updated = get_text("atom:updated")

                    paper_id = paper_url.rstrip("/").split("/")[-1]

                    # Skip duplicate IDs
                    if not paper_id or paper_id in seen_ids:
                        continue

                    seen_ids.add(paper_id)

                    authors = []

                    for author in entry.findall(
                        "atom:author", self.NAMESPACE
                    ):
                        name = author.find(
                            "atom:name", self.NAMESPACE
                        )

                        if name is not None and name.text:
                            authors.append(name.text.strip())

                    categories = [
                        category.attrib.get("term", "")
                        for category in entry.findall(
                            "atom:category", self.NAMESPACE
                        )
                    ]

                    papers.append({
                        "paper_id": paper_id,
                        "title": " ".join(title.split()),
                        "authors": ", ".join(authors),
                        "abstract": " ".join(abstract.split()),
                        "paper_url": paper_url,
                        "published_date": published,
                        "updated_date": updated,
                        "categories": ", ".join(categories),
                        "source": "arXiv",
                        "collected_at": datetime.now().isoformat()
                    })

                print(f"Research papers collected: {len(papers)}")
                return papers

            except requests.exceptions.HTTPError as error:

                print(f"ArXiv HTTP Error: {error}")
                return []

            except requests.exceptions.RequestException as error:

                if attempt < self.max_retries - 1:

                    delay = self.base_delay * (2 ** attempt)
                    delay += random.uniform(1, 3)

                    print(f"Network error: {error}")
                    print(f"Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)

                else:
                    print(f"Research scraper failed: {error}")
                    return []

            except ET.ParseError as error:

                print(f"XML parsing error: {error}")
                return []

            except Exception as error:

                print(f"Unexpected research scraper error: {error}")
                return []

        return []


if __name__ == "__main__":

    scraper = ResearchPaperScraper()

    papers = scraper.fetch_papers(
        search_query="artificial intelligence",
        max_results=5
    )

    print(f"\nTotal Papers Found: {len(papers)}\n")

    for paper in papers:

        print("-" * 60)
        print("Title:", paper["title"])
        print("Authors:", paper["authors"])
        print("Published:", paper["published_date"])
        print("Paper ID:", paper["paper_id"])
        print("URL:", paper["paper_url"])
