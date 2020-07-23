from typing import Callable, Dict, List, Type
from app.domain import commands, events
from app.services import unit_of_work


class MessageBus:

    def __init__(
        self,
        uow: unit_of_work.UnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],
        command_handlers: Dict[Type[commands.Command], Callable]
    ):
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.uow = uow

    def handle(self, message):
        self.queue = [message]

        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                self._handle_event(message)
            if isinstance(message, commands.Command):
                self._handle_command(message)

    def _handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            handler(event, self.uow)

    def _handle_command(self, command: commands.Command):
        handler = self.command_handlers[type(command)]
        events = handler(command, self.uow)
        self.queue.extend(events)
