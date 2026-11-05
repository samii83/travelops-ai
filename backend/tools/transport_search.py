import json
from pathlib import Path


DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "destinations.json"
)


def search_transport(
    destination: str,
    origin: str,
    travelers: int
):

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        destinations = json.load(file)

    destination_data = destinations.get(destination)

    if destination_data is None:
        return {
            "found": False,
            "message": "Destination not found"
        }

    transport = destination_data["estimated_transport"]

    price = transport.get(origin)

    if price is None:
        return {
            "found": False,
            "message": f"No transport estimate available from {origin}"
        }

    return {
        "found": True,
        "origin": origin,
        "destination": destination,
        "estimated_round_trip_per_person": price,
        "travelers": travelers,
        "estimated_total": price * travelers,
        "currency": "INR",
        "data_source": "curated_demo_dataset"
    }