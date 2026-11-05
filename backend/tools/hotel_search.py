import json
from pathlib import Path


DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "destinations.json"
)


def search_hotels(
    destination: str,
    preference: str = "comfortable"
):

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        destinations = json.load(file)

    destination_data = destinations.get(destination)

    if destination_data is None:
        return {
            "found": False,
            "hotels": []
        }

    hotels = destination_data["hotels"]

    matching_hotels = [
        hotel
        for hotel in hotels
        if hotel["category"].lower() == preference.lower()
    ]

    return {
        "found": len(matching_hotels) > 0,
        "destination": destination,
        "preference": preference,
        "hotels": matching_hotels,
        "data_source": "curated_demo_dataset"
    }