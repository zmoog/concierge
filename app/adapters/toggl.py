import json
import urllib
import requests

from datetime import datetime
from app import config


class TogglAdapter:

    def summary(self, since: datetime, until: datetime):
        """Fetches the Toggl report between `since` and `until` dates.

        Toggl Reports API v2
        https://github.com/toggl/toggl_api_docs/blob/master/reports.md
        https://github.com/toggl/toggl_api_docs/blob/master/reports/summary.md  
        """
        params = dict(
            workspace_id=config.TOGGL_WORKSPACE_ID,
            since=since,
            until=until,
            user_agent=config.TOGGL_USER_AGENT,
        )

        url = "https://toggl.com/reports/api/v2/summary?" + \
            urllib.parse.urlencode(params)

        # For the authentication details see the official Toggl API docs:
        # https://github.com/toggl/toggl_api_docs/blob/master/chapters/authentication.md
        resp = requests.get(url, auth=(config.TOGGL_API_TOKEN, "api_token"))

        if resp.status_code == 200:
            return json.loads(resp.content)

        # TODO: should we add a http exception to report back the HTTP status?
        raise Exception(resp.content)
