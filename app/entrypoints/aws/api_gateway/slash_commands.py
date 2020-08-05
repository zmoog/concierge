import json
import logging
from typing import Any

from datetime import date

from app import config
from app.adapters import aws, slack
from app.domain import commands

app_logger = logging.getLogger()
app_logger.setLevel(config.LOG_LEVEL)

logger = logging.getLogger(__name__)


dispatcher = slack.SlashCommandDispatcher()
sns = aws.SNSCommandPublisher(
    config.SNS_COMMANDS_TOPIC_ARN,
)


@dispatcher.route(
    "/refurbished",
    text_regex="(?P<store>it|us|uk|au) (?P<product>ipad|iphone|mac)"
)
def check_refurbished(store: str, product: str):
    resp = sns.publish(
        commands.CheckRefurbished(
            store=store,
            products=[product]
        )
    )
    logger.info(f'publish: {resp}')


@dispatcher.route(
    "/summarize"
)
def summarize():
    resp = sns.publish(
        commands.Summarize(day=date.today())
    )
    logger.info(f'publish: {resp}')


def dispatch(event: dict, context: Any = None):
    """
    Handle the AWS Lambda event from the API Gateway carring the
    HTTP request from Slack for a slash command invoked by a user.
    """
    try:
        # dump the event in the log, it will be removed later
        # or replaced w/ an appropriate log level
        # logging.info(json.dumps(event))

        body, headers = event['body'], event['headers']

        # Checks if the request really come from Slack, see
        # https://api.slack.com/authentication/verifying-requests-from-slack
        # for more details
        slack.verify_signature(body, headers)

        # create a new /command using the payload
        # from Slack
        slash_command = slack.build_slash_command(body)

        # dispatch the /command to invoke the most
        # appropriate business command
        dispatcher.dispatch(slash_command)

        return build_proxy_response(200, body={'text': 'On it!'})

    except slack.RouteNotFound as e:
        logger.warning(e)
        return build_proxy_response(
            200,
            body={
                'response_type': 'ephemeral',
                'text': 'I don\'t know how to handle your request ¯\\_(ツ)_/¯'
            }
        )
    except slack.InvalidSignature:
        return build_proxy_response(401)


def build_proxy_response(
    status_code: int,
    body=None
):
    resp = {
        'statusCode': status_code
    }
    if body:
        resp['body'] = json.dumps(body)

    return resp
