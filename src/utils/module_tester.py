
import importlib


class ModuleTester:

    def __init__(self):

        self.modules = [
            "src.database.data_access",
            "src.database.csv_storage",
            "src.database.github_storage",
            "src.database.news_storage",
            "src.database.jobs_storage",
            "src.database.product_storage",
            "src.database.pipeline_history_storage",
            "src.pipeline.pipeline_tracker",
            "src.pipeline.github_pipeline",
            "src.pipeline.news_pipeline",
            "src.pipeline.jobs_pipeline",
            "src.pipeline.product_pipeline",
            "src.pipeline.data_aggregator",
            "src.pipeline.data_processing_pipeline",
            "src.utils.data_cleaner",
            "src.utils.data_validator",
            "src.utils.data_quality",
            "src.utils.data_insights",
            "src.utils.search_engine",
            "src.utils.data_filter",
            "src.utils.report_generator",
        ]

    def test_modules(self):

        print("\nMODULE IMPORT TEST")
        print("=" * 50)

        passed = 0
        failed = 0

        for module_name in self.modules:

            try:

                importlib.import_module(module_name)

                print(f"[PASS] {module_name}")
                passed += 1

            except Exception as error:

                print(f"[FAIL] {module_name}")
                print(f"       Error: {error}")
                failed += 1

        print("\nTEST SUMMARY")
        print("-" * 40)
        print(f"Passed : {passed}")
        print(f"Failed : {failed}")
        print(f"Total  : {len(self.modules)}")

        return passed, failed


if __name__ == "__main__":

    tester = ModuleTester()

    tester.test_modules()
