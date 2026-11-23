import os
import pandas as pd


class DataAccessLayer:

    def __init__(self):
        self.data_folder = "data/raw"

        self.datasets = {
            "github": "github_repositories.csv",
            "news": "ai_news.csv",
            "jobs": "ai_jobs.csv",
            "products": "ai_products.csv",
        }

    def get_data(self, dataset_name):

        file_name = self.datasets.get(dataset_name.lower())

        if not file_name:
            print(f"Unknown dataset: {dataset_name}")
            return pd.DataFrame()

        file_path = os.path.join(
            self.data_folder,
            file_name
        )

        if not os.path.exists(file_path):
            print(f"Dataset not found: {file_path}")
            return pd.DataFrame()

        try:
            df = pd.read_csv(file_path)
            return df

        except Exception as error:
            print(f"Data loading error: {error}")
            return pd.DataFrame()

    def get_summary(self):

        summary = {}

        for name in self.datasets:

            df = self.get_data(name)

            summary[name] = {
                "total_records": len(df),
                "columns": list(df.columns)
            }

        return summary


if __name__ == "__main__":

    dal = DataAccessLayer()

    print("\nDATASET SUMMARY")
    print("=" * 40)

    summary = dal.get_summary()

    for dataset, details in summary.items():

        print(f"\nDataset: {dataset}")
        print(f"Records: {details['total_records']}")
        print(f"Columns: {details['columns']}")