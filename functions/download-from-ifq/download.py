import os
import json
import datetime

from app.services.ifq import IFQ, IssueNotAvailable
from app.services.dropbox import DropboxService
from app.tasks import Ifq2DropboxTask

task = Ifq2DropboxTask(
    IFQ(os.environ['IFQ_USERNAME'], os.environ['IFQ_PASSWORD']),
    DropboxService(os.environ['DROPBOX_ROOT_FOLDER'], os.environ['DROPBOX_ACCESS_TOKEN'])
)

def handler(event, context):

    try:
        task.execute(datetime.date.today())
        available = True

    except IssueNotAvailable:
        available = False

    return {
        "available": available,
    }
