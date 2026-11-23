
from src.scrapers.product_scraper import AIProductScraper
from src.database.product_storage import AIProductStorage


class AIProductPipeline:

    def __init__(self):
        self.scraper = AIProductScraper()
        self.storage = AIProductStorage()

    def run(self, limit=20):

        print("\nAI Product Pipeline Started")
        print("=" * 40)

        products = self.scraper.fetch_products(limit=limit)

        if not products:
            print("No products collected.")
            return

        print(f"Product leads collected: {len(products)}")

        self.storage.save_products(products)

        print("\nAI Product Pipeline Completed!")
        print("=" * 40)


if __name__ == "__main__":

    pipeline = AIProductPipeline()
    pipeline.run(limit=20)
