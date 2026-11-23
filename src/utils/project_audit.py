
import os


class ProjectAudit:

    def __init__(self):
        self.project_root = os.getcwd()

        self.required_files = [
            "app.py",
            "src/database/data_access.py",
            "src/database/csv_storage.py",
            "src/database/research_storage.py",
            "src/database/github_storage.py",
            "src/database/news_storage.py",
            "src/database/jobs_storage.py",
            "src/database/product_storage.py",
            "src/database/pipeline_history_storage.py",
            "src/pipeline/run_all.py",
            "src/pipeline/pipeline_controller.py",
            "src/pipeline/pipeline_tracker.py",
            "src/pipeline/data_processing_pipeline.py",
            "src/pipeline/data_aggregator.py",
            "src/utils/data_cleaner.py",
            "src/utils/data_validator.py",
            "src/utils/data_quality.py",
            "src/utils/data_insights.py",
            "src/utils/search_engine.py",
            "src/utils/data_filter.py",
            "src/utils/report_generator.py",
        ]

    def run_audit(self):

        print("\nAI INTELLIGENCE HUB - PROJECT AUDIT")
        print("=" * 55)

        existing = 0
        missing = 0

        for file_path in self.required_files:

            if os.path.exists(file_path):

                print(f"[OK]      {file_path}")
                existing += 1

            else:

                print(f"[MISSING] {file_path}")
                missing += 1

        print("\nAUDIT SUMMARY")
        print("-" * 40)
        print(f"Existing Files : {existing}")
        print(f"Missing Files : {missing}")
        print(f"Total Checked : {len(self.required_files)}")

        return {
            "existing": existing,
            "missing": missing,
            "total": len(self.required_files)
        }


if __name__ == "__main__":

    audit = ProjectAudit()

    audit.run_audit()
