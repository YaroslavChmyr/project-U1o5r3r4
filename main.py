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
            return f"Contact with the name {e} doesn't exists. Use 'add-contact' to add."
        except IndexError as e:
            return f"Index error occurred: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    return inner


@input_error
def add_contact(name, book):
    if not name:
        raise ValueError("Contact name cannot be empty.")

    if book.find(name):
        return f"Contact with the name '{name}' already exists."
    else:
        record = Record(name)
        book.add_record(record)
        return f"Contact '{name}' added."

@input_error
def remove_contact(name, book):
    record = book.find(name)
    if record:
        book.delete(name)
        return f"Contact '{name}' removed."
    else:
        raise KeyError(name)

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

            table.add_row(
                [record.name.value, phones_str, address_str, birthday_str, notes_titles_str, notes_str],
                divider=True
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

def show_help():
    print("Available commands:")
    print("  - hello: Print a welcome message.")
    print("  - all: Show all contacts.")
    print("  - add-contact: Add a new contact.")
    print("  - remove-contact: Remove a contact.")
    print("  - add-phone: Add a phone number to a contact.")
    print("  - edit-phone: Edit a phone number of a contact.")
    print("  - remove-phone: Remove a phone number from a contact.")
    print("  - show-phones: Show all phone numbers of a contact.")
    print("  - add-birthday: Add a birthday to a contact.")
    print("  - show-birthday: Show the birthday of a contact.")
    print("  - birthdays [days]: Show upcoming birthdays for the specified number of days (default is 7 days).")
    print("  - add-address: Add an address to a contact.")
    print("  - edit-address: Edit the address of a contact.")
    print("  - remove-address: Remove the address of a contact.")
    print("  - add-note: Add a note to a contact.")
    print("  - edit-note: Edit a note of a contact.")
    print("  - remove-note: Remove a note from a contact.")
    print("  - search-note: Search for a note by title.")
    print("  - help: Show available commands.")
    print("  - close/exit: Close the assistant bot.")

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
            elif command == "all":
                show_all(book)
            elif command == "add-contact":
                name = input("Please enter contact name: ")
                print(add_contact(name, book))
            elif command == "remove-contact":
                name = input("Please enter contact name: ")
                print(remove_contact(name, book))
            elif command == "add-phone":
                name = input("Please enter contact name: ")
                phone = input("Please enter contact's phone: ")
                print(add_phone(name, phone, book))
            elif command == "edit-phone":
                name = input("Please enter contact name: ")
                old_phone = input("Please enter phone: ")
                new_phone = input("Please enter new phone: ")
                print(edit_phone(name, old_phone, new_phone, book))
            elif command == "remove-phone":
                name = input("Please enter contact name: ")
                phone = input("Please enter phone number to remove: ")
                print(remove_phone(name, phone, book))
            elif command == "show-phones":
                name = input("Please enter contact name: ")
                print(show_phones(name, book))
            elif command == "add-birthday":
                name = input("Please enter contact name: ")
                birthday = input("Please enter contact's birthday: ")
                print(add_birthday(name, birthday, book))
            elif command == "show-birthday":
                name = input("Please enter contact name: ")
                print(show_birthday(name, book))
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
                title = input("Please enter note title: ")
                note = input("Please enter note text: ")
                print(add_note(name, title, note, book))
            elif command == "edit-note":
                name = input("Please enter contact name: ")
                title = input("Please enter note title: ")
                new_note = input("Please enter text for a new note: ")
                print(edit_note(name, title, new_note, book))
            elif command == "remove-note":
                name = input("Please enter contact name: ")
                title = input("Please enter note title: ")
                print(remove_note(name, title, book))
            elif command == "search-note":
                title = input("Please enter note title: ")
                print(search_note(title, book))



            elif command == "add-email":
                name = input("Please enter contact name: ")
                email = input("Please enter email which you want add: ")
                print(add_email(name, email, book))
            elif command == "remove-email":
                name = input("Please enter contact name: ")
                email = input("Please enter email which you want delete: ")
                print(remove_email(name, email, book))
            elif command == "show-emails":
                name = input("Please enter contact name: ")
                print(show_emails(name, book)) 



            elif command == "help":
                show_help()
            else:
                print("Invalid command.")
    finally:
        book.save_to_file("address_book.dat")


if __name__ == "__main__":
    main()
