"""
Gemini Interface
"""

import logging
from dateutil.parser import parse
import uuid, datetime, os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Environment variables
load_dotenv(find_dotenv())
GEMINI_KEY = os.getenv("GEMINI_KEY")


class LiaGemini:
    def __init__(self):

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=GEMINI_KEY,
        )

    def get_answer(self, question: str) -> str:

        completion = self.client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "LIA",
                "X-Title": "LIA",
            },
            model="google/gemini-2.0-pro-exp-02-05:free",
            temperature=2.0,
            top_p=0.9,
            messages=[
                {
                    "role": "user",
                    "content": question,
                }
            ],
        )

        answer = completion.choices[0].message.content

        if answer:
            return answer
        else:
            return ""
