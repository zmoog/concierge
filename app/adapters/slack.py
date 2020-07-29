import collections
import hashlib
import hmac
import logging
import json
import re
import requests

from typing import Callable, Dict, Optional, Pattern

from urllib.parse import parse_qs
from pydantic.dataclasses import dataclass
from app import config

logger = logging.getLogger(__name__)
SlackConfig = collections.namedtuple("SlackConfig", "webhook_url")


@dataclass
class SlashCommand:
    name: str
    text: Optional[str]


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

    def post_message(self, message: dict):
        """
        Posts the message to to channel configured in the webhook.
        """
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(message)

        requests.post(
            self.config.webhook_url,
            headers={
                "Content-type": "application/json"
            },
            data=json.dumps(message)
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
        logger.info(f'adding route {id}')

        def decorator(func: Callable) -> Callable:
            route = Route(
                id=id,
                pattern=re.compile(text_regex) if text_regex else None,
                handler=func
            )
            self.routes[id] = route
            return route

        return decorator

    def dispatch(self, cmd: SlashCommand):

        if cmd.name not in self.routes:
            logger.error(f'can\'t find a route for cmd {cmd.name}')
            raise RouteNotFound()

        route = self.routes[cmd.name]

        if route.pattern:
            match = route.pattern.match(cmd.text)
            if not match:
                msg = f'{cmd.text} doesn\'t match {route.pattern}'
                logger.warning(msg)
                raise RouteNotFound(msg)

            # call the command handler
            logger.info(f'handing off cmd {cmd.name} to {route.handler}')
            route.handler(**match.groupdict())
        else:
            # call the command handler
            route.handler()


def build_slash_command(body: str) -> SlashCommand:

    cmd = parse_qs(body)

    if 'text' in cmd:
        text = cmd['text'][0]
    else:
        text = None

    return SlashCommand(
        name=cmd['command'][0],
        text=text,
    )


class InvalidSignature(Exception):
    pass


class RouteNotFound(Exception):
    pass


def verify_signature(body: str, headers: Dict[str, str]):

    signature = headers.get('X-Slack-Signature')
    timestamp = headers.get('X-Slack-Request-Timestamp')

    req = str.encode(f'v0:{timestamp}:{body}')

    request_hash = 'v0=' + hmac.new(
            str.encode(config.SLACK_SIGNING_SECRET),
            req,
            hashlib.sha256
        ).hexdigest()

    if not hmac.compare_digest(request_hash, signature):
        raise InvalidSignature()
