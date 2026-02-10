"""Slack module."""

import logging
import re
from collections.abc import Callable
from typing import Any
from slack_sdk import WebClient
from slack_sdk.rtm_v2 import RTMClient
from slack_sdk.errors import SlackApiError


LOGGER = logging.getLogger(__name__)


class PageySlack:
    """Pagey Slack Class."""

    # --------------------------------------------------------------------------
    # Constructor
    # --------------------------------------------------------------------------
    def __init__(self, token: str, command_callback: Callable[[str], str]) -> None:
        """Initialize Slack client and command callback."""
        self._token = token
        self._slack = WebClient(token=token)
        self._rtm_client = RTMClient(token=token, web_client=self._slack)
        self._bot_id: str | None = None
        self._command_callback = command_callback

    # --------------------------------------------------------------------------
    # Public Functions
    # --------------------------------------------------------------------------
    def connect(self) -> bool:
        """Connect to Slack and return True on success, otherwise False."""
        try:
            # Read bot's user ID by calling Web API method `auth_test`.
            auth_response = self._slack.auth_test()
        except SlackApiError as exc:
            error = exc.response.get("error", "unknown_error")
            LOGGER.error("Slack auth_test failed: %s", error)
            return False

        self._bot_id = auth_response.get("user_id")
        return self._bot_id is not None

    def run(self) -> None:
        """Run this Slack bot and endlessly evaluate Slack events using RTMClient."""

        @self._rtm_client.on("message")
        def _on_message(_: RTMClient, event: dict) -> None:
            channel = event.get("channel")
            text = event.get("text", "")

            if not channel or not text:
                return

            command, _ = self._parse_bot_commands([event])
            if command is not None:
                self._handle_command(command, channel)

        # Start the RTM event loop (blocking call).
        self._rtm_client.start()

    # --------------------------------------------------------------------------
    # Private Functions
    # --------------------------------------------------------------------------
    def _handle_command(self, command: str, channel: str) -> None:
        """Execute a bot command and send the response back to Slack."""
        # The callback will take care of generating the response for Slack.
        response = self._command_callback(command)

        # Send the response back to the channel.
        self._slack.chat_postMessage(channel=channel, text=response)

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
