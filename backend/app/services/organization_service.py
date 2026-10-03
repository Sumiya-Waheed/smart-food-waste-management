from datetime import datetime, timezone

from app.data.store import organizations
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate
from app.utils.id_generator import generate_id


class OrganizationService:

    @staticmethod
    def create_organization(
        data: OrganizationCreate,
    ) -> Organization:
        organization = Organization(
            id=generate_id("ORG"),
            **data.model_dump(),
        )

        organizations[organization.id] = organization

        return organization

    @staticmethod
    def get_organization(
        organization_id: str,
    ) -> Organization:
        organization = organizations.get(organization_id)

        if organization is None:
            raise ValueError("Organization not found.")

        return organization

    @staticmethod
    def list_organizations() -> list[Organization]:
        return list(organizations.values())

    @staticmethod
    def activate_organization(
        organization_id: str,
    ) -> Organization:
        organization = OrganizationService.get_organization(
            organization_id
        )

        organization.is_active = True
        organization.updated_at = datetime.now(timezone.utc)

        return organization

    @staticmethod
    def deactivate_organization(
        organization_id: str,
    ) -> Organization:
        organization = OrganizationService.get_organization(
            organization_id
        )

        organization.is_active = False
        organization.updated_at = datetime.now(timezone.utc)

        return organization