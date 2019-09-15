import os
import datetime
import json
import logging

from app.services.slack import SlackService, SlackConfig
from app.services.toggl import TogglService, TogglConfig
from app.handlers.run import RunIntentHandler
from app.intents.toggl import TogglSummaryIntent

root_logger = logging.getLogger()
root_logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

runner = RunIntentHandler(
            SlackService(
                SlackConfig(os.environ["SLACK_WEBHOOK_URL"])))

intent = TogglSummaryIntent(
            TogglService(
                TogglConfig(
                    os.environ["TOGGL_API_TOKEN"],
                    os.environ["TOGGL_USER_AGENT"],
                    os.environ["TOGGL_WORKSPACE_ID"],
                )
            )
)


def handler(event, context):

    logger.info(f"event: {event}")

    # entities = {
    #     "since": "2019-09-12",
    #     "until": "2019-09-12",
    # }

    runner.execute(intent, event.get("entities", {}))
