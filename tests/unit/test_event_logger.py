from app.domain import events
from app.services import handlers
from app.adapters import terminal


def test_log_event_as_text(mocker, uow):
    spy = mocker.spy(terminal, "log")

    event = events.IFQIssueDownloaded(filename="ilfatto-2020-07-23.pdf")
    handlers.log_event(event, uow)

    spy.assert_called_once_with(
        "IFQIssueDownloaded(filename='ilfatto-2020-07-23.pdf')"
    )
