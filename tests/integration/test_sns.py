from app.services import messagebus
# from app.domain import commands
from app.adapters import apple, aws, slack
# from app.entrypoints.aws.lambda_function.sns import dispatch_command


def test_check_refurbished_products_triggered_by_a_sns_notification(
    mocker,
    from_json,
    messagebus: messagebus.MessageBus,
    refurbished_adapter: apple.RefurbishedStoreAdapter,
    slack_adapter: slack.SlackAdapter,
):
    # setup event from SNS
    event = from_json(
        'tests/data/aws/sns/events/publish/check-refurbished.json'
    )
    assert event

    mocker.patch.object(refurbished_adapter, "search")
    refurbished_adapter.search.side_effect = [[]]

    mocker.patch.object(slack_adapter, 'post_message')
    slack_adapter.post_message.side_effect = [None]

    # cmd = commands.CheckRefurbished(store='it', products=['ipad'])
    # messagebus.handle(cmd)

    sns_handler = aws.SNSMessageHandler(messagebus)
    sns_handler.dispatch(event)

    message = {
        'text': "Hey, can't find any 'ipad' in the 'it' store now 🤔"
    }
    slack_adapter.post_message.assert_called_once_with(
        message
    )
