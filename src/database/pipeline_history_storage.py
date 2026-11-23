
import os
import csv
from datetime import datetime


class PipelineHistoryStorage:

    def __init__(self):

        self.file_path = "data/processed/pipeline_history.csv"

        self.fieldnames = [
            "pipeline_name",
            "status",
            "execution_time",
            "result",
            "timestamp",
            "error"
        ]

        os.makedirs(
            "data/processed",
            exist_ok=True
        )

        if not os.path.exists(self.file_path):
            with open(
                self.file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=self.fieldnames
                )

                writer.writeheader()

    def save_history(self, result):

        try:

            file_exists = os.path.exists(self.file_path)

            with open(
                self.file_path,
                "a",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=self.fieldnames,
                    extrasaction="ignore"
                )

                if not file_exists or os.path.getsize(self.file_path) == 0:
                    writer.writeheader()

                writer.writerow({
                    "pipeline_name": result.get("pipeline", ""),
                    "status": result.get("status", ""),
                    "execution_time": result.get("execution_time", 0),
                    "result": str(result.get("result", "")),
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "error": result.get("error", "")
                })

            print("Pipeline history saved successfully!")
            return True

        except Exception as error:

            print(f"Pipeline history save failed: {error}")
            return False


if __name__ == "__main__":

    storage = PipelineHistoryStorage()

    print("Pipeline History Storage Ready")
    print("Columns:", storage.fieldnames)
