
import pytest

from backend.tools.budget_calculator import calculate_budget
from backend.tools.destination_search import search_destination
from backend.tools.hotel_search import search_hotels
from backend.tools.transport_search import search_transport


def test_destination_search():
    result = search_destination("Goa")
    assert result["found"] is True


def test_unknown_destination():
    result = search_destination("Unknown City")
    assert result["found"] is False


def test_hotel_search():
    result = search_hotels("Goa", "comfortable")
    assert result["found"] is True
    assert result["hotels"][0]["price_per_night"] == 2500


def test_transport_search():
    result = search_transport("Goa", "Bhubaneswar", 2)
    assert result["estimated_total"] == 13000


def test_missing_transport_route():
    result = search_transport("Goa", "Unknown City", 2)
    assert result["found"] is False


def test_budget_calculation():
    result = calculate_budget(
        hotel_price_per_night=2500,
        duration_days=5,
        travelers=2,
        transport_per_person=6500,
        food_per_person_per_day=500,
        activities_per_person=1250,
        local_transport=3000
    )
    assert result["total_estimated_cost"] == 33500


def test_invalid_duration():
    with pytest.raises(ValueError):
        calculate_budget(
            hotel_price_per_night=2500,
            duration_days=0,
            travelers=2,
            transport_per_person=6500,
            food_per_person_per_day=500,
            activities_per_person=1250
        )
