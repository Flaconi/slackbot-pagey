"""Pagerduty module."""


from typing import List, Dict, Any
from dateutil import parser
import datetime
import json
import sys
import requests


def fetch_schedules(token: str) -> List[Dict[str, Any]]:
    """Fetch oncall schedules from Pagerduty API."""
    url = "https://api.pagerduty.com/oncalls"
    now = datetime.datetime.now()
    data = {}

    for item in __fetch_pagerduty(url, "oncalls", token):
        if item["start"] and item["end"]:
            date_start = parser.parse(item["start"])
            date_end = parser.parse(item["end"])
            if now.timestamp() > date_start.timestamp() and now.timestamp() < date_end.timestamp():
                team_name = item["escalation_policy"]["summary"]
                if team_name not in data:
                    data[team_name] = []
                data[team_name].append(item["user"]["summary"])

    response = ""
    for team, names in data.items():
        response += f"\nteam: {team}\n--------------------------------\n"
        for name in names:
            response += f"* {name}\n"

    return response


def __fetch_pagerduty(url: str, ret_key: str, token: str) -> List[Dict[str, Any]]:
    """Make generic requests against Pagerduty API."""
    headers = {
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Content-Type": "application/json",
        "Authorization": f"Token token={token}",
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
            print(str(url_err), file=sys.stdout)
            break
        except requests.exceptions.HTTPError as http_err:
            print(str(http_err), file=sys.stdout)
            break
        except requests.exceptions.TooManyRedirects as redir_err:
            print(str(redir_err), file=sys.stdout)
            break
        except requests.exceptions.ConnectTimeout as conn_time_err:
            print(str(conn_time_err), file=sys.stdout)
            break
        except requests.exceptions.ReadTimeout as read_time_err:
            print(str(read_time_err), file=sys.stdout)
            break
        except requests.exceptions.Timeout as time_err:
            print(str(time_err), file=sys.stdout)
            break
        except requests.exceptions.ConnectionError as conn_err:
            print(str(conn_err), file=sys.stdout)
            break
        except requests.exceptions.RequestException as req_err:
            print(str(req_err), file=sys.stdout)
            break
    # close response object after done
    # TODO: add try-except
    response.close()

    return data
