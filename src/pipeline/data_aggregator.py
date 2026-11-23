
import pandas as pd

from src.database.data_access import DataAccessLayer


class DataAggregator:

    def __init__(self):
        self.data_access = DataAccessLayer()

    def get_all_data(self):

        datasets = [
            "github",
            "news",
            "jobs",
            "products"
        ]

        all_data = {}

        for dataset in datasets:

            df = self.data_access.get_data(dataset)

            all_data[dataset] = df

        return all_data

    def get_combined_summary(self):

        all_data = self.get_all_data()

        summary = []

        for dataset, df in all_data.items():

            summary.append({
                "dataset": dataset,
                "total_records": len(df)
            })

        return pd.DataFrame(summary)


if __name__ == "__main__":

    aggregator = DataAggregator()

    print("\nDATA AGGREGATION SUMMARY")
    print("=" * 40)

    summary = aggregator.get_combined_summary()

    print(summary.to_string(index=False))
