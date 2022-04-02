from datetime import date

from app.domain.commands import Summarize
from app.domain.events import TogglEntriesSummarized
from app.services.handlers import summarize


def test_summarize_without_entries(mocker, uow, toggl_adapter, from_json):

    summary = from_json("tests/data/toggl/summary-2020-07-19.json")
    mocker.patch.object(toggl_adapter, "summary")
    toggl_adapter.summary.side_effect = [summary]

    expected_events = [
        TogglEntriesSummarized(
            summary="""\
Here's the summary for Thursday, June 25 2020

---

Oooops, there are no entries here ¯\\_(ツ)_/¯

"""
        )
    ]

    cmd = Summarize(day=date(2020, 6, 25))

    actual_events = summarize(cmd, uow, {})

    assert len(actual_events) == len(expected_events)
    assert actual_events[0].summary == expected_events[0].summary


def test_summarize_with_entries(mocker, uow, toggl_adapter, from_json):

    summary = from_json("tests/data/toggl/summary-2020-06-25.json")
    mocker.patch.object(toggl_adapter, "summary")
    toggl_adapter.summary.side_effect = [summary]

    expected_events = [
        TogglEntriesSummarized(
            summary="""\
Here's the summary for Thursday, June 25 2020

---

# Arduino (11 hours)
 * AEK R2: check datocms upload (22 minutes)
 * Classroom: meeting w/ Luca Osti (33 minutes)
 * Contact Us: add tags in Support API (an hour)
 * 🌊 Inbox (39 minutes)
 * IoT Cloud: 'measured at' support added [add dual-write] (an hour)
 * Onboarding (6 hours)

# Maintenance (3 hours)
 * 🍲 Dinner (2 hours)
 * 🍜 Lunch (an hour)

# Professional development (an hour)
 * Concierge: today recap (an hour)

"""
        )
    ]

    cmd = Summarize(day=date(2020, 6, 25))

    actual_events = summarize(cmd, uow, {})

    assert len(actual_events) == len(expected_events)
    assert actual_events[0].summary == expected_events[0].summary
