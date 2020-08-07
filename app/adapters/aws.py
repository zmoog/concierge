import boto3
import json
import logging
from typing import Any, Dict

# from app import config
from app.domain import commands
from app.services import messagebus

logger = logging.getLogger(__name__)

cmds = {
    'CheckRefurbished': commands.CheckRefurbished,
    'Summarize': commands.Summarize,
}


sns_client = boto3.client('sns')


class SNSCommandPublisher:
    """SNSCommandPublisher handle the publishing of application commands
    to a SNS topic for async processing.
    """

    def __init__(self, topic_arn: str):
        """
        The ``topic_arn`` is the ARN of the SNS topic to publish the
        commands into.
        """
        self.topic_arn = topic_arn

    def publish(self, cmd: commands.Command, context: Dict[str, Any]):
        """Publish a ``cmd`` command into the command SNS topic."""
        msg = dict(
            TopicArn=self.topic_arn,
            Message=cmd.json(),
            MessageAttributes={
                'type-command': {
                    'DataType': 'String',
                    'StringValue': type(cmd).__name__,
                },
                'context': {
                    'DataType': 'String',
                    'StringValue': json.dumps(context),
                }
            }
        )
        logger.info(f'{msg!r}')
        return sns_client.publish(**msg)


class SNSMessageHandler:
    """SNSMessageHandler handles the process of an event received
    from a SNS topic subscription."""
    def __init__(self, bus: messagebus.MessageBus):
        self.messagebus = bus

    def dispatch(self, event: dict):
        """Extract the commands from the record contained in the event
        received from the SNS topic.

        Each record is examined looking for a command. All the commands found
        are dispatched for execution.
        """
        records = event.get('Records', [])
        logger.info(f'received {len(records)} records')

        for record in records:
            message = record.get('Sns')
            if message:
                msg_attributes = message.get('MessageAttributes')
                logger.info(f'dispatching {msg_attributes}')

                if 'type-command' in msg_attributes:
                    cmd_name = msg_attributes.get('type-command').get('Value')
                    context = json.loads(
                        msg_attributes.get('context').get('Value'),
                    )

                    logger.info(f'cmds {cmd_name}')
                    if cmd_name in cmds:
                        logger.info(f'ok cmd {cmd_name}')

                        cmd = cmds[cmd_name].parse_raw(
                            message.get('Message'),
                        )
                        logger.info(f'dispatching command {cmd} to the bus')
                        self.messagebus.handle(cmd, context)
                    else:
                        logger.info(f'No command found for {cmd_name}')
