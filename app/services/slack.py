import collections
import json
import requests


SlackConfig = collections.namedtuple("SlackConfig", "webhook_url")


class SlackService(object):

    def __init__(self, config: SlackConfig):
        self.config = config

    def post(self, message):
        requests.post(self.config.webhook_url, headers={"Content-type": "application/json"}, data=json.dumps(message))


