from typing import Optional

from console_bot.services.decorators import input_error, route
from console_bot.services.types import Command
from console_bot.services.utils import ADDRESS_BOOK, Record, Phone, ROUTE_MAP


@route("hello")
def hello() -> str:
    """
    Отвечает в консоль "How can I help you?"
    """
    return "\nHow can I help you?"


@route("add", 3)
@input_error
def add_user(command: Command) -> str:
    """
    По этой команде бот сохраняет в памяти новый контакт.
    Пользователь вводит команду add, имя, номер телефона и дату рождения, обязательно через пробел.
    Пример команды: add Taras 0961233214 15.10.1988
    """
    try:
        ADDRESS_BOOK().get_contact(command.name)
    except KeyError:
        pass
    else:
        raise ValueError(f"\nContact with the name {command.name} already exists. "
                         f"To add a new number to an existing contact, use the <change> command.")

    ADDRESS_BOOK().add_record(Record(**command.__dict__))

    return f"\nSuccessfully created a new contact '{command.name}'"


@route("remove", 1)
@input_error
def remove_user(command: Command) -> str:
    """
    По этой команде бот удаляет контакт.
    Пользователь вводит команду remove и имя, обязательно через пробел.
    Пример команды: remove Taras
    """
    contact = ADDRESS_BOOK().get_contact(command.name)

    ADDRESS_BOOK().change_contact(contact, remove=True)  # Temporary command due to impossibility to change object in the file

    return f"\nSuccessfully deleted contact '{command.name}'"


@route('add-phone', 2)
@input_error
def add_phone(command: Command) -> str:
    """
    По этой команде бот сохраняет в памяти новый номер телефона для существующего контакта.
    Пользователь вводит команду add-phone, имя и новый номер телефона, обязательно через пробел.
    Пример команды: add-phone Taras 0961233032
    """
    contact = ADDRESS_BOOK().get_contact(command.name)

    phone = contact.add_phone(command.phone)

    ADDRESS_BOOK().change_contact(contact)  # Temporary command due to impossibility to change object in the file

    return f"\nContact phone number {command.name} '{phone.value}' successfully added"


@route("change-phone", 2)
@input_error
def change_phone(command: Command) -> Optional[str]:
    """
    По этой команде бот заменяет старый номер телефона новым для существующего контакта.
    Пользователь вводит команду change-phone, имя и новый номер телефона, обязательно через пробел.
    Далее пользователю будет предложено выбрать из списка номер, который необходимо заменить новым.
    Пример команды: change-phone Taras 0961233789
    """
    contact = ADDRESS_BOOK().get_contact(command.name)

    while True:
        print(user_phone(command))

        try:
            index = int(input("Enter the index number of the phone from the list you want to replace: "))
        except ValueError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")
            continue

        if index == 0:
            return

        try:
            old_phone, new_phone = contact.replace_phone(index, command.phone)
        except IndexError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")
        else:
            break

    ADDRESS_BOOK().change_contact(contact)  # Temporary command due to impossibility to change object in the file

    return f"\nContact phone number {command.name} '{old_phone.value}' " \
           f"has been successfully replaced by '{new_phone.value}'"


@route("remove-phone", 1)
@input_error
def remove_phone(command: Command) -> Optional[str]:
    """
    По этой команде бот удаляет номер телефона существующего контакта.
    Пользователь вводит команду change, имя и номер телефона, который необходимо удалить, обязательно через пробел.
    Пользователь может не вводить номер телефона, тогда ему будет предложено выбрать номер из списка.
    Пример команды: remove-phone Taras 0961233214
    """
    contact = ADDRESS_BOOK().get_contact(command.name)

    index = None

    if command.phone:
        _phone = Phone(command.phone)

        for num, phone in enumerate(contact.phones, 1):
            if _phone.value == phone.value:
                index = num
                break

    while True:
        if not index:
            print(user_phone(command))
            index = None

            try:
                index = int(input("Enter the index number of the phone from the list you want to replace: "))
            except ValueError:
                print("\nChoose a number from the list!")
                print("\n(Enter 0 to cancel)")
                continue

        if index == 0:
            return

        try:
            old_phone = contact.remove_phone(index)
        except IndexError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")
        else:
            break

    ADDRESS_BOOK().change_contact(contact)  # Temporary command due to impossibility to change object in the file

    return f"\nContact phone number {command.name} '{old_phone.value}' deleted successfully"


@route("phone", 1)
@input_error
def user_phone(command: Command) -> str:
    """
    По этой команде бот выводит в консоль номера телефонов для указанного контакта.
    Пользователь вводит команду phone и имя контакта, чьи номера нужно показать, обязательно через пробел.
    Пример команды: phone Taras
    """
    contact = ADDRESS_BOOK().get_contact(command.name)

    return (f"Phone numbers of {command.name}\n\t" +
            "\n\t".join([f"{num}. {x.value}" for num, x in enumerate(contact.phones, 1)]))


@route("change-bd", 1)
@input_error
def change_birthday(command: Command):
    """
    По этой команде изменяет день рождения для существующего контакта.
    Пользователь вводит команду change-bd и имя обязательно через пробел.
    Пример команды: change-bd Taras
    """
    contact = ADDRESS_BOOK().get_contact(command.name)

    birthday = input(f"Enter the date of birth of the contact '{command.name}' in the format YYYY.MM.DD or DD.MM.YYYY: ")

    contact.change_birthday(birthday)

    ADDRESS_BOOK().change_contact(contact)  # Temporary command due to impossibility to change object in the file

    return f"\nDate of birth {contact.birthday.value} of the contact '{command.name}' successfully saved"


@route("days-bd", 1)
@input_error
def days_before_birthday(command: Command):
    """
    По этой команде бот выводит в консоль, сколько осталось дней до дня рождения контакта.
    Пользователь вводит команду days-bd и имя контакта, обязательно через пробел.
    Пример команды: days-bd Taras
    """
    days = ADDRESS_BOOK().get_contact(command.name).days_to_birthday()

    return f"Until the birthday of {command.name} {days} days" if days else \
        f"Contact '{command.name}' does not have a birthday recorded. " \
        f"To add or change a contact's birthday, use the <change-bd>"


@route("show all")
@input_error
def show_all_users() -> str:
    """
    По этой команде бот выводит все сохраненные контакты с номерами телефонов и датами рождений в консоль.
    """
    format_users = []

    for contact in ADDRESS_BOOK().iterator(1):
        contact = contact[0]

        phones = ', '.join([str(x.value) for x in contact.phones])
        birthday = contact.birthday.value if contact.birthday else '–'

        format_users.append(f"{contact.name.value:<10} : {birthday} : {phones:^12}")

    return '\n'.join(format_users)


@route("search-contact", 1)
def search_contacts(command: Command) -> str:
    """
    По этой команде бот выводит в консоль всех контактов, у которых есть совпадение со строкой поиска в имени, или номере.
    Пользователь вводит команду days-bd и имя контакта, обязательно через пробел.
    Пример команды: search-contact Tar
    """
    format_contacts = []

    search = command.name

    for contact in ADDRESS_BOOK().iterator(1):
        contact = contact[0]

        if search is None or search in contact.name.value \
                or any(search in str(x.value) for x in contact.phones):

            phones = ', '.join([str(x.value) for x in contact.phones])
            birthday = contact.birthday.value if contact.birthday else '–'

            format_contacts.append(f"{contact.name.value:<10} : {birthday} : {phones:^12}")

    return '\n'.join(format_contacts)


@route("help")
def help_command() -> str:
    """
    Выводит список доступных команд
    """
    bot_commands = {}

    for key, value in ROUTE_MAP.items():

        if value.handler in bot_commands:
            bot_commands[value.handler] += f", {key}"
        else:
            bot_commands[value.handler] = key

    return '\n'.join([s for s in [cmd + func.__doc__ for func, cmd in bot_commands.items()]])


@route(["good bye", "close", "exit"])
def close_bot() -> str:
    """
    По любой из команд: "good bye", "close", "exit",
    бот завершает свою роботу после того, как выведет в консоль "Good bye!".
    """
    return "Good bye!"
