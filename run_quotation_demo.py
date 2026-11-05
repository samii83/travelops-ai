
from backend.agents.langgraph_agent import run_travel_agent_graph
from backend.services.quotation_builder import build_quotation

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

agent_result = run_travel_agent_graph(travel_request)

quotation = build_quotation(
    travel_request,
    agent_result["execution_log"]
)

print("\n========== STRUCTURED QUOTATION ==========\n")
print(quotation.model_dump_json(indent=2))

print("\n========== FINANCIAL VALIDATION ==========\n")

item_total = sum(item.amount for item in quotation.items)

print("Item total:", item_total)
print("Quotation total:", quotation.total_estimated_cost)

assert item_total == quotation.total_estimated_cost
assert quotation.total_estimated_cost == 33500
assert quotation.cost_per_person == 16750

print("All financial checks passed!")
