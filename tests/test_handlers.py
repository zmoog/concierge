import pytest

from app.handlers.run import RunIntentHandler
from app.intents.toggl import TogglSummaryIntent


@pytest.fixture(scope="session")
def run_intent_handler(slack_service):
    return RunIntentHandler(slack_service)


def test_run_intent(run_intent_handler, toggl_service):

    intent = TogglSummaryIntent(toggl_service)
    entities = {
        "since": "2019-09-12",
        "until": "2019-09-12",
    }

    run_intent_handler.execute(intent, entities)
