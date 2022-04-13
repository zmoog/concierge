import json

import pytest

from app import bootstrap, config
from app.adapters import (
    apple,
    classeviva,
    dropbox,
    ifq,
    slack,
    telegram,
    toggl,
)
from app.services.messagebus import MessageBus
from app.services.unit_of_work import UnitOfWork

# @pytest.fixture(scope="session")
# def tmp_dir(tmpdir_factory):
#     """
#     A tmp folder will be created before running
#     each test and deleted at the end, this way all the
#     tests work in isolation.
#     """
#     return str(tmpdir_factory.mktemp("ConciergeTest"))


# @pytest.fixture(scope="session")
# def ifq2dropbox(ifq, dropbox):
#     return Ifq2DropboxTask(ifq, dropbox)


# @pytest.fixture(scope="session")
# def toggl_config():
#     return TogglConfig(
#         os.environ["TOGGL_API_TOKEN"],
#         os.environ["TOGGL_USER_AGENT"],
#         os.environ["TOGGL_WORKSPACE_ID"],
#     )


# @pytest.fixture(scope="session")
# def toggl_service(toggl_config):
#     return TogglService(toggl_config)


# @pytest.fixture(scope="session")
# def summary_intent(toggl_service, slack_service):
#     return TogglSummaryIntent(toggl_service)


# @pytest.fixture(scope="session")
# def slack_config():
#     return SlackConfig(webhook_url=os.environ["SLACK_WEBHOOK_URL"])


# @pytest.fixture(scope="session")
# def slack_service(slack_config):
#     return SlackService(slack_config)


@pytest.fixture(scope="function")
def refurbished_adapter():
    return apple.RefurbishedStoreAdapter()


@pytest.fixture(scope="function")
def dropbox_adapter():
    return dropbox.DropboxAdapter(
        config.DROPBOX_ROOT_FOLDER,
        config.DROPBOX_ACCESS_TOKEN,
    )


@pytest.fixture(scope="function")
def classeviva_adapter():
    return classeviva.ClassevivaAdapter()


@pytest.fixture(scope="function")
def ifq_adapter():
    return ifq.IFQAdapter(
        config.IFQ_USERNAME,
        config.IFQ_PASSWORD,
    )


@pytest.fixture(scope="function")
def slack_adapter():
    return slack.SlackAdapter(
        slack.SlackConfig(webhook_url=config.SLACK_WEBHOOK_URL)
    )


@pytest.fixture(scope="function")
def telegram_adapter():
    return telegram.TelegramAdapter(config.TELEGRAM_TOKEN)


@pytest.fixture(scope="function")
def toggl_adapter():
    return toggl.TogglAdapter()


@pytest.fixture(scope="function")
def uow(
    refurbished_adapter,
    classeviva_adapter,
    dropbox_adapter,
    ifq_adapter,
    slack_adapter,
    telegram_adapter,
    toggl_adapter,
):
    return UnitOfWork(
        refurbished_adapter,
        classeviva_adapter,
        dropbox_adapter,
        ifq_adapter,
        slack_adapter,
        telegram_adapter,
        toggl_adapter,
    )


@pytest.fixture(scope="function")
def messagebus(uow):
    return MessageBus(
        uow,
        bootstrap.event_handlers,
        bootstrap.command_handlers,
    )


@pytest.fixture(scope="function")
def from_json():
    def wrapper(path: str):
        with open(path) as f:
            return json.loads(f.read())

    return wrapper
