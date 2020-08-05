import json
import logging
from typing import Any

from app import bootstrap, config
from app.adapters import aws

# setup logging
app_logger = logging.getLogger()
app_logger.setLevel(config.LOG_LEVEL)

logger = logging.getLogger(__name__)

# wire up required components
messagebus = bootstrap.for_lambda()
sns_handler = aws.SNSMessageHandler(
    messagebus,
)


def dispatch_command(event: dict, context: Any = None):
    # dump the event in the log, it will be removed later
    # or replaced w/ an appropriate log level
    logger.info(f"event: {json.dumps(event)}")

    sns_handler.dispatch(event)
