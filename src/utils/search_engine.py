import os
import pandas as pd


class AIIntelligenceSearch:

    def __init__(self):

        self.data_folder = "data/raw"

        self.datasets = {
            "github": "github_repositories.csv",
            "news": "ai_news.csv",
            "jobs": "ai_jobs.csv",
            "products": "ai_products.csv",
        }

    def search(self, keyword):

        keyword = keyword.strip().lower()

        if not keyword:
            print("Please enter a search keyword.")
            return

        results = []

        for category, file_name in self.datasets.items():

            file_path = os.path.join(
                self.data_folder,
                file_name
            )

            if not os.path.exists(file_path):
                continue

            try:
                df = pd.read_csv(file_path)

                text_columns = df.select_dtypes(
                    include=["object", "string"]
                ).columns

                mask = pd.Series(False, index=df.index)

                for column in text_columns:

                    mask |= df[column].astype("string").str.lower().str.contains(
                        keyword,
                        na=False,
                        regex=False
                    )

                matched = df[mask].copy()

                if not matched.empty:
                    matched.insert(0, "category", category)
                    results.append(matched)

            except Exception as error:
                print(f"Error searching {file_name}: {error}")

        if results:

            final_results = pd.concat(
                results,
                ignore_index=True
            )

            print(f"\nSearch Results for: {keyword}")
            print(f"Total Results: {len(final_results)}\n")

            print(final_results.to_string(index=False))

            return final_results

        else:

            print(f"No results found for: {keyword}")
            return pd.DataFrame()


if __name__ == "__main__":

    search_engine = AIIntelligenceSearch()

    keyword = input("Enter AI search keyword: ")

    search_engine.search(keyword)