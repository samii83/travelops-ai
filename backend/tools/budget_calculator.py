import math


def calculate_budget(
    hotel_price_per_night: float,
    duration_days: int,
    travelers: int,
    transport_per_person: float,
    food_per_person_per_day: float,
    activities_per_person: float,
    local_transport: float = 0
):

    if duration_days < 1 or travelers < 1:
        raise ValueError("Invalid trip duration or traveler count")

    if any(
        cost < 0
        for cost in [
            hotel_price_per_night,
            transport_per_person,
            food_per_person_per_day,
            activities_per_person,
            local_transport
        ]
    ):
        raise ValueError("Costs cannot be negative")

    nights = max(duration_days - 1, 0)

    rooms = math.ceil(travelers / 2)

    hotel_cost = (
        hotel_price_per_night * nights * rooms
    )

    transport_cost = transport_per_person * travelers

    food_cost = (
        food_per_person_per_day
        * duration_days
        * travelers
    )

    activities_cost = (
        activities_per_person * travelers
    )

    total = (
        hotel_cost
        + transport_cost
        + food_cost
        + activities_cost
        + local_transport
    )

    return {
        "currency": "INR",
        "breakdown": {
            "hotel": hotel_cost,
            "transport": transport_cost,
            "food": food_cost,
            "activities": activities_cost,
            "local_transport": local_transport
        },
        "total_estimated_cost": total,
        "cost_per_person": round(total / travelers, 2),
        "nights": nights,
        "rooms": rooms,
        "data_type": "illustrative_estimate"
    }