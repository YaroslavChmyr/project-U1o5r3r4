# Personal assistant

Personal assistant is a command line application for storing and interacting with address book entries and notes.

Personal assistant allows:
- Store contacts with names, addresses, phone numbers, email and birthdays in the contact book
- Display a list of contacts whose birthday is a specified number of days from the current date
- Check the  entered phone number and email when creating or editing a record and notify the user in case of incorrect entry
- Search for contacts among book contacts
- Edit and delete entries from the contact book
- Keep notes with text information
- Search for notes
- Edit and delete notes

## Downloads

## Requirements

- prettytable library
```
>>> pip install prettytable
```

## Command list:

- **add-contact**: Add a new contact.
- **remove-contact**: Remove contact.
- **add-phone**: Add a phone number to contact.
- **edit-phone**: Edit an existing phone number.
- **remove-phone**: Delete a phone number from a contact.
- **show-phones**: Display phone numbers for the contact.
- **add-birthday**: Add a birhtday to contact.
- **show-birthday**: Display birthday for the contact.
- **birthdays [days]**: Show birthdays that will occur during the next day interval. Days is 7 by default.
- **add-address**: Add address to contact.
- **edit-address**: Edit an existing address.
- **remove-address**: Remove address.
- **add-email**: Add email address to contact.
- **edit-email**: Edit an existing email address.
- **remove-email**: Delete email address from a contact.
- **add-note**: Add note with a title to the contact.
- **edit-note**: Edit an existing note.
- **remove-note**: Remove note from a contact.
- **search-note**: Search for note by title.
- **all**: Display information about all contacts.
- **hello**: Get a greeting from an assistant.
- **close** or **exit**: Close the program.

## Examples:

### Add contact to the contact book
```
Welcome to the assistant bot!
Enter a command: add-contact
Please enter contact name: Yaroslav
Contact added.
```
### Add a contact phone number
```
Enter a command: add-phone
Please enter contact name: Lisa
Please enter contact's phone: 0997411235
Phone added.
```

### Add a contact birthday
```
Enter a command: add-birthday
Please enter contact name: Lisa
Please enter contact's birthday: 25.12.1986
Birthday added.
```

