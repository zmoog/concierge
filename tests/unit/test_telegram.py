import logging
import os

import pytest

from app.adapters.telegram import TelegramAdapter


external_access = pytest.mark.skipif(
    os.environ.get('E2E', '') != 'yes', reason='E2E tests are not enabled'
)


@external_access
def test_send_message_on_a_telegram_group(
    telegram_adapter: TelegramAdapter,
    caplog
):
    caplog.set_level(logging.INFO)
    telegram_adapter.send("Hello world from Concierge bot 🍺")
