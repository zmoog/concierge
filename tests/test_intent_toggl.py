import datetime


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


def test_find_previous_business_day__simple(summary_intent):

    thursday = datetime.date(2019, 9, 12)
    friday = datetime.date(2019, 9, 13)

    previous_business_day = summary_intent._find_previous_business_day(friday)

    assert previous_business_day == thursday


def test_find_previous_business_day__cross_weekend(summary_intent):

    friday = datetime.date(2019, 9, 13)
    monday = datetime.date(2019, 9, 16)

    previous_business_day = summary_intent._find_previous_business_day(monday)

    assert previous_business_day == friday
