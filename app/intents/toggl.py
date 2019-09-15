import datetime
import json
import logging


class TogglSummaryIntent(object):
    """Fetches the report data from Toggl and format as a Slack message.
    """

    def __init__(self, toggl_service):
        self.logger = logging.getLogger(__name__)
        self.toggl = toggl_service

    def execute(self, execution_id: str, entities: dict):
        """Executes the intent using the given entities
        """
        if "since" in entities and "until" in entities:
            since = entities["since"]
            until = entities["until"]
        else:
            business_day = self._find_previous_business_day(datetime.date.today())
            since = business_day.strftime("%Y-%m-%d")
            until = business_day.strftime("%Y-%m-%d")

        summary = self.toggl.summary(since, until)

        if "data" not in summary or len(summary["data"]) == 0:
            return {
                "title": "No data",
                "text": "There are no entries for this date."
            }

        if self.logger.isEnabledFor(logging.DEBUG):
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

    def _find_previous_business_day(self, date):
        """Find the previous business day of the given date.

        The current definition of 'business day' is quite simple and limited to week days between mon-fri. It doesn't
        consider holidays at all (it can be a future improvement).

        :param date: the date of the given day. :return: a date object of the previous business day (see the
        description above for a devinition of the 'business day' term.
        """
        business_days = [0, 1, 2, 3, 4]  # Monday to Friday

        previous_day = date - datetime.timedelta(days=1)

        while previous_day.weekday() not in business_days:
            previous_day -= datetime.timedelta(days=1)

        return previous_day
