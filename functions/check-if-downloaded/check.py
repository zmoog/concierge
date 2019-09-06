import os
import datetime
import json

from app.services.dropbox import DropboxService

dropboxService = DropboxService(os.environ['DROPBOX_ROOT_FOLDER'], os.environ['DROPBOX_ACCESS_TOKEN'])


def handler(event, context):
    """Handles the entry poiny fo the language.
    """
    filename = datetime.date.today().strftime('ilfatto-%Y%m%d.pdf')

    exists = dropboxService.exists(filename)

    return {
        'exists': bool(exists)
    }
