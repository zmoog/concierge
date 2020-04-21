import os
import datetime
import logging

from app.services.slack import SlackService, SlackConfig
from app.services.toggl import TogglService, TogglConfig
from app.handlers.run import RunIntentHandler
from app.intents.toggl import TogglSummaryIntent
from app.datetime import find_previous_business_day

root_logger = logging.getLogger()
root_logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

runner = RunIntentHandler(
            SlackService(
                SlackConfig(os.environ["SLACK_WEBHOOK_URL"])))

toggl_service = TogglService(
                TogglConfig(
                    os.environ["TOGGL_API_TOKEN"],
                    os.environ["TOGGL_USER_AGENT"],
                    os.environ["TOGGL_WORKSPACE_ID"],
                )
            )

intent = TogglSummaryIntent(toggl_service)

generators = {
    "previous_business_day": find_previous_business_day,
}


def handler(event, context):

    logger.info(f"event: {event}")

    if 'when' in event and event['when'] in generators:
        date = generators.get(event['when'])()
    else:
        date = datetime.date.today()

    entities = {
        "since": date,
        "until": date,
    }

    runner.execute(intent, entities)
