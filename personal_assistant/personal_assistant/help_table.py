from prettytable import PrettyTable

def show_help():
    tablehelp = PrettyTable()
    tablehelp.align = "l"

    tablehelp.field_names = ["Command", "Description"]

    information = [
        ("hello", "Print a welcome message"),
        ("all", "Show all contacts"),
        ("add-contact", "Add a new contact"),
        ("remove-contact", "Remove a contact"),
        ("add-phone", "Add a phone number to a contact"),
        ("edit-phone", "Edit a phone number of a contact"),
        ("remove-phone", "Remove a phone number from a contact"),
        ("show-phones", "Show all phone numbers of a contact"),
        ("add-birthday", "Add a birthday to a contact"),
        ("show-birthday", "Show the birthday of a contact"),
        ("birthdays [days]", "Show upcoming birthdays for the specified number of days (default is 7 days)"),
        ("add-address", "Add an address to a contact"),
        ("edit-address", "Edit the address of a contact"),
        ("remove-address", "Remove the address of a contact"),
        ("add-note", "Add a note to a contact"),
        ("edit-note", "Edit a note of a contact"),
        ("remove-note", "Remove a note from a contact"),
        ("search-note", "Search for a note by title"),
        ("help", "Show available commands"),
        ("close/exit", "Close the assistant bot")
    ]

    for row in information:
        tablehelp.add_row(row)

    print(tablehelp)