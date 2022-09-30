from types import FunctionType

from console_bot.services.decorators import input_error
from console_bot.services.types import Command
from .register_handlers import ROUTE_MAP, Handler


def search_arguments(text: str) -> tuple[Handler, str | None]:
    data = ROUTE_MAP.get(text.lower())

    if data:
        return data, None
    
    command, *args = text.split(maxsplit=1)
    args = args[0] if args else None

    data = ROUTE_MAP.get(command.lower())

    if not data:
        raise ValueError(f"Sorry, but there is no '{command}' command\n"
                         f"Type 'help' command to see all available commands")
    return data, args


@input_error
def text_parsing(text: str) -> tuple[FunctionType, Command | None]:
    data, args = search_arguments(text)

    if not data.command_object:
        return data.handler, None

    if not args:
        if data.quantity_arg == 1:
            raise ValueError("Enter user name")
        raise ValueError("Give me name and phone please")

    args = args.rsplit(maxsplit=2)

    args = args + [''] if (len(args) < 2) and (len(args) == data.quantity_arg) else args

    _command: Command = data.command_object

    try:
        _args = _command(*args)
    except TypeError:
        raise ValueError("Please tell me your name and phone number, separated by a space")

    return data.handler, _args
    