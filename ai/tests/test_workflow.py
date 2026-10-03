import json
from pathlib import Path

from ai.models.schemas import RecipientOrganization
from ai.workflows.donation_workflow import run_donation_workflow


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = (
    BASE_DIR
    / "ai"
    / "data"
    / "sample_data.json"
)


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def test_donation_workflow():
    data = load_data()

    recipients = [
        RecipientOrganization(**item)
        for item in data["recipients"]
    ]

    donation = data["donations"][0]

    result = run_donation_workflow(
        donation,
        recipients,
    )

    assert result is not None
    assert result.status in {"Coordinated", "No Match"}

    if result.status == "Coordinated":
        assert result.recommended_organization is not None