from src.pipeline.pipeline_tracker import PipelineTracker

from src.pipeline.github_pipeline import GitHubPipeline
from src.pipeline.news_pipeline import AINewsPipeline

from src.pipeline.jobs_pipeline import AIJobsPipeline
from src.pipeline.remotive_pipeline import RemotivePipeline
from src.pipeline.remoteok_pipeline import RemoteOKPipeline
from src.pipeline.jobicy_pipeline import JobicyPipeline
from src.pipeline.himalayas_pipeline import HimalayasPipeline

from src.pipeline.product_pipeline import AIProductPipeline
from src.pipeline.startup_pipeline import StartupPipeline
from src.pipeline.research_pipeline import ResearchPipeline


class PipelineController:

    def __init__(self):

        self.tracker = PipelineTracker()

        self.pipelines = [
            ("GitHub Pipeline", GitHubPipeline),
            ("AI News Pipeline", AINewsPipeline),

            # 5 Job Sources
            ("Arbeitnow Jobs Pipeline", AIJobsPipeline),
            ("Remotive Jobs Pipeline", RemotivePipeline),
            ("RemoteOK Jobs Pipeline", RemoteOKPipeline),
            ("Jobicy Jobs Pipeline", JobicyPipeline),
            ("Himalayas Jobs Pipeline", HimalayasPipeline),

            ("AI Products Pipeline", AIProductPipeline),
            ("Startup Pipeline", StartupPipeline),
            ("Research Pipeline", ResearchPipeline),
        ]

    def execute_all(self):

        print("\n" + "=" * 60)
        print("AI INTELLIGENCE HUB - MASTER CONTROLLER")
        print("=" * 60)

        results = []

        for name, pipeline_class in self.pipelines:

            print(f"\nStarting {name}")

            try:

                pipeline = pipeline_class()

                if name == "Startup Pipeline":

                    result = self.tracker.track(
                        name,
                        pipeline.run,
                        [
                            "https://openai.com",
                            "https://www.anthropic.com",
                            "https://deepmind.google"
                        ]
                    )

                elif name == "Research Pipeline":

                    print(
                        "Skipped: Research API requires "
                        "controlled execution."
                    )
                    continue

                else:

                    result = self.tracker.track(
                        name,
                        pipeline.run
                    )

                results.append(result)

                print(
                    f"{result['status']} | {name}"
                )

            except Exception as error:

                print(
                    f"FAILED | {name} | {error}"
                )

        print("\n" + "=" * 60)
        print("CONTROLLER EXECUTION COMPLETED")
        print("=" * 60)

        return results


if __name__ == "__main__":

    controller = PipelineController()
    controller.execute_all()