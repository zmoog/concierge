import requests


class TelegramAdapter:
    def __init__(self, token):
        self.token = token
        # self.chat_id = chat_id

    def send_message(self, msg: str, chat_id: str):
        params = {
            "text": msg,
            "chat_id": chat_id,
        }

        resp = requests.get(
            f"https://api.telegram.org/{self.token}/sendMessage", params=params
        )

        if resp.status_code != 200:
            raise TelegramError(
                f"message not sent: status_code {resp.status_code}"
            )


class TelegramError(Exception):
    pass
