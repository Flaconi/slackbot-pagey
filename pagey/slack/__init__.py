"""Slack module."""

from typing import Tuple, Optional, List, Dict, Any, Callable
import time
import re
import sys

from slackclient import SlackClient  # type: ignore


class PageySlack:
    """Pagey Slack Class."""

    RTM_READ_DELAY = 1  # 1 second delay between reading from RTM

    # --------------------------------------------------------------------------
    # Contrcutor
    # --------------------------------------------------------------------------
    def __init__(self, token: str, commandCallback: Callable[[str], str]) -> None:
        """Constructor."""
        self.__slack = SlackClient(token)
        self.__bot_id = None
        self.__commandCallback = commandCallback

    # --------------------------------------------------------------------------
    # Public Functions
    # --------------------------------------------------------------------------
    def connect(self) -> bool:
        """Connect to Slack and return True on success, otherwise False."""
        if self.__slack.rtm_connect(with_team_state=False):
            # Read bot's user ID by calling Web API method `auth.test`
            self.__bot_id = self.__slack.api_call("auth.test")["user_id"]
            return True
        return False

    def run(self) -> bool:
        """Run this Slack bot and wait endlessly to evaluate Slack events."""
        while True:
            command, channel = self.__parse_bot_commands(self.__slack.rtm_read())
            if command:
                self.__handle_command(command, channel)
            time.sleep(self.RTM_READ_DELAY)

    # --------------------------------------------------------------------------
    # Private Functions
    # --------------------------------------------------------------------------
    def __handle_command(self, command: str, channel: Optional[str]) -> None:
        """Executes bot command if the command is known."""
        # The callback will take care about setting the response for slack
        response = self.__commandCallback(command)

        # Sends the response back to the channel
        self.__slack.api_call("chat.postMessage", channel=channel, text=response)

    def __parse_bot_commands(
        self, slack_events: List[Dict[str, Any]]
    ) -> Tuple[Optional[str], Optional[str]]:
        """Parse commands.

        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event["type"] == "message" and "subtype" not in event:
                user_id, message = PageySlack.__parse_direct_mention(event["text"])
                if user_id == self.__bot_id:
                    return message, event["channel"]
        return None, None

    @staticmethod
    def __parse_direct_mention(message_text: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse mentions.

        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        mention_regex = "^<@(|[WU].+?)>(.*)"
        matches = re.search(mention_regex, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)
