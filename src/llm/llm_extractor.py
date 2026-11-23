
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

        if not prompt:
            return "Please enter a question."

        # Gemini
        if self.gemini_key:
            try:
                from google import genai

                client = genai.Client(api_key=self.gemini_key)

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                if response.text:
                    return response.text

            except Exception as error:
                print("Gemini failed:", error)

        # Groq
        if self.groq_key:
            try:
                from groq import Groq

                client = Groq(api_key=self.groq_key)

                response = client.chat.completions.create(
                   model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an intelligent AI assistant "
                                "for an AI Intelligence Hub. "
                                "Give clear, accurate and helpful answers."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3
                )

                return response.choices[0].message.content

            except Exception as error:
                print("Groq failed:", error)

        # DeepSeek
        if self.deepseek_key:
            try:
                from openai import OpenAI

                client = OpenAI(
                    api_key=self.deepseek_key,
                    base_url="https://api.deepseek.com"
                )

                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful AI assistant."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3
                )

                return response.choices[0].message.content

            except Exception as error:
                print("DeepSeek failed:", error)

        return "No working LLM API provider is available."

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

    def _parse_json(self, response):

        if not response:
            return {}

        response = response.strip()

        if response.startswith("```"):
            response = response.split("\n", 1)[-1]
            response = response.rsplit("```", 1)[0].strip()

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            print("Invalid JSON response.")
            return {}


if __name__ == "__main__":

    extractor = LLMExtractor()

    print("LLM Extractor Initialized")
    print("Gemini Configured:", bool(extractor.gemini_key))
    print("Groq Configured:", bool(extractor.groq_key))
    print("DeepSeek Configured:", bool(extractor.deepseek_key))

    print("\nTesting AI Response...")

    result = extractor.generate_response(
        "Explain Artificial Intelligence in 2 simple sentences."
    )

    print("\nAI Response:")
    print(result)
