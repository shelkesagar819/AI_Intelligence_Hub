
import csv
import os


class AIProductStorage:

    def __init__(self):
        self.file_path = "data/raw/ai_products.csv"

        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True
        )

        self.fieldnames = [
            "product_name",
            "company",
            "website",
            "category",
            "description",
            "pricing_model",
            "source_url",
            "published_date",
            "source",
            "collected_at"
        ]

    def save_products(self, products):

        if not products:
            print("No products to save.")
            return

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
                    existing_urls.add(row.get("source_url", ""))

        new_products = [
            product for product in products
            if product.get("source_url")
            and product.get("source_url") not in existing_urls
        ]

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
                fieldnames=self.fieldnames
            )

            if not file_exists:
                writer.writeheader()

            writer.writerows(new_products)

        print(f"Products received: {len(products)}")
        print(f"New products saved: {len(new_products)}")
        print(f"Duplicates skipped: {len(products) - len(new_products)}")
