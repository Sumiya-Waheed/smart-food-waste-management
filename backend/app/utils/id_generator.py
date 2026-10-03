import uuid


def generate_id(prefix: str) -> str:
    """
    Generate a unique ID with a readable prefix.

    Example:
        generate_id("ORG") -> ORG-a1b2c3d4
    """
    unique_part = uuid.uuid4().hex[:8]
    return f"{prefix}-{unique_part}"