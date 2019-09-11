import os
import datetime
import pytest

from app.services.dropbox import DropboxService
from app.services.ifq import IFQ
from app.tasks import Ifq2DropboxTask
from app.services.toggl import TogglService, TogglConfig

# @pytest.fixture(scope="session")
# def tmp_dir(tmpdir_factory):
#     """
#     A tmp folder will be created before running
#     each test and deleted at the end, this way all the
#     tests work in isolation.
#     """
#     return str(tmpdir_factory.mktemp("ConciergeTest"))


@pytest.fixture(scope="session")
def dropbox():
    return DropboxService(os.environ['DROPBOX_ROOT_FOLDER'], os.environ['DROPBOX_ACCESS_TOKEN'])

@pytest.fixture(scope="session")
def ifq():
    return IFQ(os.environ['IFQ_USERNAME'], os.environ['IFQ_PASSWORD'])

@pytest.fixture(scope="session")
def ifq2dropbox(ifq, dropbox):
    return Ifq2DropboxTask(ifq, dropbox)

@pytest.fixture(scope="session")
def toggl_config():
    return TogglConfig(
        os.environ["TOGGL_API_TOKEN"],
        os.environ["TOGGL_USER_AGENT"],
        os.environ["TOGGL_WORKSPACE_ID"],
    )

@pytest.fixture(scope="session")
def toggl_service(toggl_config):
    return TogglService(toggl_config)

