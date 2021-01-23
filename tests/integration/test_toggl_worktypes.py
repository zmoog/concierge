from datetime import date

from app.adapters import slack, toggl
from app.domain import commands
from app.services import messagebus


def test_toggl_worktypes(
    mocker,
    messagebus: messagebus.MessageBus,
    toggl_adapter: toggl.TogglAdapter,
    slack_adapter: slack.SlackAdapter,
    from_json,
):
    mocker.patch.object(toggl_adapter, "details")
    toggl_adapter.details.side_effect = [
        from_json("tests/data/toggl/details-2021-01-05.json")["data"]
    ]

    mocker.patch.object(slack_adapter, 'post_message')
    slack_adapter.post_message.side_effect = [None]

    cmd = commands.SummarizeWorkTypes(since=date(2021, 1, 5),
                                      until=date(2021, 1, 5),
                                      project_ids=["153201265"])

    messagebus.handle(cmd, {})

    message = {
        'text': """
```
 - business:planned 0.0%
 - business:unplanned 0.0%
 - maintenance:planned 22.5%
 - maintenance:unplanned 4.4%
 - uncategorized 73.0%

```
"""
    }

    slack_adapter.post_message.assert_called_once_with(
        message, {}
    )
