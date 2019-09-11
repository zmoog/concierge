from app.intents.toggl import TogglSummary


def test_summary(toggl_service):

    intent = TogglSummary(toggl_service)

    entities = {
        "since": "2019-09-10",
        "until": "2019-09-10",
    }

    summary = intent.execute("random-execution-id", entities)

    assert "title" in summary
    assert summary["title"] == "Toggl Summary for Tuesday, September 10th 2019"

    assert "text" in summary
    assert "attachments" in summary

