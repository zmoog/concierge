import logging
import uuid


class RunIntentHandler(object):

    def __init__(self, slack_service):
        # self.logger = logging.getLogger("concierge.handlers.run-intent")
        self.logger = logging.getLogger(__name__)
        self.slack = slack_service

    def execute(self, intent, entities: dict):

        execution_id = uuid.uuid4()

        self.logger.info(f"Running intent {intent}")
        message = intent.execute(execution_id, entities)

        self.logger.info(f"posting resulting message {message} to Slack")
        self.slack.post(message)
