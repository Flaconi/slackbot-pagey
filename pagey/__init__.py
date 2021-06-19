"""Main file for pagey."""

import os

from .args import *
from .pagerduty import *
from .defaults import DEF_NAME, DEF_DESC, DEF_VERSION, DEF_GITHUB
from .slack import *

COMMANDS = ["oncall", "info"]


def main() -> None:
    """Run main entrypoint."""
    # Parse command line arguments
    get_args()

    # Ensure environment tokens are present
    try:
        SLACK_TOKEN = os.environ["PAGEY_SLACK_TOKEN"]
    except KeyError:
        print("Error, env variable 'PAGEY_SLACK_TOKEN' not set", file=sys.stderr)
        sys.exit(1)
    try:
        PD_TOKEN = os.environ["PAGEY_PD_TOKEN"]
    except KeyError:
        print("Error, env variable 'PAGEY_PD_TOKEN' not set", file=sys.stderr)
        sys.exit(1)

    # Initialize Pagerduty module
    pagerduty = PageyPD(PD_TOKEN)

    def commandCallback(command: str) -> str:
        """This is a callback function for Slack to evaluate response based on given command.

        Args:
            command (str): the command/message after the bot mention (e.g.: @pagey <command>).

        Returns:
            str: The reply to be sent to Slack.
        """
        # [Command: oncall] Get Pagerduty schedules
        if command.startswith("oncall"):
            schedules = pagerduty.get_schedules()
            response = ""
            for team, users in schedules.items():
                response += f"*{team}*\n"
                # Sort by escalation level
                users.sort(key=lambda s: s["level"])
                for user in users:
                    if int(user["level"]) == 1:
                        response += (
                            f"* [lvl: *{user['level']}* -> {user['until']}] *{user['name']}*\n"
                        )
                    else:
                        response += (
                            f"* [lvl: *{user['level']}* -> {user['until']}] {user['name']}\n"
                        )
                response += "\n"
            return response
        # [Command: info] Report some info
        if command.startswith("info"):
            return f"{DEF_NAME} ({DEF_VERSION}) - {DEF_DESC}\nFind me here: {DEF_GITHUB}\n"

        return "Available commands: " + ", ".join(COMMANDS)

    # Connect to Slack (RTM mode)
    slack = PageySlack(SLACK_TOKEN, commandCallback)
    if not slack.connect():
        print("Connection to Slack failed. Exception traceback printed above.", file=sys.stderr)
        sys.exit(1)
    print("Pagey connected to Slack and running!")
    slack.run()


if __name__ == "__main__":
    main()
