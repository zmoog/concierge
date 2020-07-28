import json
from datetime import date
# from urllib.parse import parse_qs

from app import bootstrap
from app.adapters import slack
from app.domain import commands, model


messagebus = bootstrap.for_lambda()

whens = {
    'today': date.today,
    'previous_business_day': model.find_previous_business_day
}


handler = slack.SlashCommandHandler()


@handler.route(
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


@handler.route(
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
    print(json.dumps(event))
    return handler.handle(event['body'], event['headers'])
