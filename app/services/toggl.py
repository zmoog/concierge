import json
import collections
import datetime
import requests


TogglConfig = collections.namedtuple("TogglConfig", "api_token user_agent workspace_id")


class TogglService(object):

    def __init__(self, config):
        self.config = config

    def summary(self, since, until):

        url = f"https://toggl.com/reports/api/v2/summary?workspace_id={self.config.workspace_id}&since={since}&until={until}&user_agent={self.config.user_agent}"

        resp = requests.get(url, auth=(self.config.api_token, "api_token"))

        if resp.status_code == 200:
            return json.loads(resp.content)

        raise Exception(resp.content)
