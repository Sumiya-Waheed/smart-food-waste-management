from __future__ import annotations

import json
import os
from typing import List

from dotenv import load_dotenv
from crewai import Crew, LLM, Process, Task

from ai.agents import (
    create_coordinator_agent,
    create_inventory_agent,
    create_logistics_agent,
    create_matching_agent,
)
from ai.models.schemas import (
    CoordinationResult,
    Donation,
    InventoryResult,
    LogisticsResult,
    MatchResult,
    RecipientOrganization,
)
from ai.prompts.prompts import (
    COORDINATOR_AGENT_PROMPT,
    INVENTORY_AGENT_PROMPT,
    LOGISTICS_AGENT_PROMPT,
    MATCHING_AGENT_PROMPT,
)

load_dotenv()


# =========================================================
# DETERMINISTIC MATCHING
# =========================================================

def calculate_match_score(
    donation: Donation,
    recipient: RecipientOrganization,
) -> float:

    score = 0.0

    need_scores = {
        "low": 10,
        "medium": 20,
        "high": 30,
    }

    score += need_scores.get(
        recipient.need_level.lower(),
        0,
    )

    if recipient.distance_km <= 3:
        score += 30
    elif recipient.distance_km <= 5:
        score += 20
    elif recipient.distance_km <= 10:
        score += 10

    if recipient.capacity >= donation.quantity:
        score += 25

    if recipient.availability.lower() == "available":
        score += 15

    return score


def deterministic_match(
    donation: Donation,
    recipients: List[RecipientOrganization],
) -> tuple[
    List[RecipientOrganization],
    List[str],
]:

    eligible = []
    warnings = []

    for recipient in recipients:

        category_match = any(
            category.lower().strip()
            == donation.category.lower().strip()
            for category in recipient.accepted_food_categories
        )

        if not category_match:
            continue

        if recipient.capacity < donation.quantity:
            continue

        if recipient.availability.lower().strip() != "available":
            continue

        eligible.append(recipient)

    if not eligible:
        warnings.append(
            "No recipient organization passed deterministic eligibility checks."
        )

    return eligible, warnings


# =========================================================
# DEMO / DETERMINISTIC RESULTS
# =========================================================

def demo_inventory_result(
    donation_data: dict,
) -> InventoryResult:

    donation = Donation(**donation_data)

    extracted = [
        f"Food name: {donation.food_name}",
        f"Quantity: {donation.quantity} {donation.unit}",
        f"Category: {donation.category}",
        f"Preparation time: {donation.preparation_time}",
        f"Available until: {donation.available_until}",
        f"Pickup location: {donation.pickup_location}",
        f"Condition: {donation.condition}",
    ]

    missing = []

    if not donation.preparation_time:
        missing.append("Preparation time")

    if not donation.available_until:
        missing.append("Available-until time")

    return InventoryResult(
        donation=donation,
        extracted_information=extracted,
        missing_information=missing,
        safety_note=(
            "Food safety is not legally or medically certified by the system. "
            "Final acceptance and safety decisions remain with responsible humans."
        ),
    )


def demo_match_result(
    donation: Donation,
    recipients: List[RecipientOrganization],
) -> MatchResult:

    eligible, warnings = deterministic_match(
        donation,
        recipients,
    )

    if not eligible:
        return MatchResult(
            matched=False,
            recommended_organization=None,
            match_score=0,
            match_reason=(
                "No recipient passed the deterministic eligibility checks."
            ),
            alternatives=[],
            validation_warnings=warnings,
        )

    ranked = sorted(
        eligible,
        key=lambda r: calculate_match_score(
            donation,
            r,
        ),
        reverse=True,
    )

    best = ranked[0]

    alternatives = [
        recipient.name
        for recipient in ranked[1:]
    ]

    score = calculate_match_score(
        donation,
        best,
    )

    reason = (
        f"{best.name} is eligible because it accepts "
        f"{donation.category}, has capacity for "
        f"{donation.quantity} {donation.unit}, is currently "
        f"available, has {best.need_level} need, and is "
        f"approximately {best.distance_km} km from the pickup location."
    )

    return MatchResult(
        matched=True,
        recommended_organization=best.name,
        match_score=score,
        match_reason=reason,
        alternatives=alternatives,
        validation_warnings=warnings,
    )


def demo_logistics_result(
    donation: Donation,
    match: MatchResult,
    recipients: List[RecipientOrganization],
) -> LogisticsResult:

    if not match.matched:
        return LogisticsResult(
            feasible=False,
            pickup_time="Not scheduled",
            delivery_target="No recipient selected",
            priority="High",
            collection_instructions=[],
            warnings=[
                "Logistics cannot be finalized without a recipient."
            ],
        )

    recipient = next(
        r
        for r in recipients
        if r.name == match.recommended_organization
    )

    pickup_time = "As soon as possible"

    if donation.available_until:
        pickup_time = (
            "Pickup as soon as practical before the donation's "
            f"availability deadline of {donation.available_until}."
        )

    priority = "High"

    instructions = [
        f"Collect the donation from {donation.pickup_location}.",
        f"Deliver to {recipient.name} in {recipient.location}.",
        f"Supplied distance: approximately {recipient.distance_km} km.",
        "Keep the responsible coordinator informed of collection status.",
    ]

    warnings = [
        "Distance is a supplied demo value; no live routing or traffic data is used.",
        "Responsible humans must confirm final food acceptance and safety.",
    ]

    return LogisticsResult(
        feasible=True,
        pickup_time=pickup_time,
        delivery_target=(
            f"{recipient.name}, {recipient.location}"
        ),
        priority=priority,
        collection_instructions=instructions,
        warnings=warnings,
    )


def demo_coordination_result(
    donation: Donation,
    match: MatchResult,
    logistics: LogisticsResult,
) -> CoordinationResult:

    if match.matched:
        status = "Coordinated"

        next_action = (
            f"Contact {match.recommended_organization} "
            "and arrange collection."
        )

    else:
        status = "No Match"

        next_action = (
            "Review the donation and recipient list "
            "for another eligible option."
        )

    summary = (
        f"{donation.quantity} {donation.unit} of "
        f"{donation.food_name} are available for donation "
        f"from {donation.pickup_location}."
    )

    donor_message = (
        f"Your donation of {donation.quantity} "
        f"{donation.unit} of {donation.food_name} has been "
        f"processed. Recommended recipient: "
        f"{match.recommended_organization or 'None'}."
    )

    recipient_message = (
        f"A donation of {donation.quantity} "
        f"{donation.unit} of {donation.food_name} is proposed "
        "for your organization. Please confirm acceptance "
        "and collection arrangements."
    )

    warnings = list(
        match.validation_warnings
    )

    warnings.extend(
        logistics.warnings
    )

    return CoordinationResult(
        status=status,
        donation_summary=summary,
        recommended_organization=(
            match.recommended_organization
        ),
        match_reason=match.match_reason,
        pickup_time=logistics.pickup_time,
        delivery_target=logistics.delivery_target,
        priority=logistics.priority,
        next_action=next_action,
        donor_message=donor_message,
        recipient_message=recipient_message,
        warnings=list(dict.fromkeys(warnings)),
        safety_disclaimer=(
            "This system does not legally or medically certify "
            "food safety. Final food acceptance and safety "
            "decisions remain with responsible humans."
        ),
    )


# =========================================================
# GROQ LLM
# =========================================================

def create_groq_llm():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to your .env file."
        )

    return LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=api_key,
        temperature=0.1,
    )


# =========================================================
# REAL CREWAI WORKFLOW
# =========================================================

def run_real_crewai_workflow(
    donation_data: dict,
    recipients: List[RecipientOrganization],
) -> CoordinationResult:

    llm = create_groq_llm()

    inventory_agent = create_inventory_agent(llm)
    matching_agent = create_matching_agent(llm)
    logistics_agent = create_logistics_agent(llm)
    coordinator_agent = create_coordinator_agent(llm)

    donation = Donation(**donation_data)

    donation_json = json.dumps(
        donation_data,
        indent=2,
    )

    recipients_json = json.dumps(
        [
            recipient.model_dump()
            for recipient in recipients
        ],
        indent=2,
    )

    # ---------------------------------------------------------
    # DETERMINISTIC MATCHING
    # ---------------------------------------------------------

    eligible, validation_warnings = deterministic_match(
        donation,
        recipients,
    )

    ranked = sorted(
        eligible,
        key=lambda r: calculate_match_score(
            donation,
            r,
        ),
        reverse=True,
    )

    deterministic_match_data = {
        "eligible": [
            r.model_dump()
            for r in ranked
        ],
        "validation_warnings": validation_warnings,
    }

    # ---------------------------------------------------------
    # TASK 1 — INVENTORY AGENT
    # ---------------------------------------------------------

    inventory_task = Task(
        description=f"""
{INVENTORY_AGENT_PROMPT}

Raw donation:

{donation_json}

Explain the extracted donation information in concise text.

Do NOT use tools.
Do NOT return XML.
Do NOT create a function call.

Keep the response short.
""",
        expected_output=(
            "A concise explanation of the extracted donation "
            "information and any missing information."
        ),
        agent=inventory_agent,
    )

    # ---------------------------------------------------------
    # TASK 2 — MATCHING AGENT
    # ---------------------------------------------------------

    matching_task = Task(
        description=f"""
{MATCHING_AGENT_PROMPT}

Donation:

{donation_json}

Recipients:

{recipients_json}

Authoritative deterministic matching result:

{json.dumps(deterministic_match_data, indent=2)}

Explain why the highest-ranked eligible organization "
"is suitable.

Do NOT change the deterministic result.
Do NOT use tools.
Do NOT return a function call.

Keep the response concise.
""",
        expected_output=(
            "A concise explanation of the deterministic "
            "matching result."
        ),
        agent=matching_agent,
        context=[inventory_task],
    )

    # ---------------------------------------------------------
    # TASK 3 — LOGISTICS AGENT
    # ---------------------------------------------------------

    logistics_task = Task(
        description=f"""
{LOGISTICS_AGENT_PROMPT}

Donation:

{donation_json}

Recipient information:

{json.dumps(
    [r.model_dump() for r in ranked],
    indent=2,
)}

Create a concise logistics proposal.

Do NOT use tools.
Do NOT return a function call.
Do not invent traffic or live routing information.
""",
        expected_output=(
            "A concise pickup and delivery logistics proposal."
        ),
        agent=logistics_agent,
        context=[
            inventory_task,
            matching_task,
        ],
    )

    # ---------------------------------------------------------
    # TASK 4 — COORDINATOR AGENT
    # ---------------------------------------------------------

    coordinator_task = Task(
        description=f"""
{COORDINATOR_AGENT_PROMPT}

Donation:

{donation_json}

The deterministic match is:

{json.dumps(deterministic_match_data, indent=2)}

Combine the previous agent outputs into a concise
final coordination summary.

Do NOT use tools.
Do NOT return a function call.

Focus on:
- recommended organization
- match reason
- pickup
- delivery
- priority
- next action
- warnings
""",
        expected_output=(
            "A concise final coordination summary "
            "combining the four agent outputs."
        ),
        agent=coordinator_agent,
        context=[
            inventory_task,
            matching_task,
            logistics_task,
        ],
    )

    # ---------------------------------------------------------
    # CREW
    # ---------------------------------------------------------

    crew = Crew(
        agents=[
            inventory_agent,
            matching_agent,
            logistics_agent,
            coordinator_agent,
        ],
        tasks=[
            inventory_task,
            matching_task,
            logistics_task,
            coordinator_task,
        ],
        process=Process.sequential,
        verbose=False,
    )

    crew.kickoff()

    # ---------------------------------------------------------
    # PYTHON REMAINS THE SOURCE OF TRUTH
    # ---------------------------------------------------------

    inventory = demo_inventory_result(
        donation_data
    )

    match = demo_match_result(
        inventory.donation,
        recipients,
    )

    logistics = demo_logistics_result(
        inventory.donation,
        match,
        recipients,
    )

    final_result = demo_coordination_result(
        inventory.donation,
        match,
        logistics,
    )

    return final_result


# =========================================================
# PUBLIC WORKFLOW
# =========================================================

def run_donation_workflow(
    donation_data: dict,
    recipients: List[RecipientOrganization],
) -> CoordinationResult:

    demo_mode = (
        os.getenv(
            "DEMO_MODE",
            "true",
        ).lower()
        == "true"
    )

    donation = Donation(**donation_data)

    if demo_mode:

        inventory = demo_inventory_result(
            donation_data
        )

        match = demo_match_result(
            inventory.donation,
            recipients,
        )

        logistics = demo_logistics_result(
            inventory.donation,
            match,
            recipients,
        )

        return demo_coordination_result(
            inventory.donation,
            match,
            logistics,
        )

    return run_real_crewai_workflow(
        donation_data,
        recipients,
    )