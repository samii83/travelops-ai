from pydantic import BaseModel, field_validator


class TravelRequest(BaseModel):

    destination: str | None = None
    duration_days: int | None = None
    travelers: int | None = None
    budget: float | None = None
    currency: str = "INR"
    origin: str | None = None
    hotel_preference: str | None = None
    travel_style: str | None = None

    @field_validator("duration_days")
    @classmethod
    def validate_duration(cls, value):
        if value is not None and not 1 <= value <= 60:
            raise ValueError("Duration must be between 1 and 60 days")
        return value

    @field_validator("travelers")
    @classmethod
    def validate_travelers(cls, value):
        if value is not None and not 1 <= value <= 50:
            raise ValueError("Travelers must be between 1 and 50")
        return value

    @field_validator("budget")
    @classmethod
    def validate_budget(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Budget must be positive")
        return value