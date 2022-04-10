from app import config
from app.adapters import (
    apple,
    classeviva,
    dropbox,
    ifq,
    slack,
    telegram,
    toggl,
)
from app.domain import commands, events
from app.domain.commands.school import ListHomework
from app.domain.events.school import HomeworkAvailable, NoHomework
from app.services import handlers
from app.services.handlers.school import (
    list_homework,
    notify_homework_available,
    notify_no_homework,
)
from app.services.messagebus import MessageBus
from app.services.unit_of_work import UnitOfWork

refurbished_adapter = apple.RefurbishedStoreAdapter()

classeviva_adapter = classeviva.ClassevivaAdapter()

dropbox_adapter = dropbox.DropboxAdapter(
    config.DROPBOX_ROOT_FOLDER,
    config.DROPBOX_ACCESS_TOKEN,
)

ifq_adapter = ifq.IFQAdapter(
    config.IFQ_USERNAME,
    config.IFQ_PASSWORD,
)

slack_adapter = slack.SlackAdapter(
    slack.SlackConfig(webhook_url=config.SLACK_WEBHOOK_URL)
)

telegram_adapter = telegram.TelegramAdapter(config.TELEGRAM_TOKEN)

toggl_adapter = toggl.TogglAdapter()


uow = UnitOfWork(
    refurbished_adapter,
    classeviva_adapter,
    dropbox_adapter,
    ifq_adapter,
    slack_adapter,
    telegram_adapter,
    toggl_adapter,
)

command_handlers = {
    commands.CheckRefurbished: handlers.check_refurbished,
    ListHomework: list_homework,
    commands.DownloadIFQ: handlers.download_ifq,
    commands.Summarize: handlers.summarize,
}

event_handlers = {
    events.RefurbishedProductAvailable: [
        handlers.notify_refurbished_product_available,
    ],
    events.RefurbishedProductNotAvailable: [
        handlers.notify_refurbished_product_not_available,
    ],
    HomeworkAvailable: [
        notify_homework_available,
    ],
    NoHomework: [
        notify_no_homework,
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
            handlers.log_summarized_entries,
        ],
        events.RefurbishedProductAvailable: [
            handlers.log_refurbished_product,
        ],
        events.RefurbishedProductNotAvailable: [
            handlers.log_event,
        ],
        HomeworkAvailable: [
            notify_homework_available,
        ],
        NoHomework: [
            notify_no_homework,
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
