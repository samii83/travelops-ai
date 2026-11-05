import json

from backend.tools.destination_search import search_destination
from backend.tools.hotel_search import search_hotels
from backend.tools.transport_search import search_transport
from backend.tools.budget_calculator import calculate_budget
from backend.tools.knowledge_search import search_travel_knowledge

TOOL_REGISTRY = {
    "search_destination": search_destination,
    "search_hotels": search_hotels,
    "search_transport": search_transport,
    "calculate_budget": calculate_budget,
    "search_travel_knowledge": search_travel_knowledge
}


def execute_tool(tool_name: str, arguments: str):

    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {tool_name}")

    try:
        parsed_arguments = json.loads(arguments)

        if not isinstance(parsed_arguments, dict):
            raise ValueError("Tool arguments must be a JSON object")

        tool_function = TOOL_REGISTRY[tool_name]

        result = tool_function(**parsed_arguments)

        return {
            "success": True,
            "tool": tool_name,
            "result": result
        }

    except Exception as error:

        return {
            "success": False,
            "tool": tool_name,
            "error": str(error)
        }