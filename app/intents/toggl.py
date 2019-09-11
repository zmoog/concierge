import json


class TogglSummary(object):
    
    def __init__(self, toggl_service, slack_service):
        self.toggl = toggl_service
        self.slack = slack_service

    def execute(self, execution_id: str, entities: dict):

        summary = self.toggl.summary(entities["since"], entities["until"])

        if "data" not in summary or len(summary["data"]) == 0:
            return {
                "title": "No data",
                "text": "There are no entries for this date."
            }

        print(json.dumps(summary, indent=2))

        attachments = [
            {
                "title": entry["title"]["project"], 
                "text": "".join([" * {}\n".format(item["title"]["time_entry"]) for item in entry["items"]]),
                "mrkdwn_in": ["text"]
            } for entry in summary["data"]
        ]

        message = {
            "text": "Toggl Summary",
            "attachments": attachments
        }

        self.slack.post(message)

        return message
