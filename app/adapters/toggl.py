import urllib
import requests

from datetime import datetime
from typing import Any, Dict, List

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

        if resp.status_code != 200:
            return Exception(resp.content)

        return resp.json()

    def details(self,
                since: datetime,
                until: datetime,
                project_ids: List[int] = None) -> List[Dict[Any, Any]]:
        """Fetches the Toggl detailed report between `since` and `until` datetimes.

        Toggl Reports API v2
        https://github.com/toggl/toggl_api_docs/blob/master/reports/detailed.md
        """
        params = dict(
            workspace_id=config.TOGGL_WORKSPACE_ID,
            since=since,
            until=until,
            user_agent=config.TOGGL_USER_AGENT,
            page=1,
        )

        if project_ids:
            params["project_ids"] = ".".join(project_ids)

        has_more = True

        while has_more:
            result = self._get_details_page(params)
            # print("total_count", result["total_count"])
            # print("per_page", result["per_page"])
            for entry in result["data"]:
                yield entry

            if not result["data"]:
                has_more = False

            params["page"] += 1

    def _get_details_page(_, params) -> Dict[str, Any]:

        url = "https://toggl.com/reports/api/v2/details?" + \
            urllib.parse.urlencode(params)

        # For the authentication details see the official Toggl API docs:
        # https://github.com/toggl/toggl_api_docs/blob/master/chapters/authentication.md
        resp = requests.get(url, auth=(config.TOGGL_API_TOKEN, "api_token"))

        if resp.status_code != 200:
            raise Exception(resp.content)

        return resp.json()
