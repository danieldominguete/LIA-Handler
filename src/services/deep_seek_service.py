from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

import os

# Environment variables
load_dotenv(find_dotenv())
DEEP_SEEK_KEY = os.getenv("DEEP_SEEK_KEY")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=DEEP_SEEK_KEY,
)

completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "teste",
        "X-Title": "teste",
    },
    model="deepseek/deepseek-r1:free",
    messages=[
        {
            "role": "user",
            "content": "Prepare uma resposta no idioma português Brasil. Qual é o santo católico que se celebra no dia de 12 de março segundo o calendário liturgico do Brasil? Envie uma resposta em texto sem formatação em idioma português do brasil.",
        }
    ],
)
print(completion.choices[0].message.content)
