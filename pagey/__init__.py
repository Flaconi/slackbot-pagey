"""Main file for pagey."""

import os
import sys

from .args import get_args
from .defaults import DEF_DESC, DEF_GITHUB, DEF_NAME, DEF_VERSION
from .pagerduty import PageyPD
from .slack import PageySlack

COMMANDS = ["oncall", "info"]


def main() -> None:
    """Run main entrypoint."""
    # Parse command line arguments
    get_args()

    # Ensure environment tokens are present
    try:
        slack_token = os.environ["PAGEY_SLACK_TOKEN"]
    except KeyError:
        print("Error, env variable 'PAGEY_SLACK_TOKEN' not set", file=sys.stderr)
        sys.exit(1)
    try:
        pd_token = os.environ["PAGEY_PD_TOKEN"]
    except KeyError:
        print("Error, env variable 'PAGEY_PD_TOKEN' not set", file=sys.stderr)
        sys.exit(1)

    # Initialize Pagerduty module
    pagerduty = PageyPD(pd_token)

    def command_callback(command: str) -> str:
        """Callback for Slack to evaluate response based on the given command.

        Args:
            command: The command/message after the bot mention (e.g.: @pagey <command>).

        Returns:
            The reply to be sent to Slack.
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
    slack = PageySlack(slack_token, command_callback)
    if not slack.connect():
        print(
            "Connection to Slack failed. Exception traceback printed above.",
            file=sys.stderr,
        )
        sys.exit(1)
    print("Pagey connected to Slack and running!")
    slack.run()


if __name__ == "__main__":
    main()
