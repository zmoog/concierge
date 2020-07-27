import decimal

from refurbished.parser import Product

from app.entrypoints.aws_lambda import run_slash_command
from app.bootstrap import refurbished_adapter, slack_adapter


# def test_slash_commands_with_a_bad_token(from_json):
#     # setup event from the AWS lambda proxy
#     event = from_json(
#         'tests/data/aws/lambda/events/api-gateway/slack/slash-commands/bad-token.json'
#     )

#     resp = run_slash_command(event, None)

#     assert 'statusCode' in resp
#     assert resp['statusCode'] == 403


def test_slash_commands_from_a_dm(
    mocker,
    from_json,
):
    # setup event from the AWS lambda proxy
    event = from_json(
        'tests/data/aws/lambda/events/api-gateway/slack/slash-commands/dm.json'
    )

    # setup fake response from Apple Store and spy on Slack adapters
    # spy = mocker.spy(slack_adapter, "post_message")
    mocker.patch.object(slack_adapter, "post_message")
    mocker.patch.object(refurbished_adapter, "search")
    refurbished_adapter.search.side_effect = [[
        Product(
            name='iPad Wi-Fi + Cellular 32GB ricondizionato',
            price=decimal.Decimal('419.00'),
            previous_price=decimal.Decimal('489.00'),
            savings_price=decimal.Decimal('70.00')
        )]]

    resp = run_slash_command(event, None)

    assert 'statusCode' in resp
    assert resp['statusCode'] == 200

    message = {
        'text': '\nFound 1 ipad(s):\n\n- iPad Wi-Fi + Cellular 32GB ricondizionato at ~489.00~ *419.00* (-70.00)\n\n'
    }
    slack_adapter.post_message.assert_called_once_with(
        message
    )
