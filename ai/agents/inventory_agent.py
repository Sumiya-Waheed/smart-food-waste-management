from crewai import Agent


def create_inventory_agent(llm=None) -> Agent:
    return Agent(
        role="Food Inventory Agent",
        goal=(
            "Extract accurate structured donation information "
            "without inventing missing information."
        ),
        backstory=(
            "You specialize in converting raw food donation information "
            "into reliable structured inventory data."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )