"""Main file for pagey."""

import os

from .args import *
from .pagerduty import *
from .slack import *


def main() -> None:
    """Run main entrypoint."""
    get_args()

    try:
        SLACK_TOKEN = os.environ["PAGEY_SLACK_TOKEN"]
    except KeyError:
        print("Error, env variable 'PAGEY_SLACK_TOKEN' not set", file=sys.stdout)
        sys.exit(1)
    try:
        PD_TOKEN = os.environ["PAGEY_PD_TOKEN"]
    except KeyError:
        print("Error, env variable 'PAGEY_PD_TOKEN' not set", file=sys.stdout)
        sys.exit(1)

    # Initialize pagerduty
    # Get schedules
    schedules = fetch_schedules(PD_TOKEN)
    response = ""
    print(schedules)
    for team, users in schedules.items():
        response += f"*{team}*\n"
        # Sort by escalation level
        users.sort(key=lambda s: s["level"])
        for user in users:
            response += f"* [lvl: *{user['level']}* -> {user['until']}] {user['name']}\n"
        response += "\n"

    # Slack command callback
    def commandCallback(command: str) -> str:
        """This is a callback function for slack to evaluate response based on given command."""
        if command.startswith("oncall"):
            return response
        return "Available commands: oncall"

    # Connect to Slack (RTM)
    slack = PageySlack(SLACK_TOKEN, commandCallback)
    if not slack.connect():
        print("Connection to Slack failed. Exception traceback printed above.", file=sys.stderr)
        sys.exit(1)
    print("Pagey connected to Slack and running!")
    slack.run()


if __name__ == "__main__":
    main()
