import decimal
# import pytest
# from app import bootstrap

from refurbished.parser import Product

from app.adapters import apple, slack
from app.domain import commands, events
from app.services import handlers, messagebus


# @pytest.fixture
# def bus():
#     bus = bootstrap.for_cli()
#     yield bus


def test_available_products(
    mocker,
    uow,
    refurbished_adapter: apple.RefurbishedStoreAdapter
):
    # summary = from_json("tests/data/toggl/summary-2020-07-19.json")
    mocker.patch.object(refurbished_adapter, "search")
    refurbished_adapter.search.side_effect = [[
        Product(
            name='iPad Wi-Fi + Cellular 32GB ricondizionato',
            url='https://www.apple.com/it/ipad-wifi-32gb',
            price=decimal.Decimal('419.00'),
            previous_price=decimal.Decimal('489.00'),
            savings_price=decimal.Decimal('70.00')
        ), 
        Product(
            name='iPad Wi-Fi + Cellular 128GB ricondizionato',
            url='https://www.apple.com/it/ipad-wifi-cellular-128gb',
            price=decimal.Decimal('499.00'),
            previous_price=decimal.Decimal('579.00'),
            savings_price=decimal.Decimal('80.00')
        )]]

    # bus.add_event_handler(type(cmd))
    cmd = commands.CheckRefurbished(store='it', products=['ipad'])
    actual_events = handlers.check_refurbished(cmd, uow, {})

    # print('actual_events', actual_events)
    assert actual_events, "no events generated"

    expected_events = [events.RefurbishedProductAvailable(text="""\
Found 2 ipad(s):

- iPad Wi-Fi + Cellular 32GB ricondizionato at ~489.00~ *419.00* (-70.00)
- iPad Wi-Fi + Cellular 128GB ricondizionato at ~579.00~ *499.00* (-80.00)
""")]
    assert actual_events == expected_events


def test_unavailable_products(
    mocker,
    messagebus: messagebus.MessageBus,
    refurbished_adapter: apple.RefurbishedStoreAdapter,
    slack_adapter: slack.SlackAdapter,
):
    mocker.patch.object(refurbished_adapter, "search")
    refurbished_adapter.search.side_effect = [[]]

    mocker.patch.object(slack_adapter, 'post_message')
    slack_adapter.post_message.side_effect = [None]

    cmd = commands.CheckRefurbished(store='it', products=['ipad'])

    messagebus.handle(cmd, {})

    message = {
        'text': "Hey, can't find any 'ipad' in the 'it' store now 🤔"
    }
    slack_adapter.post_message.assert_called_once_with(
        message, {}
    )
