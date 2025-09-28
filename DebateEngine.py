from openai import OpenAI
import os
from prompts import OPENING_PROMPT, REBUTTAL_PROMPT, CLOSING_PROMPT

# Pick model from env var or fallback
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
KEY = os.environ.get("OPENAI_API_KEY")

# Ensure key exists
if not KEY:
    raise EnvironmentError("Set OPENAI_API_KEY in your environment.")

# Create client instance
client = OpenAI(api_key=KEY)

def call_llm(system_prompt: str, user_prompt: str, temperature=0.4):

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=700,
    )
    return resp.choices[0].message.content.strip()

# --- Debate-specific functions ---

def generate_openings(topic: str):

    sys = "You are a structured debate assistant. Provide clear arguments for both sides."
    user = OPENING_PROMPT.format(topic=topic)
    return call_llm(sys, user, temperature=0.4)

def generate_rebuttals(topic: str, pro_text: str, con_text: str):

    sys = "You are a critical debate engine. Provide targeted rebuttals to prior points."
    user = REBUTTAL_PROMPT.format(topic=topic)
    user += f"\n\nPro arguments:\n{pro_text}\n\nCon arguments:\n{con_text}"
    return call_llm(sys, user, temperature=0.45)

def generate_closing(topic: str, side: str):

    sys = "You are a persuasive debate coach. Provide crisp closing remarks."
    user = CLOSING_PROMPT.format(topic=topic, side=side)
    return call_llm(sys, user, temperature=0.45)