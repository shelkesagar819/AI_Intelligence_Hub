
import os
import pandas as pd


class MasterDataExporter:

    def __init__(self):
        self.raw_folder = "data/raw"
        self.processed_folder = "data/processed"
        self.export_folder = "data/exports"
        os.makedirs(self.export_folder, exist_ok=True)

    def export_to_excel(self):

        datasets = {
            "GitHub": "github_repositories.csv",
            "AI_News": "ai_news.csv",
            "AI_Jobs": "ai_jobs.csv",
            "AI_Products": "ai_products.csv",
            "Startups": "startups.csv",
            "Research_Papers": "research_papers.csv",
        }

        output_file = os.path.join(
            self.export_folder,
            "AI_Intelligence_Master_Data.xlsx"
        )

        exported_count = 0
        total_records = 0

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

            for sheet_name, file_name in datasets.items():

                processed_file = os.path.join(
                    self.processed_folder,
                    file_name.replace(".csv", "_cleaned.csv")
                )
                raw_file = os.path.join(self.raw_folder, file_name)

                file_path = (
                    processed_file if os.path.exists(processed_file)
                    else raw_file if os.path.exists(raw_file)
                    else None
                )

                if file_path is None:
                    print(f"Skipped: {file_name} not found")
                    continue

                try:
                    df = pd.read_csv(file_path)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

                    print(f"Exported: {sheet_name} | {len(df)} records")
                    exported_count += 1
                    total_records += len(df)

                except Exception as error:
                    print(f"Error exporting {sheet_name}: {error}")

            pd.DataFrame(columns=[
                "entity_id",
                "entity_name",
                "canonical_name",
                "source",
                "match_status",
                "confidence_score"
            ]).to_excel(
                writer,
                sheet_name="Entity_Mapping_Log",
                index=False
            )

            exported_count += 1

        print("\n" + "=" * 40)
        print("MASTER EXCEL EXPORT REPORT")
        print("=" * 40)
        print(f"Sheets Created : {exported_count}")
        print(f"Total Records  : {total_records}")
        print(f"Output File    : {output_file}")
        print("=" * 40)


if __name__ == "__main__":
    exporter = MasterDataExporter()
    exporter.export_to_excel()
