from crewai import Agent


def create_coordinator_agent(llm=None) -> Agent:
    return Agent(
        role="Donation Coordinator Agent",
        goal=(
            "Combine inventory, matching, and logistics information "
            "into one final coordination result."
        ),
        backstory=(
            "You are the final coordination layer of a smart food "
            "waste management system."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )