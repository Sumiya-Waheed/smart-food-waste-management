from crewai import Agent


def create_matching_agent(llm=None) -> Agent:
    return Agent(
        role="Food Donation Matching Agent",
        goal=(
            "Match suitable food donations to recipient organizations "
            "using deterministic validation and clear reasoning."
        ),
        backstory=(
            "You specialize in food donation matching based on capacity, "
            "compatibility, need, availability, and distance."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )