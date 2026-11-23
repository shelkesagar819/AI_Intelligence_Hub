
import time

from src.utils.logger import log_info, log_error
from src.database.pipeline_history_storage import PipelineHistoryStorage


class PipelineTracker:

    def __init__(self):
        self.history_storage = PipelineHistoryStorage()

    def track(self, pipeline_name, pipeline_function, *args, **kwargs):

        start_time = time.time()

        log_info(f"{pipeline_name} started")

        try:

            result = pipeline_function(*args, **kwargs)

            execution_time = round(
                time.time() - start_time, 2
            )

            report = {
                "pipeline": pipeline_name,
                "status": "SUCCESS",
                "execution_time": execution_time,
                "result": result,
                "error": ""
            }

            self.history_storage.save_history(report)

            log_info(
                f"{pipeline_name} completed successfully "
                f"in {execution_time} seconds"
            )

            return report

        except Exception as error:

            execution_time = round(
                time.time() - start_time, 2
            )

            report = {
                "pipeline": pipeline_name,
                "status": "FAILED",
                "execution_time": execution_time,
                "result": None,
                "error": str(error)
            }

            self.history_storage.save_history(report)

            log_error(
                f"{pipeline_name} failed: {error}"
            )

            return report


if __name__ == "__main__":

    tracker = PipelineTracker()

    print("Pipeline Tracker Ready")
