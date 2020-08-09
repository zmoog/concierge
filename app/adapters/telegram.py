import logging
import requests

logger = logging.getLogger(__name__)


class TelegramAdapter:

    def __init__(self, token: str, default_chat_id: str):
        self.token = token
        self.default_chat_id = default_chat_id

    def send(self, msg: str, chat_id: str = None):
        """Sends a Telegram message to ``chat_id``."""
        params = {
            'chat_id': chat_id or self.default_chat_id,
            'text': msg
        }
        resp = requests.get(
            f'https://api.telegram.org/{self.token}/sendMessage',
            params=params
        )

        if resp.status_code != 200:
            raise Exception(
                'failed to send the Telegram message.'
                f' status_code: {resp.status_code},'
                f' text: {resp.text}'
            )
