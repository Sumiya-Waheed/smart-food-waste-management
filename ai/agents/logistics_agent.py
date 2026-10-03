from crewai import Agent


def create_logistics_agent(llm=None) -> Agent:
    return Agent(
        role="Food Donation Logistics Agent",
        goal=(
            "Create a practical pickup and delivery proposal "
            "using supplied donation and recipient information."
        ),
        backstory=(
            "You specialize in coordinating food collection and delivery "
            "under time constraints."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )