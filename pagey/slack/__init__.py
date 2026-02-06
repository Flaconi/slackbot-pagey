"""Slack module."""

from collections.abc import Callable
import re
import time
from typing import Any

from slackclient import SlackClient  # type: ignore


class PageySlack:
    """Pagey Slack Class."""

    RTM_READ_DELAY = 1  # 1 second delay between reading from RTM

    # --------------------------------------------------------------------------
    # Constructor
    # --------------------------------------------------------------------------
    def __init__(self, token: str, command_callback: Callable[[str], str]) -> None:
        """Initialize Slack client and command callback."""
        self._slack = SlackClient(token)
        self._bot_id: str | None = None
        self._command_callback = command_callback

    # --------------------------------------------------------------------------
    # Public Functions
    # --------------------------------------------------------------------------
    def connect(self) -> bool:
        """Connect to Slack and return True on success, otherwise False."""
        if self._slack.rtm_connect(with_team_state=False):
            # Read bot's user ID by calling Web API method `auth.test`.
            auth_response = self._slack.api_call("auth.test")
            self._bot_id = auth_response["user_id"]
            return True
        return False

    def run(self) -> None:
        """Run this Slack bot and endlessly evaluate Slack events."""
        while True:
            command, channel = self._parse_bot_commands(self._slack.rtm_read())
            if command and channel:
                self._handle_command(command, channel)
            time.sleep(self.RTM_READ_DELAY)

    # --------------------------------------------------------------------------
    # Private Functions
    # --------------------------------------------------------------------------
    def _handle_command(self, command: str, channel: str) -> None:
        """Execute a bot command and send the response back to Slack."""
        # The callback will take care of generating the response for Slack.
        response = self._command_callback(command)

        # Send the response back to the channel.
        self._slack.api_call("chat.postMessage", channel=channel, text=response)

    def _parse_bot_commands(
        self,
        slack_events: list[dict[str, Any]],
    ) -> tuple[str | None, str | None]:
        """Parse commands from Slack RTM events.

        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and
        channel. If it's not found, then this function returns (None, None).
        """
        for event in slack_events:
            if event.get("type") == "message" and "subtype" not in event:
                user_id, message = self._parse_direct_mention(event.get("text", ""))
                if user_id == self._bot_id and message is not None:
                    return message, event["channel"]
        return None, None

    @staticmethod
    def _parse_direct_mention(
        message_text: str,
    ) -> tuple[str | None, str | None]:
        """Parse direct mentions from the beginning of a message.

        Finds a direct mention (a mention that is at the beginning) in message
        text and returns the user ID which was mentioned along with the
        remaining message. If there is no direct mention, returns (None, None).
        """
        mention_regex = r"^<@(|[WU].+?)>(.*)"
        matches = re.search(mention_regex, message_text)
        # The first group contains the username, the second group contains the
        # remaining message.
        if not matches:
            return None, None
        return matches.group(1), matches.group(2).strip()
