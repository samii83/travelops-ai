
import json
from pathlib import Path

DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "destinations.json"
)


def load_destinations():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def search_destination(destination: str):

    destinations = load_destinations()

    result = destinations.get(destination)

    # Handle unknown destinations before accessing their data
    if result is None:
        return {
            "found": False,
            "message": f"No information available for {destination}",
            "data_source": "curated_demo_dataset"
        }

    return {
        "found": True,
        "destination": destination,
        "description": result["description"],
        "best_for": result["best_for"],
        "attractions": result["attractions"],
        "estimated_food_per_person_per_day":
            result["estimated_food_per_person_per_day"],
        "estimated_local_transport":
            result["estimated_local_transport_per_trip"],
        "data_source": "curated_demo_dataset"
    }
