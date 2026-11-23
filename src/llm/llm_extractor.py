
import os
import json
from dotenv import load_dotenv

load_dotenv()


class LLMExtractor:

    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")

    def generate_response(self, prompt):

        if not prompt or not prompt.strip():
            return "Please enter a question."

        errors = []

        # ==========================================
        # 1. GEMINI
        # ==========================================
        if self.gemini_key:

            try:
                from google import genai

                client = genai.Client(
                    api_key=self.gemini_key
                )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                if response.text and response.text.strip():
                    print("Gemini: Response generated successfully.")
                    return response.text

                errors.append("Gemini returned an empty response.")

            except Exception as error:
                errors.append(f"Gemini failed: {error}")
                print(f"Gemini error: {error}")

        # ==========================================
        # 2. GROQ
        # ==========================================
        if self.groq_key:

            try:
                from groq import Groq

                client = Groq(
                    api_key=self.groq_key,
                    timeout=30.0,
                    max_retries=1
                )

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an intelligent AI assistant "
                                "for AI Intelligence Hub. "
                                "Give accurate, clear, structured "
                                "and helpful answers. "
                                "Never invent dataset information."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3
                )

                answer = response.choices[0].message.content

                if answer and answer.strip():
                    print("Groq: Response generated successfully.")
                    return answer

                errors.append("Groq returned an empty response.")

            except Exception as error:
                errors.append(f"Groq failed: {error}")
                print(f"Groq error: {error}")

        # ==========================================
        # 3. DEEPSEEK
        # ==========================================
        if self.deepseek_key:

            try:
                from openai import OpenAI

                client = OpenAI(
                    api_key=self.deepseek_key,
                    base_url="https://api.deepseek.com",
                    timeout=30.0,
                    max_retries=1
                )

                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful and accurate "
                                "AI assistant. Provide clear answers "
                                "and never invent information."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3
                )

                answer = response.choices[0].message.content

                if answer and answer.strip():
                    print("DeepSeek: Response generated successfully.")
                    return answer

                errors.append("DeepSeek returned an empty response.")

            except Exception as error:
                errors.append(f"DeepSeek failed: {error}")
                print(f"DeepSeek error: {error}")

        # ==========================================
        # 4. NO PROVIDER AVAILABLE
        # ==========================================

        if not any([
            self.gemini_key,
            self.groq_key,
            self.deepseek_key
        ]):
            return "No working LLM API provider available. No API keys configured."

        print("All LLM providers failed.")

        for error in errors:
            print(error)

        return "No working LLM API provider available. Check provider errors in logs."

    # ==========================================
    # JSON EXTRACTION
    # ==========================================

    def extract_json(self, text):

        if not text:
            return {}

        prompt = (
            "Extract structured information from the following text. "
            "Return only valid JSON. Do not include markdown fences.\n\n"
            + text
        )

        response = self.generate_response(prompt)

        if response.startswith("No working LLM"):
            return {}

        return self._parse_json(response)

    # ==========================================
    # JSON PARSER
    # ==========================================

    def _parse_json(self, response):

        if not response:
            return {}

        response = response.strip()

        if response.startswith("```"):

            response = response.split("\n", 1)[-1]
            response = response.rsplit("```", 1)[0].strip()

            if response.startswith("json"):
                response = response[4:].strip()

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            print("Invalid JSON response.")
            return {}

    # ==========================================
    # PROVIDER STATUS
    # ==========================================

    def get_provider_status(self):

        return {
            "Gemini Configured": bool(self.gemini_key),
            "Groq Configured": bool(self.groq_key),
            "DeepSeek Configured": bool(self.deepseek_key)
        }


if __name__ == "__main__":

    extractor = LLMExtractor()

    print("LLM Extractor Initialized")
    print(extractor.get_provider_status())

    print("\nTesting AI Response...")

    result = extractor.generate_response(
        "Explain Artificial Intelligence in 2 simple sentences."
    )

    print("\nAI Response:")
    print(result)
