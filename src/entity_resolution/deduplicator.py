
import re
from urllib.parse import urlparse


class StartupDeduplicator:

    def normalize_name(self, name):

        if not name:
            return ""

        name = name.lower().strip()

        name = re.sub(
            r"\b(inc|llc|ltd|limited|corp|corporation|pvt|private)\b",
            "",
            name
        )

        name = re.sub(r"[^a-z0-9]", "", name)

        return name

    def normalize_website(self, website):

        if not website:
            return ""

        website = website.strip().lower()

        if not website.startswith(("http://", "https://")):
            website = "https://" + website

        parsed = urlparse(website)

        domain = parsed.netloc.replace("www.", "")

        return domain.strip("/")

    def is_duplicate(self, startup, existing_data):

        new_name = self.normalize_name(
            startup.get("startup_name", "")
        )

        new_website = self.normalize_website(
            startup.get("website", "")
        )

        for existing in existing_data:

            existing_name = self.normalize_name(
                existing.get("startup_name", "")
            )

            existing_website = self.normalize_website(
                existing.get("website", "")
            )

            # Name match
            if new_name and existing_name == new_name:
                return True

            # Website match
            if new_website and existing_website == new_website:
                return True

        return False


if __name__ == "__main__":

    deduplicator = StartupDeduplicator()

    print("Startup Deduplicator Ready")
    print(
        deduplicator.normalize_name("OpenAI Inc.")
    )
    print(
        deduplicator.normalize_website("https://www.openai.com")
    )
