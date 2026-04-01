import os
from openai import OpenAI

# personal api key from openai
GPT_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = GPT_KEY)

def get_analysis(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()