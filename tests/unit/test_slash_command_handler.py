from app.adapters.slack import SlashCommandDispatcher


dispatcher = SlashCommandDispatcher()


@dispatcher.route(
    "/refurbished",
    text_regex="(?P<store>it|us) (?P<product>ipad|iphone|mac)"
)
def check_refurbished(store: str, product: str):
    assert store == 'it'
    assert product == 'mac'


def test_simple_command(from_json):
    event = from_json(
        'tests/data/aws/lambda/events/api-gateway/slack/slash-commands/dm.json'
    )

    respo = dispatcher.dispatch(event["body"], event["headers"])

    assert respo['statusCode'] == 200
