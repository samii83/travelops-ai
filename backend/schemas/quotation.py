
from pydantic import BaseModel
from typing import Optional


class QuotationItem(BaseModel):
    category: str
    description: str
    amount: float


class TravelQuotation(BaseModel):
    destination: str
    duration_days: int
    travelers: int
    currency: str = "INR"

    hotel_name: str
    items: list[QuotationItem]

    total_estimated_cost: float
    cost_per_person: float
    budget: Optional[float] = None
    remaining_budget: Optional[float] = None

    attractions: list[str]
    assumptions: list[str]
    data_source: str = "curated_demo_dataset"
