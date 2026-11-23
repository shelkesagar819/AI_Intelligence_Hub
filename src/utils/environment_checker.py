
import os
import sys


class EnvironmentChecker:

    def __init__(self):

        self.required_folders = [
            "data/raw",
            "data/processed",
            "data/exports",
            "data/logs",
            "src/scrapers",
            "src/pipeline",
            "src/database",
            "src/utils",
            "src/llm",
            "src/entity_resolution",
            "docs",
            "config",
        ]

        self.required_files = [
            "requirements.txt",
            "app.py",
        ]

    def check_python(self):

        print("\nPYTHON ENVIRONMENT")
        print("-" * 40)

        print(f"Python Version: {sys.version.split()[0]}")
        print(f"Python Executable: {sys.executable}")

    def check_folders(self):

        print("\nFOLDER CHECK")
        print("-" * 40)

        for folder in self.required_folders:

            if os.path.isdir(folder):
                print(f"[OK] {folder}")
            else:
                print(f"[MISSING] {folder}")

    def check_files(self):

        print("\nFILE CHECK")
        print("-" * 40)

        for file_path in self.required_files:

            if os.path.isfile(file_path):
                print(f"[OK] {file_path}")
            else:
                print(f"[MISSING] {file_path}")

    def check_env_file(self):

        print("\nENVIRONMENT CONFIG")
        print("-" * 40)

        if os.path.isfile(".env"):
            print("[OK] .env file exists")
        else:
            print("[INFO] .env file not created (optional)")

    def run(self):

        print("\nAI INTELLIGENCE HUB - ENVIRONMENT CHECK")
        print("=" * 50)

        self.check_python()
        self.check_folders()
        self.check_files()
        self.check_env_file()

        print("\nEnvironment check completed.")


if __name__ == "__main__":

    checker = EnvironmentChecker()
    checker.run()
