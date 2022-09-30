from types import FunctionType
from typing import Optional

from console_bot.services.types import Command

ROUTE_MAP = {}


class Handler:

    def __init__(self,
                 handler: FunctionType,
                 command_object: Optional[Command] = None,
                 quantity_arg: int = 0) -> None:
        self.handler: FunctionType = handler
        self.command_object: Optional[Command] = command_object
        self.quantity_arg: int = quantity_arg

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ', '.join([f"{k}={v.__name__ if isinstance(v, FunctionType) else v}"
                                          for k, v in self.__dict__.items()]))


def register_message_handler(func: FunctionType, commands: str | list, quantity_arg: int = 0) -> FunctionType:
    if isinstance(commands, str):
        commands = [commands]

    for command in commands:
        command_object = Command if quantity_arg else None

        ROUTE_MAP.update({command: Handler(handler=func, command_object=command_object, quantity_arg=quantity_arg)})

    return func
