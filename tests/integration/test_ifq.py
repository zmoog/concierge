from datetime import date

from app.adapters import dropbox, ifq, slack
from app.domain import commands
from app.services.messagebus import MessageBus


def test_issue_is_already_available(
    mocker,
    messagebus: MessageBus,
    dropbox_adapter: dropbox.DropboxAdapter,
    slack_adapter: slack.SlackAdapter,
):
    mocker.patch.object(dropbox_adapter, 'exists')
    dropbox_adapter.exists.side_effect = [True]

    mocker.patch.object(slack_adapter, 'post_message')
    slack_adapter.post_message.side_effect = [None]

    cmd = commands.DownloadIFQ(day=date(2020, 7, 30))

    messagebus.handle(cmd, {})

    message = {
        'text': "Hey, the IFQ issue named`ilfatto-20200730.pdf`"
        " is already available."
    }
    slack_adapter.post_message.assert_called_once_with(
        message, {}
    )


def test_ifq_issue_downloaded(
    mocker,
    messagebus: MessageBus,
    dropbox_adapter: dropbox.DropboxAdapter,
    ifq_adapter: ifq.IFQAdapter,
    slack_adapter: slack.SlackAdapter,
):
    mocker.patch.object(dropbox_adapter, 'exists')
    mocker.patch.object(dropbox_adapter, 'put_file')
    mocker.patch.object(ifq_adapter, 'download_pdf')
    dropbox_adapter.exists.side_effect = [False]
    dropbox_adapter.put_file.side_effect = [None]
    ifq_adapter.download_pdf.side_effect = ['/some/path']

    mocker.patch.object(slack_adapter, 'post_message')
    slack_adapter.post_message.side_effect = [None]

    cmd = commands.DownloadIFQ(day=date(2020, 7, 30))

    messagebus.handle(cmd, {})

    message = {
        'text': "Hey, the IFQ issue named `ilfatto-20200730.pdf` "
        "has been downloaded successfully! 🎉"
    }
    slack_adapter.post_message.assert_called_once_with(
        message, {}
    )


def test_ifq_issue_download_failed(
    mocker,
    messagebus: MessageBus,
    dropbox_adapter: dropbox.DropboxAdapter,
    slack_adapter: slack.SlackAdapter,
):
    mocker.patch.object(dropbox_adapter, 'exists')
    dropbox_adapter.exists.side_effect = Exception("ka-booom!")

    mocker.patch.object(slack_adapter, 'post_message')
    slack_adapter.post_message.side_effect = [None]

    cmd = commands.DownloadIFQ(day=date(2020, 7, 30))

    messagebus.handle(cmd, {})

    message = {
        'text': "Hey, the download of the IFQ issue "
        "named `ilfatto-20200730.pdf` is failed"
        " (`Exception('ka-booom!')`)."
    }
    slack_adapter.post_message.assert_called_once_with(
        message, {}
    )
