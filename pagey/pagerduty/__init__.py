"""Pagerduty module."""

import datetime
import json
import logging
from typing import Any

from dateutil import parser
import requests


LOGGER = logging.getLogger(__name__)


class PageyPD:
    """Pagey PagerDuty Class."""

    # --------------------------------------------------------------------------
    # Constructor
    # --------------------------------------------------------------------------
    def __init__(self, token: str) -> None:
        self.__token = token

    # --------------------------------------------------------------------------
    # Public Functions
    # --------------------------------------------------------------------------
    def get_schedules(self) -> dict[str, Any]:
        """Fetch oncall schedules from Pagerduty API."""
        url = "https://api.pagerduty.com/oncalls"
        now = datetime.datetime.now()
        data: dict[str, Any] = {}

        for item in self.__get_api_response(url, "oncalls"):
            if item["start"] and item["end"]:
                date_start = parser.parse(item["start"])
                date_end = parser.parse(item["end"])
                if (
                    now.timestamp() > date_start.timestamp()
                    and now.timestamp() < date_end.timestamp()
                ):
                    team_name = item["escalation_policy"]["summary"]
                    if team_name not in data:
                        data[team_name] = []
                    data[team_name].append(
                        {
                            "name": item["user"]["summary"],
                            "level": item["escalation_level"],
                            "until": f"{date_end:%Y-%m-%d}",
                        }
                    )
        return data

    # --------------------------------------------------------------------------
    # Private Functions
    # --------------------------------------------------------------------------
    def __get_api_response(self, url: str, ret_key: str) -> list[dict[str, Any]]:
        """Make generic GET requests against Pagerduty API and return its response.

        Args:
            url: API URL to request against.
            ret_key: The top-level JSON key for which to return its children.

        Returns:
            A list of response dicts.
        """
        # Required request headers for PD APIv2
        headers = {
            "Accept": "application/vnd.pagerduty+json;version=2",
            "Content-Type": "application/json",
            "Authorization": f"Token token={self.__token}",
        }
        limit = 20
        offset = 0
        data: list[dict[str, Any]] = []

        response: requests.Response | None = None
        try:
            while True:
                params: dict[str, Any] = {
                    "limit": limit,
                    "offset": offset,
                }
                response = requests.request(
                    "GET",
                    url,
                    params=params,
                    headers=headers,
                    timeout=30,
                )
                response.raise_for_status()

                val = json.loads(response.content.decode("utf-8"))
                data.extend(val.get(ret_key, []))

                # Do we paginate?
                if val.get("more"):
                    offset += limit
                    continue
                break

        except requests.exceptions.RequestException:
            LOGGER.exception("PagerDuty API request failed")
        finally:
            if response is not None:
                response.close()

        return data
