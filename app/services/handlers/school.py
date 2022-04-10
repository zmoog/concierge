from itertools import groupby
from typing import Any, Dict, List

from app import config
from app.domain import events
from app.domain.commands.school import ListHomework
from app.domain.events.school import HomeworkAvailable, NoHomework
from app.services.unit_of_work import UnitOfWork


def list_homework(
    cmd: ListHomework, uow: UnitOfWork, context: Dict[str, Any]
) -> List[events.Event]:
    assignments = uow.classeviva.list_assignments(
        days=cmd.days
    )  # for the next n days
    print(f"fetched {len(assignments)} assignments")

    if not assignments:
        return [NoHomework(days=cmd.days)]

    return [HomeworkAvailable(assignments, days=cmd.days)]


def notify_no_homework(
    event: NoHomework, uow: UnitOfWork, context: Dict[str, Any]
):
    msg = f"No homework for the next {event.days} days"
    group_id = config.TELEGRAM_DEFAULT_GROUP_ID

    print(f"notifying using telegram to group {group_id}: {msg}")

    uow.telegram.send_message(
        msg,
        config.TELEGRAM_DEFAULT_GROUP_ID,
    )


def notify_homework_available(
    event: HomeworkAvailable, uow: UnitOfWork, context: Dict[str, Any]
):
    msg = f"Here's the homework for the next {event.days} days:\n\n"
    group_id = config.TELEGRAM_DEFAULT_GROUP_ID

    def by_start_date(entry):
        # return entry.starts_at[:10]
        return entry.starts_at.date()

    # I want the grade list sorted by date, ascending
    sorted_entries = sorted(
        event.assignments, key=by_start_date, reverse=False
    )

    for day, entries in groupby(sorted_entries, key=by_start_date):
        msg += f"{day:%Y-%m-%d}\n"
        for entry in entries:
            msg += f"- {entry.teacher}, {entry.notes}\n"
        msg += "\n"

    print(f"notifying using telegram to group {group_id}: {msg}")

    uow.telegram.send_message(msg, group_id)
