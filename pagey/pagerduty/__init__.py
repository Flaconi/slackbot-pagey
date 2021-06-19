"""Pagerduty module."""

from typing import List, Dict, Any
import datetime
import json
import sys

from dateutil import parser
import requests


class PageyPD:
    """Pagey PagerDuty Class."""

    # --------------------------------------------------------------------------
    # Contrcutor
    # --------------------------------------------------------------------------
    def __init__(self, token: str) -> None:
        self.__token = token

    # --------------------------------------------------------------------------
    # Public Functions
    # --------------------------------------------------------------------------
    def get_schedules(self) -> Dict[str, Any]:
        """Fetch oncall schedules from Pagerduty API."""
        url = "https://api.pagerduty.com/oncalls"
        now = datetime.datetime.now()
        data = {}  # type: Dict[str, Any]

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
    def __get_api_response(self, url: str, ret_key: str) -> List[Dict[str, Any]]:
        """Make generic GET requests against Pagerduty API and return its response.

        Args:
            url (str): API URL to request against.
            ret_key (str): The top-level JSON key for which to return its childs.

        Returns:
            list: Returns list of response dicts.
        """
        # Required request headers for PD APIv2
        headers = {
            "Accept": "application/vnd.pagerduty+json;version=2",
            "Content-Type": "application/json",
            "Authorization": f"Token token={self.__token}",
        }
        params = {}
        limit = 20
        offset = 0
        data = []  # type: List[Dict[str, Any]]

        while True:
            params = {
                "limit": limit,
                "offset": offset,
            }
            try:
                response = requests.request(
                    "GET",
                    url,
                    params=params,
                    headers=headers,
                    timeout=30,
                )
                val = json.loads(response.content.decode("utf-8"))
                data = data + val[ret_key]  # concatenate result list
                # Do we paginate?
                if val["more"]:
                    offset += limit
                    continue
                break
            except requests.exceptions.URLRequired as url_err:
                print(str(url_err), file=sys.stderr)
                break
            except requests.exceptions.HTTPError as http_err:
                print(str(http_err), file=sys.stderr)
                break
            except requests.exceptions.TooManyRedirects as redir_err:
                print(str(redir_err), file=sys.stderr)
                break
            except requests.exceptions.ConnectTimeout as conn_time_err:
                print(str(conn_time_err), file=sys.stderr)
                break
            except requests.exceptions.ReadTimeout as read_time_err:
                print(str(read_time_err), file=sys.stderr)
                break
            except requests.exceptions.Timeout as time_err:
                print(str(time_err), file=sys.stderr)
                break
            except requests.exceptions.ConnectionError as conn_err:
                print(str(conn_err), file=sys.stderr)
                break
            except requests.exceptions.RequestException as req_err:
                print(str(req_err), file=sys.stderr)
                break
        # close response object after done
        # TODO: add try-except
        response.close()

        return data
