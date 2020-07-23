import collections
import logging
import json
import requests


SlackConfig = collections.namedtuple("SlackConfig", "webhook_url")


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

    def post_message(self, message):
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
