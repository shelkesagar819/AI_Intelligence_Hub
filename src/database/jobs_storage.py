
import csv
import os


class AIJobsStorage:

    def __init__(self):

        self.file_path = "data/raw/ai_jobs.csv"

        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True
        )

        self.fieldnames = [
            "company",
            "job_title",
            "location",
            "is_remote",
            "job_url",
            "job_type",
            "tags",
            "published_date",
            "source",
            "collected_at"
        ]

    def save_jobs(self, jobs):

        if not jobs:
            print("No jobs to save.")
            return 0

        existing_urls = set()

        if os.path.exists(self.file_path):

            with open(
                self.file_path,
                "r",
                encoding="utf-8",
                newline=""
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:

                    url = (row.get("job_url") or "").strip()

                    if url:
                        existing_urls.add(url)

        new_jobs = []

        for job in jobs:

            if not isinstance(job, dict):
                continue

            job_url = str(job.get("job_url") or "").strip()

            if not job_url or job_url in existing_urls:
                continue

            existing_urls.add(job_url)

            clean_job = {
                field: job.get(field, "")
                for field in self.fieldnames
            }

            clean_job["job_url"] = job_url

            new_jobs.append(clean_job)

        file_exists = (
            os.path.exists(self.file_path)
            and os.path.getsize(self.file_path) > 0
        )

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

            if not file_exists:
                writer.writeheader()

            writer.writerows(new_jobs)

        print(f"Jobs received: {len(jobs)}")
        print(f"New jobs saved: {len(new_jobs)}")
        print(f"Duplicates skipped: {len(jobs) - len(new_jobs)}")

        return len(new_jobs)
