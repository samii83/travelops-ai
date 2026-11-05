from backend.tools.destination_search import search_destination
from backend.tools.hotel_search import search_hotels
from backend.tools.transport_search import search_transport
from backend.tools.budget_calculator import calculate_budget


print("\n--- DESTINATION SEARCH ---")

print(search_destination("Goa"))


print("\n--- HOTEL SEARCH ---")

print(search_hotels("Goa", "comfortable"))


print("\n--- TRANSPORT SEARCH ---")

print(search_transport("Goa", "Bhubaneswar", 2))


print("\n--- BUDGET CALCULATOR ---")

print(
    calculate_budget(
        hotel_price_per_night=2500,
        duration_days=5,
        travelers=2,
        transport_per_person=6500,
        food_per_person_per_day=500,
        activities_per_person=1200,
        local_transport=3000
    )
)