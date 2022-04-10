from datetime import datetime

from app.adapters import classeviva, telegram
from app.domain.commands.school import ListHomework
from app.domain.model.school import Assignment
from app.services import messagebus


def test_no_homework(
    mocker,
    messagebus: messagebus.MessageBus,
    classeviva_adapter: classeviva.ClassevivaAdapter,
    telegram_adapter: telegram.TelegramAdapter,
):
    mocker.patch.object(classeviva_adapter, "list_assignments")
    classeviva_adapter.list_assignments.side_effect = [
        [
            # Product(
            #     name="iPad Wi-Fi + Cellular 32GB ricondizionato",
            #     family="ipad",
            #     url="https://www.apple.com/it/shop/product/FR7K2TY/A/ipad-wifi-32gb",  # noqa: E501
            #     price=decimal.Decimal("419.00"),
            #     previous_price=decimal.Decimal("489.00"),
            #     savings_price=decimal.Decimal("70.00"),
            # ),
            # Product(
            #     name="iPad Wi-Fi + Cellular 128GB ricondizionato",
            #     family="ipad",
            #     url="https://www.apple.com/it/shop/product/FR7K2TY/A/ipad-wifi-cellular-128gb",  # noqa: E501
            #     price=decimal.Decimal("499.00"),
            #     previous_price=decimal.Decimal("499.00"),
            #     savings_price=decimal.Decimal("0.00"),
            # ),
        ]
    ]

    mocker.patch.object(telegram_adapter, "send_message")
    telegram_adapter.send_message.side_effect = [None]

    cmd = ListHomework(days=5)

    messagebus.handle(cmd, {})

    message = "No homework for the next 5 days"
    group_id = "161035319"
    telegram_adapter.send_message.assert_called_once_with(message, group_id)


def test_homework_available(
    mocker,
    messagebus: messagebus.MessageBus,
    classeviva_adapter: classeviva.ClassevivaAdapter,
    telegram_adapter: telegram.TelegramAdapter,
):
    mocker.patch.object(classeviva_adapter, "list_assignments")
    classeviva_adapter.list_assignments.side_effect = [
        [
            Assignment(
                id=1,
                teacher="PESANDO MARGHERITA",
                notes="Terminare l’ex 4 di pag 95 + ex 5 and 6",
                starts_at=datetime(2022, 4, 11),
                ends_at=datetime(2022, 4, 11),
            ),
            Assignment(
                id=1,
                teacher="DICEMBRE ELISA",
                notes="CONSEGNA E CORREZIONE VERIFICA GRAMMATICA",
                starts_at=datetime(2022, 4, 12),
                ends_at=datetime(2022, 4, 12),
            ),
        ]
    ]

    mocker.patch.object(telegram_adapter, "send_message")
    telegram_adapter.send_message.side_effect = [None]

    cmd = ListHomework(days=5)
    messagebus.handle(cmd, {})

    message = """Here's the homework for the next 5 days:

2022-04-11
- PESANDO MARGHERITA, Terminare l’ex 4 di pag 95 + ex 5 and 6

2022-04-12
- DICEMBRE ELISA, CONSEGNA E CORREZIONE VERIFICA GRAMMATICA

"""
    group_id = "161035319"
    telegram_adapter.send_message.assert_called_once_with(message, group_id)
