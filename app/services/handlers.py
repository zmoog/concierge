import datetime
import traceback
from typing import Any, Dict, List

from humanize import naturaldelta

from app.adapters import terminal
from app.domain import commands, events
from app.services.unit_of_work import UnitOfWork


def summarize(
    cmd: commands.Summarize,
    uow: UnitOfWork,
    context: Dict[str, Any],
) -> List[events.Event]:
    """Summarize the toggl entries for a given day"""
    with uow:
        summary = uow.toggl.summary(cmd.day, cmd.day)
        x = cmd.day.strftime('%A, %B %d %Y')
        text = f"Here's the summary for {x}\n\n---\n\n"

        if not summary["data"]:
            text += "Oooops, there are no entries here ¯\\_(ツ)_/¯\n\n"
            return [events.TogglEntriesSummarized(text)]

        for entry in summary["data"]:
            project_duration = 0
            items_text = ""
            for item in entry["items"]:
                item_duration = item["time"]
                project_duration += item_duration
                duration = naturaldelta(
                    datetime.timedelta(milliseconds=item_duration)
                )
                items_text += \
                    f" * {item['title']['time_entry']} ({duration})\n"

            x = naturaldelta(
                datetime.timedelta(milliseconds=project_duration)
            )

            text += f"# {entry['title']['project']} ({x})\n"
            text += items_text
            text += "\n"
        return [events.TogglEntriesSummarized(text)]


def check_refurbished(
    cmd: commands.CheckRefurbished,
    uow: UnitOfWork,
    context: Dict[str, Any],
) -> List[events.Event]:
    """Checks the refurbished section of the Apple Store looking for deals."""
    with uow:
        _events = []
        for product in cmd.products:
            products = uow.refurbished.search(cmd.store, product)
            if not products:
                _events.append(events.RefurbishedProductNotAvailable(
                    store=cmd.store,
                    product=product,
                ))
                continue

            text = f"Found {len(products)} {product}(s):\n\n"
            for p in products:
                text += \
                    f"- <{p.url}|{p.name}> at ~{p.previous_price}~ \
*{p.price}* (-{p.savings_price})\n"
            _events.append(
                events.RefurbishedProductAvailable(text=text)
            )
        return _events


def download_ifq(
    cmd: commands.DownloadIFQ,
    uow: UnitOfWork,
    context: Dict[str, Any],
) -> List[events.Event]:
    FILENAME_PATTERN = 'ilfatto-%Y%m%d.pdf'
    try:
        filename = cmd.day.strftime(FILENAME_PATTERN)

        if uow.dropbox.exists(filename):
            return [events.IFQIssueAlreadyExists(filename)]

        local_file_path = uow.ifq.download_pdf(cmd.day)

        uow.dropbox.put_file(local_file_path, filename)

        return [events.IFQIssueDownloaded(filename)]
    # except ifq.IssueNotAvailable as error:
    #     return [events.ifq]
    except Exception as error:
        return [events.IFQIssueDownloadFailed(
            filename,
            error,
            traceback.format_exc(),
        )]


def log_entries_summarized(
    event: events.TogglEntriesSummarized,
    uow: UnitOfWork,
    context: Dict[str, Any],
):
    """Logs the event in the termimal"""
    terminal.log(event.summary)


def log_event(
    event: events.Event,
    uow: UnitOfWork,
    context: Dict[str, Any],
):
    """"Logs events"""
    text = str(event)
    terminal.log(text)


def notify_entries_summarized(
    event: events.TogglEntriesSummarized,
    uow: UnitOfWork,
    context: Dict[str, Any],
):
    """Notify the event in a Slack channel"""

    uow.slack.post_message({
        'text': f"""
```
{event.summary}
```
"""
    }, context)


def notify_refurbished_product_available(
    event: events.RefurbishedProductAvailable,
    uow: UnitOfWork,
    context: Dict[str, Any],
):
    """Notify the event in a Slack channel"""

    uow.slack.post_message({
        'text': f"""
{event.text}
"""
    }, context)


def notify_refurbished_product_not_available(
    event: events.RefurbishedProductNotAvailable,
    uow: UnitOfWork,
    context: Dict[str, Any],
):
    """Notify the event in a Slack channel"""

    uow.slack.post_message({
        'text': f"Hey, can't find any '{event.product}' "
        f"in the '{event.store}' store now 🤔"
    }, context)


def notify_ifq_issue_already_available(
    event: events.IFQIssueAlreadyExists,
    uow: UnitOfWork,
    context: Dict[str, Any],
):
    """Notify the event in a Slack channel"""

    uow.slack.post_message({
        'text': f'Hey, the IFQ issue named`{event.filename}`'
        ' is already available.'
    }, context)


def notify_ifq_issue_downloaded(
    event: events.IFQIssueDownloaded,
    uow: UnitOfWork,
    context: Dict[str, Any],
):
    """Notify the event in a Slack channel"""

    uow.slack.post_message({
        'text': f'Hey, the IFQ issue named `{event.filename}`'
        ' has been downloaded successfully! 🎉'
    }, context)


def notify_ifq_issue_download_failed(
    event: events.IFQIssueDownloadFailed,
    uow: UnitOfWork,
    context: Dict[str, Any],
):
    """Notify the event in a Slack channel"""

    uow.slack.post_message({
        'text': f"Hey, the download of the IFQ issue "
        f"named `{event.filename}` is failed"
        f" (`{event.error!r}`)."
    }, context)
