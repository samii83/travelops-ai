import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

response = client.chat.completions.create(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
    messages=[
        {
            "role": "user",
            "content": "Return a JSON object with destination set to Goa."
        }
    ],
    response_format={"type": "json_object"},
    temperature=0
)

print(response.choices[0].message.content)