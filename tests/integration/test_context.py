from app.adapters import apple, slack
from app.domain import commands
from app.services import messagebus


def test_unavailable_products(
    mocker,
    messagebus: messagebus.MessageBus,
    refurbished_adapter: apple.RefurbishedStoreAdapter,
    slack_adapter: slack.SlackAdapter,
):
    mocker.patch.object(refurbished_adapter, "search")
    refurbished_adapter.search.side_effect = [[]]

    mocker.patch.object(slack_adapter, 'post_message')
    slack_adapter.post_message.side_effect = [None]

    cmd = commands.CheckRefurbished(store='it', products=['ipad'])
    ctx = {
        "slack": {
            "response_url": "https://stocazzo.net",
        }
    }

    messagebus.handle(cmd, ctx)

    message = {
        'text': "Hey, can't find any 'ipad' in the 'it' store now 🤔"
    }
    slack_adapter.post_message.assert_called_once_with(
       message, ctx
    )
