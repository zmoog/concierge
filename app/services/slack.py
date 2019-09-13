import collections
import logging
import json
import requests


SlackConfig = collections.namedtuple("SlackConfig", "webhook_url")


class SlackService(object):
    """
    Offers a Slack API integration.
    """

    def __init__(self, config: SlackConfig):
        self.logger = logging.getLogger(__name__)
        self.config = config

    def post(self, message):
        """Posts the message to to channel configured in the webhook.
        """
        if self.logger.isEnabledFor("DEBUG"):
            self.logger.debug(message)
            
        requests.post(self.config.webhook_url, headers={"Content-type": "application/json"}, data=json.dumps(message))


