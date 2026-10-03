from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Donation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    donation_id: str = "D001"
    food_name: str
    quantity: float = Field(gt=0)
    unit: str
    category: str
    preparation_time: Optional[str] = None
    available_until: Optional[str] = None
    pickup_location: str
    condition: str
    missing_information: List[str] = Field(default_factory=list)


class RecipientOrganization(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    location: str
    distance_km: float = Field(ge=0)
    capacity: float = Field(gt=0)
    accepted_food_categories: List[str]
    need_level: str
    availability: str

    @field_validator("need_level")
    @classmethod
    def validate_need_level(cls, value: str) -> str:
        value = value.lower().strip()

        if value not in {"low", "medium", "high"}:
            raise ValueError(
                "need_level must be low, medium, or high"
            )

        return value


class InventoryResult(BaseModel):
    donation: Donation
    extracted_information: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    safety_note: str


class MatchResult(BaseModel):
    matched: bool
    recommended_organization: Optional[str] = None
    match_score: float = 0
    match_reason: str
    alternatives: List[str] = Field(default_factory=list)
    validation_warnings: List[str] = Field(default_factory=list)


class LogisticsResult(BaseModel):
    feasible: bool
    pickup_time: str
    delivery_target: str
    priority: str
    collection_instructions: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class CoordinationResult(BaseModel):
    status: str
    donation_summary: str
    recommended_organization: Optional[str] = None
    match_reason: str
    pickup_time: str
    delivery_target: str
    priority: str
    next_action: str
    donor_message: str
    recipient_message: str
    warnings: List[str] = Field(default_factory=list)
    safety_disclaimer: str