import deserialize
import enum
from typing import Dict, List, Optional
from asconnect.models.common import BaseAttributes, Links, Relationship, Resource

class UserRole(enum.Enum):
    """Represents a user role."""

    ACCESS_TO_REPORTS = "ACCESS_TO_REPORTS"
    ACCOUNT_HOLDER = "ACCOUNT_HOLDER"
    ADMIN = "ADMIN"
    APP_MANAGER = "APP_MANAGER"
    CLOUD_MANAGED_APP_DISTRIBUTION = "CLOUD_MANAGED_APP_DISTRIBUTION"
    CLOUD_MANAGED_DEVELOPER_ID = "CLOUD_MANAGED_DEVELOPER_ID"
    CREATE_APPS = "CREATE_APPS"
    CUSTOMER_SUPPORT = "CUSTOMER_SUPPORT"
    DEVELOPER = "DEVELOPER"
    FINANCE = "FINANCE"
    IMAGE_MANAGER = "IMAGE_MANAGER"
    MARKETING = "MARKETING"
    SALES = "SALES"

@deserialize.key("first_name", "firstName")
@deserialize.key("last_name", "lastName")
# @deserialize.key("provisioning_allowed", "provisioningAllowed")
# @deserialize.key("all_apps_visible", "allAppsVisible")
class UserInvitationAttributes(BaseAttributes):
    email: str
    first_name: str
    last_name: str
    roles: List[UserRole]
    expirationDate: str
    # provisioning_allowed: bool
    # all_apps_visible: bool
    # username: str


@deserialize.key("identifier", "id")
class UserInvitation(Resource):
    identifier: str
    attributes: UserInvitationAttributes
    relationships: Optional[Dict[str, Relationship]]
    links: Links
