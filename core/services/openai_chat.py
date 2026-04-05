import os
from openai import OpenAI

SYSTEM_PROMPT = """
You are Roofmate's AI assistant for a Brisbane roofing business.

Business details:
- Company: Roofmate
- Location: Brisbane, Queensland
- Services:
  1. Metal Roof Painting
  2. Tile Roof Painting
  3. Roof Repairs
  4. Roof Pressure Cleaning
  5. Driveway Painting
  6. Driveway Cleaning

Your behavior:
- Be friendly, short, and professional.
- Help users understand services.
- Encourage quote requests.
- Ask for name, suburb, phone, and service needed when appropriate.
- Do not invent prices or guarantees.
- If unsure, say a team member can follow up.
- Keep replies concise, usually 2-5 sentences.
"""

def build_history(messages):
    history = []
    for msg in messages:
        history.append({
            "role": msg.role,
            "content": msg.content,
        })
    return history


def get_ai_reply(user_message: str, history_messages=None) -> str:
    history_messages = history_messages or []

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-5.2")

    input_payload = []

    for item in history_messages[-12:]:
        input_payload.append({
            "role": item["role"],
            "content": item["content"],
        })

    input_payload.append({
        "role": "user",
        "content": user_message,
    })

    response = client.responses.create(
        model=model,
        instructions=SYSTEM_PROMPT,
        input=input_payload,
    )

    return response.output_text.strip()