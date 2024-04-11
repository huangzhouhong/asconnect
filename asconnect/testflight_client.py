"""Wrapper around the Apple App Store Connect APIs."""

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging
from typing import Iterator, List, Optional

from asconnect.httpclient import HttpClient

from asconnect.models import *
from asconnect.utilities import update_query_parameters


class TestflightClient:
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
        self.log = log.getChild("testflight")

    def get_beta_testers(self) -> Iterator[BetaTester]:
        self.log.info("Getting beta testers...")

        url = self.http_client.generate_url("betaTesters")

        query_parameters = {"limit": "200"}

        url = update_query_parameters(url, query_parameters)

        yield from self.http_client.get(url=url, data_type=List[BetaTester])

    def get_beta_testers_by_email(self, email) -> Iterator[BetaTester]:
        self.log.info("Getting beta testers...")
        url = self.http_client.generate_url("betaTesters")
        query_parameters = {"limit": "200", "filter[email]": email}
        url = update_query_parameters(url, query_parameters)
        yield from self.http_client.get(url=url, data_type=List[BetaTester])

    def get_internal_beta_group(self) -> Iterator[BetaTester]:
        url = self.http_client.generate_url("betaGroups")
        query_parameters = {"filter[isInternalGroup]": "true"}
        url = update_query_parameters(url, query_parameters)
        yield from self.http_client.get(url=url, data_type=List[BetaGroup])

    def create_beta_tester(self, *, group_id, email):
        return self.http_client.post(
            endpoint="betaTesters",
            data={
                "data": {
                    "type": "betaTesters",
                    "relationships": {
                        "betaGroups": {
                            "data": [{"id": group_id, "type": "betaGroups"}]
                        },
                    },
                    "attributes": {"email": email}

                }
            },
            data_type=BetaTester,
        )

    def delete_beta_tester(self, identifier):
        url = self.http_client.generate_url(f"betaTesters/{identifier}")
        raw_response = self.http_client.delete(url=url)
        return raw_response.status_code == 202 or raw_response.status_code == 204

    def invite_beta_tester(
            self,
            *,
            app_id: str,
            tester_id: str
    ) -> Optional[BetaTesterInvitation]:
        return self.http_client.post(
            endpoint="betaTesterInvitations",
            data={
                "data": {
                    "type": "betaTesterInvitations",
                    "relationships": {
                        "app": {
                            "data": {"id": app_id, "type": "apps"}
                        },
                        "betaTester": {
                            "data": {"id": tester_id, "type": "betaTesters"}
                        },
                    }
                }
            },
            data_type=BetaTesterInvitation,
        )
