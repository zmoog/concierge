import datetime


def test_empty_summary(summary_intent):

    entities = {
        "since": "2006-01-01",
        "until": "2006-01-01",
    }

    summary = summary_intent.execute("random-execution-id", entities)

    assert "text" in summary
    assert summary["text"] == f"There are no entries for this date."
    # assert "attachments" in summary


def test_summary(summary_intent):

    entities = {
        "since": "2019-09-10",
        "until": "2019-09-10",
    }

    summary = summary_intent.execute("random-execution-id", entities)

    assert "text" in summary
    assert summary["text"] == "Toggl Summary: from 2019-09-10 to 2019-09-10"

    assert "attachments" in summary
