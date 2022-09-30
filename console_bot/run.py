from console_bot.services.utils import text_parsing


def main() -> None:
    while True:
        text = input()

        result = text_parsing(text)

        if not result:
            continue

        func, args = result

        if not args:
            result = func()
        else:
            result = func(args)

        print(f"{result}\n" if result else '')

        if result == "Good bye!":
            break


if __name__ == '__main__':
    main()
