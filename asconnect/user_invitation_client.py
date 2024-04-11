import logging
from typing import Iterator, List

from asconnect.httpclient import HttpClient

from asconnect.models import UserInvitation
from asconnect.utilities import update_query_parameters


class UsersInvitationClient:
    """Wrapper class around the ASC API."""

    log: logging.Logger
    http_client: HttpClient

    def __init__(
            self,
            *,
            http_client: HttpClient,
            log: logging.Logger,
    ) -> None:
        """Construct a new client object.

        :param http_client: The API HTTP client
        :param log: Any base logger to be used (one will be created if not supplied)
        """

        self.http_client = http_client
        self.log = log.getChild("users invitation")

    def get_users(self) -> Iterator[UserInvitation]:
        """获取邀请中的用户，已接受的不包含在内

        :returns: A list of users
        """

        self.log.info("Getting users...")

        url = self.http_client.generate_url("userInvitations")

        query_parameters = {"limit": "200"}

        url = update_query_parameters(url, query_parameters)

        yield from self.http_client.get(url=url, data_type=List[UserInvitation])

    def get_users_by_email(self, email) -> Iterator[UserInvitation]:
        """获取邀请中的用户，已接受的不包含在内

        :returns: A list of users
        """

        self.log.info("Getting users...")

        url = self.http_client.generate_url("userInvitations")

        query_parameters = {"limit": "200", "filter[email]": email}

        url = update_query_parameters(url, query_parameters)

        yield from self.http_client.get(url=url, data_type=List[UserInvitation])

    def invite_user(
            self,
            *,
            email: str,
            first_name: str = 'unknown',
            last_name: str = 'unknown'
    ) -> UserInvitation:
        return self.http_client.post(
            endpoint="userInvitations",
            data={
                "data": {
                    "type": "userInvitations",
                    "attributes": {
                        "email": email,
                        "firstName": first_name,
                        "lastName": last_name,
                        "roles": ["CUSTOMER_SUPPORT"],
                        "allAppsVisible": True
                    }
                }
            },
            data_type=UserInvitation,
        )

    def canel_invite(self, *, identifier):
        url = self.http_client.generate_url(f"userInvitations/{identifier}")
        raw_response = self.http_client.delete(url=url)
        # if raw_response.status_code != 204:
        #     raise AppStoreConnectError(raw_response)
        return raw_response.status_code == 204
