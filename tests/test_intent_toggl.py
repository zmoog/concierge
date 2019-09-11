from app.intents.toggl import TogglSummary


def test_empty_summary(summary_intent):

    entities = {
        "since": "2019-09-11",
        "until": "2019-09-11",
    }

    summary = summary_intent.execute("random-execution-id", entities)

    assert "title" in summary
    # assert summary["title"] == "Toggl Summary for Tuesday, September 10th 2019"

    assert "text" in summary
    assert summary["text"] == f"There are no entries for this date."
    # assert "attachments" in summary


def test_summary(summary_intent):

    entities = {
        "since": "2019-09-10",
        "until": "2019-09-10",
    }

    summary = summary_intent.execute("random-execution-id", entities)

    assert "title" in summary
    # assert summary["title"] == "Toggl Summary for Tuesday, September 10th 2019"

    assert "text" in summary
    # assert "attachments" in summary

