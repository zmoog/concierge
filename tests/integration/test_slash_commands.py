import decimal
import logging

from refurbished.parser import Product

from app.entrypoints.aws_lambda import run_slash_command
from app.bootstrap import refurbished_adapter, slack_adapter


def test_slash_commands_with_an_invalid_token(from_json):
    # setup event from the AWS lambda proxy
    event = from_json(
        'tests/data/aws/lambda/events/api-gateway/slack/slash-commands/\
invalid-token.json'
    )

    resp = run_slash_command(event, None)

    assert 'statusCode' in resp
    assert resp['statusCode'] == 401


def test_slash_commands_from_a_dm(
    mocker,
    from_json,
    caplog,
):
    caplog.set_level(logging.INFO)

    # setup event from the AWS lambda proxy
    event = from_json(
        'tests/data/aws/lambda/events/api-gateway/slack/slash-commands/dm.json'
    )

    # setup fake response from Apple Store and spy on Slack adapters
    # spy = mocker.spy(slack_adapter, "post_message")
    mocker.patch.object(slack_adapter, "post_message")
    slack_adapter.post_message.side_effect = [None]
    mocker.patch.object(refurbished_adapter, "search")
    refurbished_adapter.search.side_effect = [[
        Product(
            name='MacBook Air 13,3"',
            price=decimal.Decimal('939.00'),
            previous_price=decimal.Decimal('1109.00'),
            savings_price=decimal.Decimal('170.00')
        )]]

    resp = run_slash_command(event, None)

    assert 'statusCode' in resp
    assert resp['statusCode'] == 200

    message = {
        'text': """
Found 1 mac(s):

- MacBook Air 13,3" at ~1109.00~ *939.00* (-170.00)

"""
    }
    slack_adapter.post_message.assert_called_once_with(
        message
    )


def test_slash_commands_without_text(
    mocker,
    from_json,
):
    # setup event from the AWS lambda proxy
    event = from_json(
        'tests/data/aws/lambda/events/api-gateway/slack/slash-commands/\
no-text.json'
    )
    mocker.patch.object(slack_adapter, "post_message")

    resp = run_slash_command(event, None)

    assert 'statusCode' in resp
    assert resp['statusCode'] == 200


def test_slash_commands_with_unexpected_text(
    mocker,
    from_json,
    caplog,
):
    caplog.set_level(logging.INFO)

    # setup event from the AWS lambda proxy
    event = from_json(
        'tests/data/aws/lambda/events/api-gateway/slack/slash-commands/\
unexpected-text.json'
    )

    # setup fake response for Slack adapter
    mocker.patch.object(slack_adapter, "post_message")

    # run the command
    resp = run_slash_command(event, None)

    assert 'statusCode' in resp
    assert resp['statusCode'] == 200
    assert 'body' in resp
    assert resp['body'] == '{\
"response_type": "ephemeral", \
"text": "I don\'t know how to handle your request \
\\u00af\\\\_(\\u30c4)_/\\u00af\
"}'
