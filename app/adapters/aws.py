import boto3
import logging

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

    def __init__(self, topic: str):
        self.topic = topic

    def publish(self, cmd: commands.Command):
        # logger.info(f'topic: {config.SNS_COMMANDS_TOPIC_ARN}')
        msg = dict(
            # TopicArn=config.SNS_COMMANDS_TOPIC_ARN,
            TopicArn=self.topic,
            # Message="Pippero",
            Message=cmd.json(),
            # MessageStructure='JSON',
            MessageAttributes={
                'type-command': {
                    'DataType': 'String',
                    'StringValue': type(cmd).__name__,
                }
            }
        )
        logger.info(f'{msg!r}')
        return sns_client.publish(**msg)


class SNSMessageHandler:

    def __init__(self, bus: messagebus.MessageBus):
        self.messagebus = bus

    def dispatch(self, event: dict):
        records = event.get('Records', [])
        logger.info(f'received {len(records)} records')

        for record in records:
            message = record.get('Sns')
            if message:
                msg_attributes = message.get('MessageAttributes')
                logger.info(f'dispatching {msg_attributes}')

                if 'type-command' in msg_attributes:
                    cmd_name = msg_attributes.get('type-command').get('Value')

                    logger.info(f'cmds {cmd_name}')
                    if cmd_name in cmds:
                        logger.info(f'ok cmd {cmd_name}')

                        cmd = cmds[cmd_name].parse_raw(
                            message.get('Message'),
                        )
                        logger.info(f'dispatching command {cmd} to the bus')
                        self.messagebus.handle(cmd)
                    else:
                        logger.info(f'No command found for {cmd_name}')
