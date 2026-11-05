
from backend.schemas.quotation import TravelQuotation, QuotationItem


def get_tool_result(execution_log, tool_name):
    for entry in execution_log:
        if entry.get("tool") == tool_name and entry.get("success"):
            return entry.get("result", {})
    return None


def build_quotation(travel_request: dict, execution_log: list):

    destination_data = get_tool_result(
        execution_log, "search_destination"
    )
    hotel_data = get_tool_result(
        execution_log, "search_hotels"
    )
    transport_data = get_tool_result(
        execution_log, "search_transport"
    )
    budget_data = get_tool_result(
        execution_log, "calculate_budget"
    )

    if not all([destination_data, hotel_data, transport_data, budget_data]):
        raise ValueError(
            "Cannot generate quotation: one or more required tools failed."
        )

    if not destination_data.get("found"):
        raise ValueError("Destination information is unavailable.")

    if not hotel_data.get("found") or not hotel_data.get("hotels"):
        raise ValueError("No matching hotel estimate is available.")

    if not transport_data.get("found"):
        raise ValueError("Transport estimate is unavailable.")

    hotels = hotel_data["hotels"]
    selected_hotel = hotels[0]

    breakdown = budget_data["breakdown"]

    items = [
        QuotationItem(
            category="Accommodation",
            description=f'{selected_hotel["name"]} - '
                        f'{budget_data["nights"]} nights, '
                        f'{budget_data["rooms"]} room(s)',
            amount=breakdown["hotel"]
        ),
        QuotationItem(
            category="Transport",
            description="Estimated round-trip transportation",
            amount=breakdown["transport"]
        ),
        QuotationItem(
            category="Food",
            description="Estimated food expenses",
            amount=breakdown["food"]
        ),
        QuotationItem(
            category="Activities",
            description="Estimated attraction expenses",
            amount=breakdown["activities"]
        ),
        QuotationItem(
            category="Local transport",
            description="Estimated local transportation",
            amount=breakdown["local_transport"]
        )
    ]

    budget = travel_request.get("budget")
    total = budget_data["total_estimated_cost"]

    attractions = [
        f'{a["name"]} (₹{a["estimated_cost_per_person"]} per person)'
        for a in destination_data.get("attractions", [])
    ]

    quotation = TravelQuotation(
        destination=travel_request["destination"],
        duration_days=travel_request["duration_days"],
        travelers=travel_request["travelers"],
        currency=budget_data["currency"],
        hotel_name=selected_hotel["name"],
        items=items,
        total_estimated_cost=total,
        cost_per_person=budget_data["cost_per_person"],
        budget=budget,
        remaining_budget=round(budget - total, 2) if budget is not None else None,
        attractions=attractions,
        assumptions=[
            "Prices are illustrative estimates, not live supplier quotations.",
            "Hotel room occupancy is based on the demo calculator assumption.",
            "Transport and hotel availability have not been confirmed.",
            "Attraction prices are estimates from the demonstration dataset."
        ]
    )

    return quotation
