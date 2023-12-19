from helpers.address_book import AddressBook, Record
from prettytable import PrettyTable


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return f"Contact with the name {e} doesn't exists. Use 'add [name] [new_phone]' to add."
        except IndexError:
            return "Invalid command format. Use 'phone [name]' to get contact number."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    return inner


@input_error
def add_contact(args, book):
    if len(args) == 2:
        name, phone = args
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    else:
        raise ValueError(
            "Invalid command format. Use '[name] [phone]' as command arguments."
        )


@input_error
def change_contact(args, book):
    if len(args) == 2:
        name, new_phone = args
        record = book.find(name)
        if record:
            record.edit_phone(record.phones[0].value, new_phone)
            return "Contact updated."
        else:
            raise KeyError(name)
    else:
        raise ValueError(
            "Invalid command format. Use '[name] [phone]' as command arguments."
        )


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return record.phones[0].value
    else:
        raise KeyError(name)


@input_error
def show_all(book):
    if book.data.values():
        table = PrettyTable()
        table.field_names = ["Name", "Phones", "Address", "Birthday", "Notes"]
        table.align = "l"

        for record in book.data.values():
            phones_str = ", ".join(p.value for p in record.phones)
            notes_str = ", ".join(n.value for n in record.notes)
            address_str = (
                record.address.value
                if hasattr(record, "address") and record.address
                else ""
            )
            birthday_str = (
                record.birthday.value
                if hasattr(record, "birthday") and record.birthday
                else ""
            )

            table.add_row(
                [record.name.value, phones_str, address_str, birthday_str, notes_str]
            )

        print(table)
    else:
        print("No contacts available.")


@input_error
def add_birthday(name, birthday, book):
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError(name)


@input_error
def show_birthday(args, book):
    if len(args) == 1:
        name = args[0]
        record = book.find(name)
        if record and record.birthday:
            return record.birthday.value
        else:
            raise KeyError(name)
    else:
        raise ValueError(
            "Invalid command format. Use 'show-birthday [name]' to get the contact's birthday."
        )


@input_error
def add_address(name, address, book):
    record = book.find(name)
    if record:
        record.add_address(address)
        return "Address added."
    else:
        raise KeyError(name)


@input_error
def edit_address(name, new_address, book):
    record = book.find(name)
    if record:
        record.edit_address(new_address)
        return "Address updated."
    else:
        raise KeyError(name)


@input_error
def remove_address(name, book):
    record = book.find(name)
    if record:
        record.remove_address()
        return "Address removed."
    else:
        raise KeyError(name)


@input_error
def add_note(name, note, book):
    record = book.find(name)
    if record:
        record.add_note(note)
        return "Note added."
    else:
        raise KeyError(name)


def main():
    try:
        book = AddressBook()
        book.load_from_file("address_book.dat")
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "all":
                show_all(book)
            elif command == "add-birthday":
                name = input("Please enter contact name: ")
                birthday = input("Please enter contact's birthday: ")
                print(add_birthday(name, birthday, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                # Default to 7 days if no argument provided
                days = int(args[0]) if args else 7
                print(book.birthdays(days))
            elif command == "add-address":
                name = input("Please enter contact name: ")
                address = input("Please enter contact's address: ")
                print(add_address(name, address, book))
            elif command == "edit-address":
                name = input("Please enter contact name: ")
                new_address = input("Please enter new address: ")
                print(edit_address(name, new_address, book))
            elif command == "remove-address":
                name = input("Please enter contact name: ")
                print(remove_address(name, book))
            elif command == "add-note":
                name = input("Please enter contact name: ")
                note = input("Please enter note text: ")
                print(add_note(name, note, book))
            else:
                print("Invalid command.")
    finally:
        book.save_to_file("address_book.dat")


if __name__ == "__main__":
    main()
