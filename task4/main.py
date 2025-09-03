
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            # Show function-provided message if any
            return str(e) or "Invalid value."
        except KeyError as e:
            # Expect KeyError(name)
            name = e.args[0] if e.args else "unknown"
            return f"Contact '{name}' not found."
        except IndexError:
            return "Not enough arguments. Type 'help' for usage."
    return inner

def parse_input(user_input: str):
    if not user_input or not user_input.strip():
        return None, []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts: dict[str, str]) -> str:
    if len(args) != 2:
        raise ValueError("Usage: add <name> <phone>")
    name, phone = args

    if name in contacts:
        return f"Contact '{name}' already exists. Use 'change {name} <phone>' to update."
    contacts[name] = phone
    return f"Added: {name} → {phone}"

@input_error
def change_contact(args, contacts: dict[str, str]) -> str:
    if len(args) != 2:
        raise ValueError("Usage: change <name> <new_phone>")
    name, phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return f"Changed: {name} → {phone}"

@input_error
def show_phone(args, contacts: dict[str, str]) -> str:
    if len(args) != 1:
        raise ValueError("Usage: phone <name>")
    name = args[0]
    if name not in contacts:
        raise KeyError(name)
    return contacts[name]

def show_all(contacts: dict[str, str]) -> dict | str:
    if not contacts:
        return "No contacts yet."
    return contacts

def help_text() -> str:
    return (
        "Available commands:\n"
        "  hello                       – greet\n"
        "  add <name> <phone>          – add a contact (name may be quoted)\n"
        "  change <name> <new_phone>   – change phone for existing contact\n"
        "  phone <name>                – show phone by name\n"
        "  all                         – list all contacts\n"
        "  help                        – show this help\n"
        "  exit | close                – quit"
    )

def main():
    contacts: dict[str, str] = {}
    print("Welcome to the assistant bot! Type 'help' for commands.")
    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nGood bye!")
            break

        command, *args = parse_input(user_input)

        match command: 
            case "hello":
                print("How can I help you?")
            case "exit" | "close":
                print("Good bye!")
                break
            case "add":
                print(add_contact(args, contacts))
            case "change":
                print(change_contact(args, contacts))
            case "phone":
                print(show_phone(args, contacts))
            case "all":
                print(show_all(contacts))
            case "help":
                print(help_text())
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()