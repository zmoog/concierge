import json
import logging


class TogglSummaryIntent(object):
    """Fetches the report data from Toggl and format as a Slack message.
    """
    
    def __init__(self, toggl_service,):
        self.logger = logging.getLogger(__name__)
        self.toggl = toggl_service

    def execute(self, execution_id: str, entities: dict):
        """Executes the intent using the given entities
        """

        summary = self.toggl.summary(entities["since"], entities["until"])

        if "data" not in summary or len(summary["data"]) == 0:
            return {
                "title": "No data",
                "text": "There are no entries for this date."
            }

        if self.logger.isEnabledFor("DEBUG"):
            self.logger.debug(json.dumps(summary, indent=2))

        # TODO: should we move to the new Slack block api for messages?
        attachments = [
            {
                "title": entry["title"]["project"], 
                "text": "".join([" * {}\n".format(item["title"]["time_entry"]) for item in entry["items"]]),
                "mrkdwn_in": ["text"]
            } for entry in summary["data"]
        ]

        return {
            "text": "Toggl Summary",
            "attachments": attachments
        }
