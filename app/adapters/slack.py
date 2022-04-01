import collections
import hashlib
import hmac
import json
import logging
import re
from typing import Any, Callable, Dict, Optional, Pattern
from urllib.parse import parse_qs

import requests
from pydantic.dataclasses import dataclass

from app import config

logger = logging.getLogger(__name__)
SlackConfig = collections.namedtuple("SlackConfig", "webhook_url")


@dataclass
class SlashCommand:
    """
    https://api.slack.com/interactivity/slash-commands#responding_to_commands
    """

    name: str
    text: Optional[str]
    team_id: str
    team_domain: str
    channel_id: str
    channel_name: str
    user_id: str
    user_name: str
    # A temporary webhook URL that you can use to generate messages responses.
    response_url: str
    trigger_id: str


class SlackAdapter:
    """
    Offers a Slack API integration.

    If you need guidance on how to build message for Slack
    check out Block Kit Builder visiting
    https://app.slack.com/block-kit-builder/.
    """

    def __init__(self, config: SlackConfig):
        self.logger = logging.getLogger(__name__)
        self.config = config

    def post_message(self, message: dict, context: dict):
        """
        Posts the message to to channel configured in the webhook.
        """

        slack_ctx = context.get("slack", {})
        logger.info(slack_ctx)

        url = slack_ctx.get("response_url", self.config.webhook_url)

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(message)

        requests.post(
            # self.config.webhook_url,
            url,
            headers={"Content-type": "application/json"},
            data=json.dumps(message),
        )


@dataclass
class Route:
    id: str
    pattern: Optional[Pattern]
    handler: Callable


class SlashCommandDispatcher:
    def __init__(self):
        self.routes: Dict[str, Route] = {}

    def route(self, id: str, text_regex: Optional[str] = None) -> Callable:
        logger.info(f"adding route {id}")

        def decorator(func: Callable) -> Callable:
            route = Route(
                id=id,
                pattern=re.compile(text_regex) if text_regex else None,
                handler=func,
            )
            self.routes[id] = route
            return route

        return decorator

    def dispatch(self, cmd: SlashCommand, context: Dict[str, Any]):

        if cmd.name not in self.routes:
            logger.error(f"can't find a route for cmd {cmd.name}")
            raise RouteNotFound()

        route = self.routes[cmd.name]

        if route.pattern:
            match = route.pattern.match(cmd.text)
            if not match:
                msg = f"{cmd.text} doesn't match {route.pattern}"
                logger.warning(msg)
                raise RouteNotFound(msg)

            # call the command handler
            args = match.groupdict()
            logger.info(
                f"handing off cmd {cmd.name} to {route.handler}"
                f" with context {context} args {args}"
            )
            route.handler(context, **args)
        else:
            # call the command handler passing the text
            route.handler(context, cmd.text)


def build_slash_command(qs: str) -> SlashCommand:
    """
    Build a new ``SlashCommand`` from a query string, usually sent by Slack
    as a slash command.

        Arguments:

        qs: percent-encoded query string to be parsed
    """

    dictionary = parse_qs(qs)

    # if 'text' in dictionary:
    #     text = dictionary['text'][0] if 'text' in dictionary else None
    # else:
    #     text = None
    text = dictionary["text"][0] if "text" in dictionary else None

    return SlashCommand(
        name=dictionary["command"][0],
        team_id=dictionary["team_id"][0],
        team_domain=dictionary["team_domain"][0],
        channel_id=dictionary["channel_id"][0],
        channel_name=dictionary["channel_name"][0],
        user_id=dictionary["user_id"][0],
        user_name=dictionary["user_name"][0],
        response_url=dictionary["response_url"][0],
        trigger_id=dictionary["trigger_id"][0],
        text=text,
    )


class InvalidSignature(Exception):
    pass


class RouteNotFound(Exception):
    pass


def verify_signature(body: str, headers: Dict[str, str]):
    """
    Verify if the signature of an Slack webhook call.

    Check https://api.slack.com/authentication/verifying-requests-from-slack
    for more details.
    """
    signature = headers.get("X-Slack-Signature", "")
    timestamp = headers.get("X-Slack-Request-Timestamp", "")

    req = str.encode(f"v0:{timestamp}:{body}")

    request_hash = (
        "v0="
        + hmac.new(
            str.encode(config.SLACK_SIGNING_SECRET), req, hashlib.sha256
        ).hexdigest()
    )

    if not hmac.compare_digest(request_hash, signature):
        raise InvalidSignature()
