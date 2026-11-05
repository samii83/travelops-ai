from backend.agents.travel_agent import run_travel_agent


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


result = run_travel_agent(travel_request)


print("\n========== FINAL RESPONSE ==========\n")

print(result["final_response"])


print("\n========== EXECUTION LOG ==========\n")

for item in result["execution_log"]:
    print(item)