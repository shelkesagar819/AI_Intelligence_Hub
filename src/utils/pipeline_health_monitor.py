
import os
import pandas as pd


class PipelineHealthMonitor:

    def __init__(self):
        self.file_path = "data/processed/pipeline_history.csv"

    def load_history(self):

        if not os.path.exists(self.file_path):
            print("Pipeline history file not found.")
            return pd.DataFrame()

        try:
            df = pd.read_csv(self.file_path)

            if df.empty:
                print("Pipeline history is empty.")

            return df

        except Exception as error:
            print(f"Error loading pipeline history: {error}")
            return pd.DataFrame()

    def generate_health_report(self):

        df = self.load_history()

        if df.empty:
            return

        print("\nPIPELINE HEALTH REPORT")
        print("=" * 50)

        if "status" in df.columns:

            print("\nExecution Status:")
            print(df["status"].value_counts().to_string())

        if "pipeline_name" in df.columns and "status" in df.columns:

            print("\nPipeline-wise Health:")

            for name, group in df.groupby("pipeline_name"):

                total = len(group)
                successful = (
                    group["status"].astype(str).str.upper() == "SUCCESS"
                ).sum()

                failed = (
                    group["status"].astype(str).str.upper() == "FAILED"
                ).sum()

                success_rate = (
                    (successful / total) * 100
                    if total else 0
                )

                print(f"\nPipeline: {name}")
                print(f"Total Runs: {total}")
                print(f"Successful: {successful}")
                print(f"Failed: {failed}")
                print(f"Success Rate: {success_rate:.2f}%")

        if "execution_time" in df.columns:

            df["execution_time"] = pd.to_numeric(
                df["execution_time"],
                errors="coerce"
            )

            print("\nAverage Execution Time:")
            print(
                df.groupby("pipeline_name")["execution_time"]
                .mean()
                .round(2)
                .to_string()
            )


if __name__ == "__main__":

    monitor = PipelineHealthMonitor()

    monitor.generate_health_report()
