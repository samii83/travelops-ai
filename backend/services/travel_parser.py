import os
import json

from dotenv import load_dotenv
from groq import Groq

from backend.schemas.travel_request import TravelRequest


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


SYSTEM_PROMPT = """
You are a professional travel request extraction assistant.

Your task is to extract travel requirements from
natural language messages.

Return ONLY a valid JSON object.

The JSON must contain these fields:

{
    "destination": string or null,
    "duration_days": integer or null,
    "travelers": integer or null,
    "budget": number or null,
    "currency": string,
    "origin": string or null,
    "hotel_preference": string or null,
    "travel_style": string or null
}

Rules:

1. Extract only information explicitly provided
   or unambiguously implied.

2. Never invent missing information.

3. Return null for missing fields.

4. Number of travelers means people, not rooms.

5. Budget must be numeric, without currency symbols.

6. Use INR when the user specifies Indian rupees.

7. If currency is not specified, default to INR.

8. Do not generate a travel itinerary.

9. Return only JSON, without Markdown.
"""


def parse_travel_request(message: str) -> TravelRequest:

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ],
        response_format={
            "type": "json_object"
        },
        temperature=0,
        max_completion_tokens=1000
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Groq returned an empty response")

    data = json.loads(content)

    return TravelRequest.model_validate(data)