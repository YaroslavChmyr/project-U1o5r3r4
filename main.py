from collections import Counter
from enum import Enum

from helpers.address_book import AddressBook, Record
from prettytable import PrettyTable


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return f"Contact with the name {e} doesn't exists. Use 'add-contact' to add."
        except IndexError:
            return "Invalid command format. Use 'phone [name]' to get contact number."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(name, book):
    record = Record(name)
    book.add_record(record)
    return "Contact added."


@input_error
def add_phone(name, phone, book):
    record = book.find(name)
    if record:
        record.add_phone(phone)
        return "Phone added."
    else:
        raise KeyError(name)


@input_error
def edit_phone(name, old_phone, new_phone, book):
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone updated."
    else:
        raise KeyError(name)


@input_error
def remove_phone(name, phone, book):
    record = book.find(name)
    if record:
        record.remove_phone(phone)
        return "Phone removed."
    else:
        raise KeyError(name)


@input_error
def show_phones(name, book):
    record = book.find(name)
    if record:
        return record.show_phones()
    else:
        raise KeyError(name)


@input_error
def show_all(book):
    if book.data.values():
        table = PrettyTable()
        table.field_names = ["Name", "Phones", "Address", "Birthday", "Note Title", "Note Content"]
        table.align = "l"

        for record in book.data.values():
            phones_str = "\n".join(p.value for p in record.phones)
            notes_str = ""
            notes_titles_str = ""
            for note in record.notes:
                for title, value in note.data.items():
                    if notes_str == "":
                        notes_str += value
                        notes_titles_str += title
                    else:
                        notes_str += f"\n{value}"
                        notes_titles_str += f"\n{title}"
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

            table.add_row([record.name.value, phones_str, address_str, birthday_str, notes_titles_str, notes_str], divider=True)

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
def show_birthday(name, book):
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value
    else:
        raise KeyError(name)


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
def add_note(name, title, note, book):
    record = book.find(name)
    if record:
        record.add_note(title, note)
        return "Note added."
    else:
        raise KeyError(name)


@input_error
def edit_note(name, title, new_note, book):
    record = book.find(name)
    if record:
        record.edit_note(title, new_note)
        return "Note updated."
    else:
        raise KeyError(name)


@input_error
def remove_note(name, title, book):
    record = book.find(name)
    if record:
        record.remove_note(title)
        return "Note removed."
    else:
        raise KeyError(name)
    

@input_error
def search_note(title, book):
    if book.data.values():
        table = PrettyTable()
        table.field_names = ["Contact Name", "Note Title", "Note Content"]
        table.align = "l"
        note_title, note, contact_name = book.search_note(title)
        table.add_row(
                [contact_name, note_title, note]
            )
        return table
    else:
        print("No notes available.")


@input_error
def add_tag(args, book: AddressBook):
    name, note_title, *tags = args

    record: Record = book.find(name)
    note = record.get_note(note_title)
    note.add_tag(tags)

    return "Tag was added successfully"


@input_error
def search_by_tags(args, book):
    name, *tags = args

    record: Record = book.find(name)
    notes = record.search_notes_by_tags(tags)
    tab = "\t"
    new_line = '\n'

    return f"Titles of found notes:\n{''.join([tab + ' - ' + note.title + new_line for note in notes])}"


class COMMANDS(str, Enum):
    CLOSE = "close"
    EXIT = "exit"
    HELLO = "hello"
    ALL = "all"

    ADD_CONTACT = "add-contact"

    ADD_PHONE = "add-phone"
    EDIT_PHONE = "edit-phone"
    REMOVE_PHONE = "remove-phone"
    SHOW_PHONES = "show-phones"

    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"
    GET_BIRTHDAYS_NEXT_WEAK = "birthdays"

    ADD_ADDRESS = "add-address"
    EDIT_ADDRESS = "edit-address"
    REMOVE_ADDRESS = "remove-address"

    ADD_NOTE = "add-note"
    EDIT_NOTE = "edit-note"
    REMOVE_NOTE = "remove-note"
    SEARCH_NOTE = "search-note"
    
    ADD_TAG = "add-tag"
    SEARCH_BY_TAGS = "search-by-tags"



def search_nearest_command(command: str):
    command = Counter(command)
    commands = [(i.value, Counter(i.value)) for i in COMMANDS]
    commands.sort(
        key=lambda main_command: ((main_command[1] | command) - (main_command[1] & command)).total()
    )
    return commands[0][0]


def main():
    try:
        book = AddressBook()
        book.load_from_file("address_book.dat")
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)
            try:
                command = COMMANDS(command)
            except ValueError:
                print("Invalid command. ")
                print(f"The most similar command is '{search_nearest_command(command)}'")
                continue

            command = COMMANDS(command)

            if command in [COMMANDS.CLOSE, COMMANDS.EXIT]:
                print("Good bye!")
                break
            elif command == COMMANDS.HELLO:
                print("How can I help you?")
            elif command == COMMANDS.ALL:
                show_all(book)
            elif command == COMMANDS.ADD_CONTACT:
                name = input("Please enter contact name: ")
                print(add_contact(name, book))
            elif command == COMMANDS.ADD_PHONE:
                name = input("Please enter contact name: ")
                phone = input("Please enter contact's phone: ")
                print(add_phone(name, phone, book))
            elif command == COMMANDS.EDIT_PHONE:
                name = input("Please enter contact name: ")
                old_phone = input("Please enter phone: ")
                new_phone = input("Please enter new phone: ")
                print(edit_phone(name, old_phone, new_phone, book))
            elif command == COMMANDS.REMOVE_PHONE:
                name = input("Please enter contact name: ")
                phone = input("Please enter phone number to remove: ")
                print(remove_phone(name, phone, book))
            elif command == COMMANDS.SHOW_PHONES:
                name = input("Please enter contact name: ")
                print(show_phones(name, book))
            elif command == COMMANDS.ADD_BIRTHDAY:
                name = input("Please enter contact name: ")
                birthday = input("Please enter contact's birthday: ")
                print(add_birthday(name, birthday, book))
            elif command == COMMANDS.SHOW_BIRTHDAY:
                name = input("Please enter contact name: ")
                print(show_birthday(name, book))
            elif command == COMMANDS.GET_BIRTHDAYS_NEXT_WEAK:
                # Default to 7 days if no argument provided
                days = int(args[0]) if args else 7
                print(book.birthdays(days))
            elif command == COMMANDS.ADD_ADDRESS:
                name = input("Please enter contact name: ")
                address = input("Please enter contact's address: ")
                print(add_address(name, address, book))
            elif command == COMMANDS.EDIT_ADDRESS:
                name = input("Please enter contact name: ")
                new_address = input("Please enter new address: ")
                print(edit_address(name, new_address, book))
            elif command == COMMANDS.REMOVE_ADDRESS:
                name = input("Please enter contact name: ")
                print(remove_address(name, book))
            elif command == COMMANDS.ADD_NOTE:
                name = input("Please enter contact name: ")
                title = input("Please enter note title: ")
                note = input("Please enter note text: ")
                print(add_note(name, title, note, book))
            elif command == COMMANDS.EDIT_NOTE:
                name = input("Please enter contact name: ")
                title = input("Please enter note title: ")
                new_note = input("Please enter text for a new note: ")
                print(edit_note(name, title, new_note, book))
            elif command == COMMANDS.REMOVE_NOTE:
                name = input("Please enter contact name: ")
                title = input("Please enter note title: ")
                print(remove_note(name, title, book))
            elif command == COMMANDS.ADD_TAG:
                print(add_tag(args, book))
            elif command == COMMANDS.SEARCH_BY_TAGS:
                print(search_by_tags(args, book))
            elif command == COMMANDS.SEARCH_NOTE:
                title = input("Please enter note title: ")
                print(search_note(title, book))
    finally:
        book.save_to_file("address_book.dat")


if __name__ == "__main__":
    main()
