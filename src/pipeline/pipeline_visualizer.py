import pandas as pd
import plotly.express as px
import os


class PipelineVisualizer:

    def __init__(self):
        self.file_path = "data/processed/pipeline_history.csv"

    def show_execution_chart(self):

        if not os.path.exists(self.file_path):
            print("Pipeline history not found!")
            return

        df = pd.read_csv(self.file_path)

        if df.empty:
            print("No pipeline data available!")
            return

        df["execution_time"] = pd.to_numeric(
            df["execution_time"], errors="coerce"
        )

        df = df.dropna(subset=["execution_time"])

        if df.empty:
            print("No valid execution times available!")
            return

        fig = px.bar(
            df,
            x="pipeline_name",
            y="execution_time",
            color="status",
            title="Pipeline Execution Performance",
            labels={
                "pipeline_name": "Pipeline",
                "execution_time": "Execution Time (Seconds)",
                "status": "Status"
            },
            template="plotly_dark"
        )

        fig.show()


if __name__ == "__main__":
    visualizer = PipelineVisualizer()
    visualizer.show_execution_chart()