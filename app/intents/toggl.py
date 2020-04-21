import datetime
import logging

from typing import Optional
from humanize import naturaldelta


def _extract_dates(entities, default_day=datetime.date.today):
    if "since" in entities and "until" in entities:
        since = entities["since"]
        until = entities["until"]
    else:
        business_day = default_day()
        since = business_day.strftime("%Y-%m-%d")
        until = business_day.strftime("%Y-%m-%d")
    return since, until


def _build_attachment(entry):

    text = "".join(
        [" * {time_entry} ({duration})\n".format(
             time_entry=item["title"]["time_entry"],
             duration=naturaldelta(
                 datetime.timedelta(milliseconds=item["time"])),
        ) for item in entry["items"]]
    )
    project_name = entry["title"]["project"]
    project_duration = datetime.timedelta(milliseconds=entry["time"])

    return {
            "title": f"{project_name} ({naturaldelta(project_duration)})",
            "text": text,
            "mrkdwn_in": ["text"]
    }


class TogglSummaryIntent:
    """Fetches the report data from Toggl and format as a Slack message.
    """
    def __init__(self, toggl_service):
        self.logger = logging.getLogger(__name__)
        self.toggl = toggl_service

    def execute(self, execution_id: str, entities: dict):
        """Executes the intent using the given entities
        """
        since, until = _extract_dates(
            entities,
            default_day=datetime.date.today
        )

        summary = self.toggl.summary(since, until)

        if "data" not in summary or len(summary["data"]) == 0:
            return {
                "text": "There are no entries for this date."
            }

        # TODO: should we move to the new Slack block api for messages?
        attachments = [
            _build_attachment(entry) for entry in summary["data"]
        ]

        return {
            "text": f"Toggl Summary: from {since} to {until}",
            "attachments": attachments
        }


# class TogglSummaryByProjectIntent(TogglBaseIntent):
#     """Fetches the report data from Toggl and format as a Slack message.
#     """

#     def execute(self, execution_id: str, entities: dict):
#         """Executes the intent using the given entities
#         """
#         since, until = _extract_dates(entities)
#         grouping_params = dict(
#             grouping='projects',
#             subgrouping='tasks'
#         )

#         summary = self.toggl.summary(since, until, grouping_params)

#         print('summary', summary)

#         if len(summary.get("data", [])) == 0:
#             return {
#                 "title": "No data",
#                 "text": "There are no entries for this date."
#             }

#         # TODO: should we move to the new Slack block api for messages?

#         attachments = [
#             self._attachment(
#                 project['title']['project'],
#                 "".join([" * {time_entry} ({duration})\n".format(
#                     time_entry=item["title"]["task"],
#                     # duration=humanize.naturaldelta(datetime.timedelta(milliseconds=item["time"])),
#                     # duration=datetime.timedelta(milliseconds=item["time"]),
#                     duration=self._format_delta(datetime.timedelta(milliseconds=item["time"]))
#                 ) for item in project["items"]])
#             ) for project in summary["data"]
#         ]

#         return {
#             "text": "Toggl Summary (group by projects and tasks)",
#             "attachments": attachments
#         }

    def _format_delta(self, delta: datetime.timedelta):

        # arbitrary number of seconds
        s = delta.seconds
        # hours
        hours = s // 3600
        # remaining seconds
        s = s - (hours * 3600)
        # minutes
        minutes = s // 60
        # remaining seconds
        # seconds = s - (minutes * 60)
        # total time
        # print '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
        # result: 03:43:40
        return '{:02}:{:02}'.format(int(hours), int(minutes))

    # def _attachment(self, title, text):
    #     return {
    #         "title": title,
    #         "text": text,
    #         "mrkdwn_in": ["text"]
    #     }
