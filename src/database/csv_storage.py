
import csv
import os
import logging


class CSVStorage:

    def __init__(self):

        self.file_path = "data/raw/startups.csv"

        self.fieldnames = [
            "startup_name",
            "description",
            "website",
            "industry",
            "employee_count",
            "source",
            "source_url",
            "collected_at"
        ]

        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True
        )

    def save_startup(self, startup_data):

        file_exists = os.path.isfile(self.file_path)

        is_empty = (
            not file_exists
            or os.path.getsize(self.file_path) == 0
        )

        try:

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

                if is_empty:
                    writer.writeheader()

                clean_data = {
                    field: startup_data.get(field, "")
                    for field in self.fieldnames
                }

                writer.writerow(clean_data)

            logging.info(
                "Startup data saved: %s",
                startup_data.get("startup_name")
            )

            return True

        except Exception as error:

            logging.error(
                "Startup storage failed: %s",
                error
            )

            return False


if __name__ == "__main__":

    storage = CSVStorage()

    print("Startup CSV Storage Ready")
    print("File:", storage.file_path)
    print("Columns:", storage.fieldnames)
