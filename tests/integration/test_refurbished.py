import decimal

from refurbished.parser import Product

from app.adapters import apple, slack
from app.domain import commands, model
from app.services import messagebus


def test_available_products(
    mocker,
    messagebus: messagebus.MessageBus,
    refurbished_adapter: apple.RefurbishedStoreAdapter,
    slack_adapter: slack.SlackAdapter,
):
    mocker.patch.object(refurbished_adapter, "search")
    refurbished_adapter.search.side_effect = [
        [
            Product(
                name="iPad Wi-Fi + Cellular 32GB ricondizionato",
                family="ipad",
                url="https://www.apple.com/it/shop/product/FR7K2TY/A/ipad-wifi-32gb",
                price=decimal.Decimal("419.00"),
                previous_price=decimal.Decimal("489.00"),
                savings_price=decimal.Decimal("70.00"),
            ),
            Product(
                name="iPad Wi-Fi + Cellular 128GB ricondizionato",
                family="ipad",
                url="https://www.apple.com/it/shop/product/FR7K2TY/A/ipad-wifi-cellular-128gb",
                price=decimal.Decimal("499.00"),
                previous_price=decimal.Decimal("499.00"),
                savings_price=decimal.Decimal("0.00"),
            ),
        ]
    ]

    mocker.patch.object(slack_adapter, "post_message")
    slack_adapter.post_message.side_effect = [None]

    cmd = commands.CheckRefurbished(store="it", products=["ipad"])

    messagebus.handle(cmd, {})

    message = {
        "text": """
Found 2 ipad(s):

- <https://www.apple.com/it/shop/product/FR7K2TY/A/ipad-wifi-32gb|iPad Wi-Fi + Cellular 32GB ricondizionato> at ~489.00~ *419.00* (-70.00)
- <https://www.apple.com/it/shop/product/FR7K2TY/A/ipad-wifi-cellular-128gb|iPad Wi-Fi + Cellular 128GB ricondizionato> at *499.00*

"""
    }
    slack_adapter.post_message.assert_called_once_with(message, {})


def test_unavailable_products(
    mocker,
    messagebus: messagebus.MessageBus,
    refurbished_adapter: apple.RefurbishedStoreAdapter,
    slack_adapter: slack.SlackAdapter,
):
    mocker.patch.object(refurbished_adapter, "search")
    refurbished_adapter.search.side_effect = [[]]

    mocker.patch.object(slack_adapter, "post_message")
    slack_adapter.post_message.side_effect = [None]

    cmd = commands.CheckRefurbished(store="it", products=["ipad"])

    messagebus.handle(cmd, {})

    message = {"text": "Hey, can't find any 'ipad' in the 'it' store now 🤔"}
    slack_adapter.post_message.assert_called_once_with(message, {})
