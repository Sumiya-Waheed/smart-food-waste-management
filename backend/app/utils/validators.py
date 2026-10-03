from datetime import datetime, timezone


def is_donation_expired(deadline: datetime) -> bool:
    """
    Return True if the safe-consumption deadline has passed.
    """
    now = datetime.now(timezone.utc)

    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)

    return deadline <= now


def validate_positive_quantity(quantity: float) -> None:
    """
    Ensure a quantity is greater than zero.
    """
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")


def validate_requested_quantity(
    requested_quantity: float,
    remaining_quantity: float,
) -> None:
    """
    Ensure the requested quantity is positive
    and does not exceed the remaining donation quantity.
    """
    validate_positive_quantity(requested_quantity)

    if requested_quantity > remaining_quantity:
        raise ValueError(
            "Requested quantity exceeds the remaining donation quantity."
        )


def validate_status_transition(
    current_status: str,
    new_status: str,
    allowed_transitions: dict[str, list[str]],
) -> None:
    """
    Validate whether a status transition is allowed.
    """
    allowed_statuses = allowed_transitions.get(current_status, [])

    if new_status not in allowed_statuses:
        raise ValueError(
            f"Invalid status transition: "
            f"{current_status} -> {new_status}"
        )