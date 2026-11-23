
import time
import schedule

from src.pipeline.github_pipeline import GitHubPipeline
from src.pipeline.news_pipeline import AINewsPipeline

from src.pipeline.jobs_pipeline import AIJobsPipeline
from src.pipeline.remotive_pipeline import RemotivePipeline
from src.pipeline.remoteok_pipeline import RemoteOKPipeline
from src.pipeline.jobicy_pipeline import JobicyPipeline
from src.pipeline.himalayas_pipeline import HimalayasPipeline

from src.pipeline.product_pipeline import AIProductPipeline


class PipelineScheduler:

    def __init__(self):

        self.pipelines = {
            "GitHub": GitHubPipeline,
            "AI News": AINewsPipeline,

            # 5 Job Sources
            "Arbeitnow Jobs": AIJobsPipeline,
            "Remotive Jobs": RemotivePipeline,
            "RemoteOK Jobs": RemoteOKPipeline,
            "Jobicy Jobs": JobicyPipeline,
            "Himalayas Jobs": HimalayasPipeline,

            "AI Products": AIProductPipeline,
        }

    def run_all_pipelines(self):

        print("\nSCHEDULED PIPELINE EXECUTION")
        print("=" * 40)

        for name, pipeline_class in self.pipelines.items():

            try:

                print(f"\nRunning {name} pipeline...")

                pipeline = pipeline_class()
                pipeline.run()

                print(f"{name} completed successfully!")

            except Exception as error:

                print(f"{name} failed: {error}")

    def start_scheduler(self):

        schedule.every(6).hours.do(
            self.run_all_pipelines
        )

        print("Pipeline Scheduler Started")
        print("Pipelines will run every 6 hours.")

        while True:

            schedule.run_pending()
            time.sleep(60)


if __name__ == "__main__":

    scheduler = PipelineScheduler()
    scheduler.start_scheduler()
