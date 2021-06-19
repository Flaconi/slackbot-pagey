"""Main file for pagey."""

import os

from .args import *
from .pagerduty import *
from .slack import *


def main() -> None:
    """Run main entrypoint."""
    # Parse command line arguments
    get_args()

    # Ensure environment tokens are present
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

    # Slack command callback
    # Add more commands into the if condition when required.
    def commandCallback(command: str) -> str:
        """This is a callback function for slack to evaluate response based on given command."""
        # [Command: oncall] Get Pagerduty schedules
        if command.startswith("oncall"):
            schedules = fetch_schedules(PD_TOKEN)
            response = ""
            for team, users in schedules.items():
                response += f"*{team}*\n"
                # Sort by escalation level
                users.sort(key=lambda s: s["level"])
                for user in users:
                    response += f"* [lvl: *{user['level']}* -> {user['until']}] {user['name']}\n"
                response += "\n"
            return response
        return "Available commands: oncall"

    # Connect to Slack (RTM mode)
    slack = PageySlack(SLACK_TOKEN, commandCallback)
    if not slack.connect():
        print("Connection to Slack failed. Exception traceback printed above.", file=sys.stderr)
        sys.exit(1)
    print("Pagey connected to Slack and running!")
    slack.run()


if __name__ == "__main__":
    main()
