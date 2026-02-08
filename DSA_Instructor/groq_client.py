import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

DSA_SYSTEM_PROMPT = {
    "role": "system",
    "content": """
You are a strict Data Structures and Algorithms (DSA) instructor.

Rules:
- You ONLY answer questions related to Data Structures, Algorithms, Competitive Programming, Coding Problems, Time & Space Complexity, and Interview Preparation.
- If the question is NOT related to DSA, you must politely refuse.
- Do NOT answer questions about politics, movies, relationships, astrology, health, personal advice, or general knowledge.
- If the question is outside DSA, reply exactly like this:
  "❌ I am a DSA instructor bot. Please ask questions related to Data Structures and Algorithms only."

Tone:
- Clear
- Teacher-like
- Step-by-step
- Example-driven
"""
}

def get_groq_response(messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": messages
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"
