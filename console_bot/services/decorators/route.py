from console_bot.services.utils import register_message_handler


def route(commands: str | list[str], quantity_arg: int = 0):
    def _route(f):
        register_message_handler(func=f, commands=commands, quantity_arg=quantity_arg)
        return f
    return _route
