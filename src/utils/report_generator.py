
import os
import json
from datetime import datetime

from src.database.data_access import DataAccessLayer
from src.utils.data_insights import DataInsightsAnalyzer


class IntelligenceReportGenerator:

    def __init__(self):
        self.data_access = DataAccessLayer()
        self.insights_analyzer = DataInsightsAnalyzer()

        self.output_folder = "data/exports"
        os.makedirs(self.output_folder, exist_ok=True)

    def generate_report(self):

        summary = self.data_access.get_summary()
        insights = self.insights_analyzer.run_analysis()

        report = {
            "report_generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "datasets_summary": summary,
            "intelligence_insights": insights
        }

        file_name = (
            "intelligence_report_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".json"
        )

        file_path = os.path.join(
            self.output_folder,
            file_name
        )

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False,
                default=str
            )

        print("\nINTELLIGENCE REPORT GENERATED")
        print("=" * 40)
        print(f"File: {file_path}")

        return report


if __name__ == "__main__":

    generator = IntelligenceReportGenerator()

    generator.generate_report()
