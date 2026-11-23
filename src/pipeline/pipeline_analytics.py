import os
import pandas as pd


class PipelineAnalytics:

    def __init__(self):
        self.file_path = "data/processed/pipeline_history.csv"

    def generate_report(self):

        if not os.path.exists(self.file_path):
            print("Pipeline history file not found!")
            return

        df = pd.read_csv(self.file_path)

        if df.empty:
            print("No pipeline execution data available.")
            return

        total_runs = len(df)

        successful_runs = len(
            df[df["status"] == "SUCCESS"]
        )

        failed_runs = len(
            df[df["status"] == "FAILED"]
        )

        success_rate = round(
            (successful_runs / total_runs) * 100, 2
        )

        average_time = round(
            df["execution_time"].mean(), 2
        )

        print("\n" + "=" * 45)
        print("     PIPELINE ANALYTICS REPORT")
        print("=" * 45)

        print(f"Total Runs        : {total_runs}")
        print(f"Successful Runs   : {successful_runs}")
        print(f"Failed Runs      : {failed_runs}")
        print(f"Success Rate     : {success_rate}%")
        print(f"Average Time     : {average_time} seconds")

        print("=" * 45)


if __name__ == "__main__":
    analytics = PipelineAnalytics()
    analytics.generate_report()