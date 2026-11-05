
from backend.agents.langgraph_agent import run_travel_agent_graph
from backend.services.quotation_builder import build_quotation
from backend.services.pdf_generator import generate_quotation_pdf

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

quotation = build_quotation(
    travel_request,
    result["execution_log"]
)

pdf_path = generate_quotation_pdf(quotation)

print("\nPDF successfully generated:")
print(pdf_path)
