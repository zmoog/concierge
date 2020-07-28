import json
from datetime import date

from app import bootstrap
from app.adapters import slack
from app.domain import commands, model


messagebus = bootstrap.for_lambda()

whens = {
    'today': date.today,
    'previous_business_day': model.find_previous_business_day
}


dispatcher = slack.SlashCommandDispatcher()


@dispatcher.route(
    "/refurbished",
    text_regex="(?P<store>it|us) (?P<product>ipad|iphone|mac)"
)
def check_refurbished(store: str, product: str):
    messagebus.handle(
        commands.CheckRefurbished(
            store=store,
            products=[product]
        )
    )


@dispatcher.route(
    "/summarize"
)
def summarize():
    messagebus.handle(
        commands.Summarize(day=date.today())
    )


def run_scheduled(event, config):
    print(f'running run_scheduled with event {event}')
    if 'Summarize' in event:
        when = event['Summarize'].get('when', 'today')

        if when not in whens:
            print(f'"{when}" is not a supported "when" value ({whens.keys()})')
            return

        day = whens[when]()
        print(f'summarizing {day}')
        cmd = commands.Summarize(day=day)
    elif 'CheckRefurbished' in event:
        cmd = commands.CheckRefurbished(
            store=event['CheckRefurbished'].get('store', 'it'),
            products=event['CheckRefurbished']['products']
        )
    elif 'DownloadIFQ' in event:
        cmd = commands.DownloadIFQ(
            day=date.today()
        )
    else:
        return

    messagebus.handle(cmd)


def run_slash_command(event, context):
    try:
        print(json.dumps(event))
        body, headers = event['body'], event['headers']

        slack.verify_signature(body, headers)
        cmd = slack.build_slash_command(body)

        dispatcher.dispatch(cmd)

        return {
            'statusCode': 200
        }

    except slack.RouteNotFound:
        return {
            'statusCode': 404
        }
    except slack.InvalidSignature:
        return {
            'statusCode': 401
        }
