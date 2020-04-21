
def test_by_project(summary_by_project_intent):

    entities = {
        "since": "2020-04-09",
        "until": "2020-04-09"
    }

    summary = summary_by_project_intent.execute("random-id", entities)

    print(summary)

    assert summary is not None

