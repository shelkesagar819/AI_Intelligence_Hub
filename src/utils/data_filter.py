import pandas as pd
import os


class DataFilterEngine:

    def __init__(self):
        self.data_folder = "data/raw"

    def load_data(self, dataset_name):

        file_path = os.path.join(
            self.data_folder,
            dataset_name
        )

        if not os.path.exists(file_path):
            print(f"File not found: {dataset_name}")
            return pd.DataFrame()

        try:
            return pd.read_csv(file_path)

        except Exception as error:
            print(f"Error loading data: {error}")
            return pd.DataFrame()

    def filter_data(self, dataset_name, column, value):

        df = self.load_data(dataset_name)

        if df.empty:
            return df

        if column not in df.columns:
            print(f"Column not found: {column}")
            print("Available columns:", list(df.columns))
            return pd.DataFrame()

        filtered_df = df[
            df[column].astype(str).str.contains(
                str(value),
                case=False,
                na=False,
                regex=False
            )
        ]

        print("\nFILTER RESULTS")
        print("=" * 40)
        print(f"Dataset : {dataset_name}")
        print(f"Column  : {column}")
        print(f"Value   : {value}")
        print(f"Results : {len(filtered_df)}")
        print("=" * 40)

        return filtered_df


if __name__ == "__main__":

    engine = DataFilterEngine()

    result = engine.filter_data(
        "github_repositories.csv",
        "language",
        "Python"
    )

    if not result.empty:
        print(result.to_string(index=False))