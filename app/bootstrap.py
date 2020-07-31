from app.domain import commands, events
from app.services.unit_of_work import UnitOfWork
from app.services.messagebus import MessageBus
from app.services import handlers
from app.adapters import apple, dropbox, ifq, slack, toggl
from app import config


dropbox_adapter = dropbox.DropboxAdapter(
    config.DROPBOX_ROOT_FOLDER,
    config.DROPBOX_ACCESS_TOKEN,
)

ifq_adapter = ifq.IFQAdapter(
    config.IFQ_USERNAME,
    config.IFQ_PASSWORD,
)

slack_adapter = slack.SlackAdapter(slack.SlackConfig(
    webhook_url=config.SLACK_WEBHOOK_URL
))

toggl_adapter = toggl.TogglAdapter()

refurbished_adapter = apple.RefurbishedStoreAdapter()

uow = UnitOfWork(
    toggl_adapter,
    ifq_adapter,
    dropbox_adapter,
    slack_adapter,
    refurbished_adapter
)

command_handlers = {
    commands.CheckRefurbished: handlers.check_refurbished,
    commands.DownloadIFQ: handlers.download_ifq,
    commands.Summarize: handlers.summarize,
}

event_handlers = {
    events.RefurbishedProductAvailable: [
        handlers.notify_refurbished_product_available
    ],
    events.TogglEntriesSummarized: [
        handlers.notify_entries_summarized,
    ],
    events.IFQIssueAlreadyExists: [
        handlers.log_event,
        handlers.notify_ifq_issue_already_available,
    ],
    events.IFQIssueDownloaded: [
        handlers.log_event,
        handlers.notify_ifq_issue_downloaded,
    ],
    events.IFQIssueDownloadFailed: [
        handlers.log_event,
        handlers.notify_ifq_issue_download_failed,
    ],
}


def for_cli():
    event_handlers = {
        events.TogglEntriesSummarized: [
            handlers.log_entries_summarized,
        ],
        events.IFQIssueAlreadyExists: [
            handlers.log_event,
        ],
        events.IFQIssueDownloaded: [
            handlers.log_event,
        ],
        events.IFQIssueDownloadFailed: [
            handlers.log_event,
        ],
    }
    return MessageBus(uow, event_handlers, command_handlers)


def for_lambda():
    return MessageBus(uow, event_handlers, command_handlers)
