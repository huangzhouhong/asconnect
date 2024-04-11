import deserialize
from typing import Dict, Optional

from asconnect.models import Reprable


@deserialize.key("identifier", "id")
class BetaTesterInvitation(Reprable):
    identifier: str
    type: str


@deserialize.key("resource_type", "type")
class BetaTesterInvitationResponse(Reprable):
    data: BetaTesterInvitation
    # links: DocumentLinks


class BetaTesterAttributes(Reprable):
    email: str


@deserialize.key("identifier", "id")
class BetaTester(Reprable):
    identifier: str
    attributes: BetaTesterAttributes


@deserialize.key("identifier", "id")
class BetaGroup(Reprable):
    identifier: str
    # 暂时就一个内部测试，其他属性不需要
