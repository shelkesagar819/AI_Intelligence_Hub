
import pandas as pd

from src.database.data_access import DataAccessLayer


class DataInsightsAnalyzer:

    def __init__(self):
        self.data_access = DataAccessLayer()

    def analyze_github(self):

        df = self.data_access.get_data("github")

        if df.empty:
            return {"message": "No GitHub data available"}

        insights = {}

        if "language" in df.columns:
            insights["top_languages"] = (
                df["language"]
                .value_counts()
                .head(10)
                .to_dict()
            )

        if "stars" in df.columns:
            df["stars"] = pd.to_numeric(
                df["stars"],
                errors="coerce"
            )

            insights["total_stars"] = int(
                df["stars"].fillna(0).sum()
            )

            insights["average_stars"] = round(
                df["stars"].fillna(0).mean(), 2
            )

        return insights

    def analyze_jobs(self):

        df = self.data_access.get_data("jobs")

        if df.empty:
            return {"message": "No jobs data available"}

        insights = {}

        if "job_title" in df.columns:
            insights["top_job_titles"] = (
                df["job_title"]
                .value_counts()
                .head(10)
                .to_dict()
            )

        if "is_remote" in df.columns:
            insights["remote_jobs"] = (
                df["is_remote"]
                .astype(str)
                .str.lower()
                .isin(["true", "1", "yes"])
                .sum()
            )

        return insights

    def analyze_news(self):

        df = self.data_access.get_data("news")

        if df.empty:
            return {"message": "No AI news available"}

        insights = {}

        if "source" in df.columns:
            insights["news_sources"] = (
                df["source"]
                .value_counts()
                .head(10)
                .to_dict()
            )

        return insights

    def analyze_products(self):

        df = self.data_access.get_data("products")

        if df.empty:
            return {"message": "No AI products available"}

        insights = {}

        if "pricing_model" in df.columns:
            insights["pricing_models"] = (
                df["pricing_model"]
                .value_counts()
                .to_dict()
            )

        if "category" in df.columns:
            insights["product_categories"] = (
                df["category"]
                .value_counts()
                .head(10)
                .to_dict()
            )

        return insights

    def run_analysis(self):

        return {
            "github": self.analyze_github(),
            "jobs": self.analyze_jobs(),
            "news": self.analyze_news(),
            "products": self.analyze_products()
        }


if __name__ == "__main__":

    analyzer = DataInsightsAnalyzer()

    results = analyzer.run_analysis()

    print("\nAI INTELLIGENCE ANALYSIS")
    print("=" * 50)

    for dataset, insights in results.items():

        print(f"\n{dataset.upper()} INSIGHTS")

        for key, value in insights.items():
            print(f"{key}: {value}")
