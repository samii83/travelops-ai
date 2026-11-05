import os
import json

from dotenv import load_dotenv
from groq import Groq

from backend.agents.tool_definitions import TRAVEL_TOOLS
from backend.agents.tool_executor import execute_tool


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


SYSTEM_PROMPT = """
You are TravelOps AI, an intelligent travel operations agent.

Your job is to prepare travel quotations.

You have access to four tools:

1. search_destination
2. search_hotels
3. search_transport
4. calculate_budget

INSTRUCTIONS:

- Use the tools to retrieve information.
- Do not invent hotel prices or transportation prices.
- Search for destination, hotels and transport first.
- Use the returned tool results to calculate the budget.
- Use the destination dataset's food and activity estimates.
- For activities, choose suitable attractions and sum their
  estimated costs per person.
- Never invent values when tool results are missing.
- If a tool fails, explain the limitation.
- Clearly label all prices as estimates.
- The dataset contains demonstration data, not live availability.
- Respect the user's budget.
- If the estimated cost exceeds the budget, explain why.

You may call multiple independent search tools in one turn.
Only calculate the budget after obtaining the relevant costs.

Provide a concise final travel quotation.
"""


def run_travel_agent(travel_request: dict):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": (
                "Prepare a travel quotation using this request:\n"
                + json.dumps(travel_request)
            )
        }
    ]

    execution_log = []

    max_iterations = 6

    for iteration in range(max_iterations):

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TRAVEL_TOOLS,
            tool_choice="auto",
            temperature=0.2,
            max_completion_tokens=2000
        )

        assistant_message = response.choices[0].message

        # No more tool calls: return final answer
        if not assistant_message.tool_calls:

            return {
                "success": True,
                "final_response": assistant_message.content,
                "execution_log": execution_log
            }

        # Preserve the assistant's tool-call message
        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        # Execute every requested tool
        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            print(f"Executing tool: {tool_name}")

            result = execute_tool(
                tool_name,
                arguments
            )

            execution_log.append(result)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return {
        "success": False,
        "final_response": "Maximum agent iterations reached.",
        "execution_log": execution_log
    }