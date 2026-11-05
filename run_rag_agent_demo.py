
from backend.agents.langgraph_agent import run_travel_agent_graph

travel_request = {
    "destination": "Goa",
    "duration_days": 5,
    "travelers": 2,
    "budget": 40000,
    "currency": "INR",
    "origin": "Bhubaneswar",
    "hotel_preference": "comfortable hotels",
    "travel_style": None
}

result = run_travel_agent_graph(travel_request)

print("\n========== RAG + LANGGRAPH RESPONSE ==========\n")
print(result["final_response"])

print("\n========== TOOL EXECUTION LOG ==========\n")

for item in result["execution_log"]:
    print(item)
