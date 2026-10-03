import json
from pathlib import Path

# =========================================================
# CrewAI + Groq compatibility patch
# Groq does not accept CrewAI's cache_breakpoint field.
# =========================================================

try:
    import crewai.llms.cache as crew_cache

    crew_cache.mark_cache_breakpoint = lambda message: message

except Exception:
    pass


from ai.models.schemas import RecipientOrganization
from ai.workflows.donation_workflow import run_donation_workflow


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ai" / "data" / "sample_data.json"


def main():

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    recipients = [
        RecipientOrganization(**item)
        for item in data["recipients"]
    ]

    donation = data["donations"][0]

    print()
    print("=" * 70)
    print("SMART FOOD WASTE MANAGEMENT")
    print("CREWAI MULTI-AGENT AI DEMO")
    print("=" * 70)

    print()
    print("DONATION")
    print("-" * 70)

    print(f"Food: {donation['food_name']}")
    print(
        f"Quantity: "
        f"{donation['quantity']} "
        f"{donation['unit']}"
    )
    print(f"Category: {donation['category']}")
    print(
        f"Pickup: "
        f"{donation['pickup_location']}"
    )
    print(
        f"Available until: "
        f"{donation['available_until']}"
    )
    print(
        f"Condition: "
        f"{donation['condition']}"
    )

    print()
    print("Running multi-agent workflow...")

    try:

        result = run_donation_workflow(
            donation,
            recipients,
        )

        print()
        print("FINAL COORDINATION RESULT")
        print("-" * 70)

        print(
            f"Status: "
            f"{result.status}"
        )

        print(
            "Recommended Organization: "
            f"{result.recommended_organization}"
        )

        print(
            f"Match Reason: "
            f"{result.match_reason}"
        )

        print(
            f"Pickup Time: "
            f"{result.pickup_time}"
        )

        print(
            f"Delivery Target: "
            f"{result.delivery_target}"
        )

        print(
            f"Priority: "
            f"{result.priority}"
        )

        print(
            f"Next Action: "
            f"{result.next_action}"
        )

        print()
        print("DONOR MESSAGE")
        print("-" * 70)
        print(result.donor_message)

        print()
        print("RECIPIENT MESSAGE")
        print("-" * 70)
        print(result.recipient_message)

        if result.warnings:

            print()
            print("WARNINGS")
            print("-" * 70)

            for warning in result.warnings:
                print(f"- {warning}")

        print()
        print("JSON RESULT")
        print("-" * 70)

        print(
            result.model_dump_json(
                indent=2
            )
        )

    except Exception as exc:

        print()
        print("ERROR")
        print("-" * 70)
        print(str(exc))


if __name__ == "__main__":
    main()