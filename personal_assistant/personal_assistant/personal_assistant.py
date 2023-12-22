from .address_book import AddressBook, Record
from prettytable import PrettyTable
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

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
            return f"Contact with the name {e} doesn't exists. Use 'add-contact' to add."
        except IndexError as e:
            return f"Index error occurred: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    inner.__doc__ = func.__doc__
    return inner


def check_name(name, book):
    if book.find(name) is None:
        raise KeyError(name)
    return True


@input_error
def add_contact(book):
    """
    Add a new contact.
    """
    name = input("Please enter contact name: ")
    if not name:
        raise ValueError("Contact name cannot be empty.")

    if book.find(name):
        return f"Contact with the name '{name}' already exists."
    else:
        record = Record(name)
        book.add_record(record)
        return f"Contact '{name}' added."

@input_error
def remove_contact(book):
    """
    Remove a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    book.delete(name)
    return f"Contact '{name}' removed."


@input_error
def add_phone(book):
    """
    Add a phone number to a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    phone = input("Please enter contact's phone: ")
    record = book.find(name)
    record.add_phone(phone)
    return "Phone added."


@input_error
def edit_phone(book):
    """
    Edit a phone number of a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    old_phone = input("Please enter phone you want to edit: ")
    new_phone = input("Please enter new phone: ")
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Phone updated."


@input_error
def remove_phone(book):
    """
    Remove a phone number from a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    phone = input("Please enter phone number to remove: ")
    record = book.find(name)
    record.remove_phone(phone)
    return "Phone removed."


@input_error
def show_phones(book):
    """
    Show all phone numbers of contacts.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    record = book.find(name)
    return record.show_phones()


@input_error
def show_all(book):
    """
    Show all contacts.
    """
    if book.data.values():
        table = PrettyTable()
        table.field_names = ["Name", "Phones", "Address", "Birthday", "Note Title", "Note Content"]
        table.align = "l"

        for record in book.data.values():
            phones_str = "\n".join(p.value for p in record.phones)
            notes_str = ""
            notes_titles_str = ""
            for note in record.notes:
                if notes_str == "":
                    notes_str += note.note
                    notes_titles_str += note.title
                else:
                    notes_str += f"\n{note.note}"
                    notes_titles_str += f"\n{note.title}"
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
                [record.name.value, phones_str, address_str, birthday_str, notes_titles_str, notes_str],
                divider=True
            )

        print(table)
    else:
        print("No contacts available.")


@input_error
def add_birthday(book):
    """
    Add a birthday to a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    birthday = input("Please enter contact's birthday: ")
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(book):
    """
    Show the birthday of a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    record = book.find(name)
    if hasattr(record, "birthday"):
        return record.birthday.value
    else:
        return f"No birthday in the system for {name}."


@input_error
def add_email(book):
    """
    Add an email address to a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    email = input("Please enter email address: ")
    record = book.find(name)
    record.add_email(email)
    return "Email added."


@input_error
def show_emails(book):
    """
    Show all email addresses for a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    record = book.find(name)
    if record.emails:
       return "\n".join(record.show_emails())
    else:
       return "There are no contact email addresses availiable."

@input_error
def add_address(book):
    """
    Add an address to a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    address = input("Please enter contact's address: ")
    record = book.find(name)
    record.add_address(address)
    return "Address added."


@input_error
def edit_address(book):
    """
    Edit the address of a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    new_address = input("Please enter new address: ")
    record = book.find(name)
    record.edit_address(new_address)
    return "Address updated."


@input_error
def remove_address(book):
    """
    Remove the address of a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    record = book.find(name)
    record.remove_address()
    return "Address removed."


@input_error
def add_note(book):
    """
    Add a note to a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    title = input("Please enter note title: ")
    note = input("Please enter note text: ")
    record = book.find(name)
    record.add_note(title, note)
    return "Note added."


@input_error
def edit_note(book):
    """
    Edit a note of a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    title = input("Please enter note title: ")
    new_note = input("Please enter text for a new note: ")
    record = book.find(name)
    record.edit_note(title, new_note)
    return "Note updated."


@input_error
def remove_note(book):
    """
    Remove a note from a contact.
    """
    name = input("Please enter contact's name: ")
    check_name(name, book)
    title = input("Please enter note title: ")
    record = book.find(name)
    record.remove_note(title)
    return "Note removed."


@input_error
def search_note(book):
    """
    Search for a note by title.
    """
    title = input("Please enter note title: ")
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

available_commands = {
    "add-contact" : "add_contact",
    "remove-contact" : "remove_contact",
    "add-phone" : "add_phone",
    "edit-phone" : "edit_phone",
    "remove-phone" : "remove_phone",
    "show-phones" : "show_phones",
    "all" : "show_all",
    "add-birthday": "add_birthday",
    "show-birthday" : "show_birthday",
    "add-address" : "add_address",
    "edit-address" :"edit_address",
    "remove-address" : "remove_address",
    "add-note" : "add_note",
    "edit-note" : "edit_note",
    "remove-note" : "remove_note",
    "search-note" : "search_note",
    "help" : "show_help",
    "exit" : "exit",
    "close" : "close",
    "hello" : "hello"
}

def show_help():
    """
    Display help information for available commands.
    """
    print("Available commands:")
    for command in available_commands.values():
        if command in ["exit","close"]:
            command_desc = "Exit the assistant bot."
        else:
            func = globals().get(command.replace("-", "_"))
            docstring = func.__doc__.strip() if func and func.__doc__ else "None"
            command_desc = docstring

        if command == "hello":
            command_desc = "Display a welcome message."

        print(f"{command: <15}: {command_desc}")

def get_user_input():
    user_input = prompt("Enter a command: ", completer=WordCompleter(available_commands.keys))
    return user_input


def main():
    try:
        book = AddressBook()
        book.load_from_file("address_book.dat")
        print("Welcome to the assistant bot!")
        while True:
            user_input = get_user_input()
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "all":
                show_all(book)
            elif command == "add-contact":
                print(add_contact(book))
            elif command == "remove-contact":
                print(remove_contact(book))
            elif command == "add-phone":
                print(add_phone(book))
            elif command == "edit-phone":
                print(edit_phone(book))
            elif command == "remove-phone":
                print(remove_phone(book))
            elif command == "show-phones":
                print(show_phones(book))
            elif command == "add-birthday":
                print(add_birthday(book))
            elif command == "show-birthday":
                print(show_birthday(book))
            elif command == "birthdays":
                # Default to 7 days if no argument provided
                days = int(args[0]) if args else 7
                print(book.birthdays(days))
            elif command == "add-address":
                print(add_address(book))
            elif command == "edit-address":
                print(edit_address(book))
            elif command == "remove-address":
                print(remove_address(book))
            elif command == "add-email":
                print(add_email(book))
            elif command == "show-emails":
                print(show_emails(book))
            elif command == "add-note":
                print(add_note(book))
            elif command == "edit-note":
                print(edit_note(book))
            elif command == "remove-note":
                print(remove_note(book))
            elif command == "search-note":
                print(search_note(book))
            elif command == "help":
                show_help()
            else:
                print("Invalid command.")
    finally:
        book.save_to_file("address_book.dat")
