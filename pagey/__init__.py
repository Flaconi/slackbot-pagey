"""Main file for pagey."""

import logging
import os
import sys

from .args import get_args
from .defaults import DEF_DESC, DEF_GITHUB, DEF_NAME, DEF_VERSION
from .logging_config import configure_logging
from .pagerduty import PageyPD
from .slack import PageySlack

COMMANDS = ["oncall", "info"]


LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Run main entrypoint."""
    configure_logging()

    # Parse command line arguments
    get_args()

    # Ensure environment tokens are present
    try:
        slack_token = os.environ["PAGEY_SLACK_TOKEN"]
    except KeyError:
        LOGGER.error("Env variable PAGEY_SLACK_TOKEN is not set")
        sys.exit(1)

    try:
        pd_token = os.environ["PAGEY_PD_TOKEN"]
    except KeyError:
        LOGGER.error("Env variable PAGEY_PD_TOKEN is not set")
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
    pagey = PageySlack(slack_token, command_callback)
    if not pagey.connect():
        LOGGER.error("Connection to Slack failed")
        sys.exit(1)

    LOGGER.info("Pagey connected to Slack and running!")

    try:
        pagey.run()
    except KeyboardInterrupt:
        LOGGER.info("Pagey Slack bot stopped by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
