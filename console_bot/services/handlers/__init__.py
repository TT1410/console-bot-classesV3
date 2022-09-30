# from console_bot.services.utils import register_message_handler
from .handlers import (
    hello,
    add_user,
    add_phone,
    change_phone,
    remove_phone,
    user_phone,
    show_all_users,
    close_bot,
    help_command
)


# register_message_handler(hello, 'hello')
# register_message_handler(add_user, 'add', 3)
# register_message_handler(add_phone, 'add-phone', 2)
# register_message_handler(change_phone, 'change-phone', 2)
# register_message_handler(remove_phone, 'remove-phone', 1)
# register_message_handler(user_phone, 'phone', 1)
# register_message_handler(show_all_users, 'show all')
# register_message_handler(close_bot, ["good bye", "close", "exit"])
# register_message_handler(help_command, "help")
