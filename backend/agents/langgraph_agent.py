
import os
import json
import operator

from typing import TypedDict, Annotated
from dotenv import load_dotenv
from groq import Groq
from langgraph.graph import StateGraph, END

from backend.agents.tool_definitions import TRAVEL_TOOLS
from backend.agents.tool_executor import execute_tool

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


SYSTEM_PROMPT = """
You are TravelOps AI, an intelligent travel operations agent.

Your job is to prepare travel quotations using the available tools.

Available tools:
1. search_destination
2. search_hotels
3. search_transport
4. calculate_budget
5. search_travel_knowledge

RAG INSTRUCTIONS:
- Use search_travel_knowledge to retrieve relevant destination information and travel policies.
- Use retrieved documents when explaining hotel rules, availability, pricing assumptions and travel restrictions.
- Treat retrieved documents as reference information, not live booking data.
- Never claim that an item is available just because it appears in a document.
- Do not invent facts that are absent from retrieved documents.

Rules:
- Retrieve destination, hotel and transport information before calculating.
- Use only values returned by tools for prices.
- Use destination tool results for food and local transport estimates.
- Select suitable attractions and sum their actual dataset costs.
- Never invent hotels, attractions, prices or services.
- If data is unavailable, clearly explain the limitation.
- All prices must be labelled as estimates.
- The dataset contains demonstration data, not live availability.
- Respect the user's budget.
- Return a clear, structured quotation.
- Mention only attractions present in the destination tool results.
- Never claim that a tour, guide, ticket or service is included unless the dataset explicitly confirms it.
- Do not calculate prices yourself. The budget calculator provides the authoritative total.
- Never invent availability or booking confirmations.
"""


# 1. Define the graph state
class TravelAgentState(TypedDict):
    messages: Annotated[list, operator.add]
    execution_log: Annotated[list, operator.add]


# 2. Agent node: ask Groq what to do
def agent_node(state: TravelAgentState):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=state["messages"],
        tools=TRAVEL_TOOLS,
        tool_choice="auto",
        temperature=0.2,
        max_completion_tokens=2000
    )

    assistant_message = response.choices[0].message

    return {
        "messages": [
            assistant_message.model_dump(exclude_none=True)
        ]
    }


# 3. Tool node: execute requested Python functions
def tool_node(state: TravelAgentState):

    last_message = state["messages"][-1]

    new_messages = []
    new_logs = []

    # Retrieve destination information from previous tool results
    destination_data = None

    for log in state["execution_log"]:
        if log.get("tool") == "search_destination" and log.get("success"):
            destination_data = log["result"]
            break

    for tool_call in last_message.get("tool_calls", []):

        tool_name = tool_call["function"]["name"]
        arguments = json.loads(tool_call["function"]["arguments"])

        # Never trust the LLM to perform financial arithmetic
        if tool_name == "calculate_budget":

            if not destination_data or not destination_data.get("found"):
                result = {
                    "success": False,
                    "tool": tool_name,
                    "error": "Destination data unavailable for budget calculation."
                }
                new_logs.append(result)

                new_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": json.dumps(result)
                })
                continue

            attractions = destination_data.get("attractions", [])

            # Include all priced attractions from our demo dataset
            verified_activity_cost = sum(
                attraction["estimated_cost_per_person"]
                for attraction in attractions
            )

            arguments["activities_per_person"] = verified_activity_cost

        print(f"Executing tool: {tool_name}")

        result = execute_tool(
            tool_name,
            json.dumps(arguments)
        )

        new_logs.append(result)

        new_messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": json.dumps(result)
        })

    return {
        "messages": new_messages,
        "execution_log": new_logs
    }


# 4. Decide whether to execute tools or finish
def route_after_agent(state: TravelAgentState):

    last_message = state["messages"][-1]

    if last_message.get("tool_calls"):
        return "tools"

    return END


# 5. Build the LangGraph workflow
workflow = StateGraph(TravelAgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "tools": "tools",
        END: END
    }
)

workflow.add_edge("tools", "agent")

travel_graph = workflow.compile()


# 6. Public function used by our application
def run_travel_agent_graph(travel_request: dict):

    initial_messages = [
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

    result = travel_graph.invoke({
        "messages": initial_messages,
        "execution_log": []
    })

    final_message = result["messages"][-1]

    return {
        "success": True,
        "final_response": final_message.get("content"),
        "execution_log": result["execution_log"]
    }
