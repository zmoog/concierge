from typing import Any, Dict

from app.adapters.slack import build_slash_command, SlashCommandDispatcher


dispatcher = SlashCommandDispatcher()


@dispatcher.route(
    "/refurbished",
    text_regex="(?P<store>it|us) (?P<product>ipad|iphone|mac)"
)
def check_refurbished(context: Dict[str, Any], store: str, product: str):
    assert store == 'it'
    assert product == 'mac'


def test_simple_command(from_json):
    event = from_json(
        'tests/data/aws/lambda/events/api-gateway/slack/slash-commands/dm.json'
    )

    dispatcher.dispatch(
        build_slash_command(event["body"]), {}
    )

    # should not raise any exception
