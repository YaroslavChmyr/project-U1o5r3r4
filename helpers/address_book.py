from collections import UserDict, defaultdict
from datetime import datetime, timedelta
import pickle, re, os


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Note(UserDict):
    def __init__(self, title, note):
        super().__init__({title: note})


class Address(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        # Phone number verification (10 digits)
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Invalid phone number format. Use a 10-digit number.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        # Date format verification (DD.MM.YYYY)
        if not re.match(r"^\d{2}\.\d{2}.\d{4}$", value):
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY.")
        super().__init__(value)


class Email(Field):
    def __init__(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format. Use name@company.com")
        super().__init__(value)
    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.notes = []
        # Assume only one address
        self.address = None
        self.email = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def show_phones(self):
        if self.phones:
            return "\n".join(phone.value for phone in self.phones)
        else:
            return "No phone numbers available."

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_note(self, title, note):
        is_title = False
        for element in self.notes:
            if title in element.data:
                is_title = True
                raise ValueError("Note with this title already exists.")
        if not is_title:
            self.notes.append(Note(title, note))

    def edit_note(self, title, new_note):
        is_note = False
        for note in self.notes:
            for element in note.data:
                if element == title:
                    note.data[title] = new_note
                    is_note = True
        if not is_note:
            raise ValueError("No note with such title. Please try again.")

    def remove_note(self, title):
        is_note = False
        for note in self.notes:
            for element in note.data:
                if element == title:
                    is_note = True
        if is_note:
            note.data.pop(title)
        else:
            raise ValueError("No note with such title. Please try again.")

    def add_address(self, address):
        if self.address:
            raise ValueError("Contact already has an address. Use 'edit-address' to modify.")
        self.address = Address(address)

    def edit_address(self, new_address):
        if self.address:
            self.address.value = new_address
        else:
            raise ValueError("No address to edit. Add an address first.")

    def remove_address(self):
        self.address = None

    def add_email(self, person, email):
        if person not in self.email:
            self.email[person] = []

        self.email[person].append(Email(email))
        print(f"Email {email} for {person} added.")

    def remove_email(self, person, email):
        if person in self.email and email in self.email[person]:
            self.email[person].remove(email)
            print(f"Email {email} for {person} has removed.")
        else:
            print(f"Email {email} for {person} has not found.")

    def show_emails(self):
        print("List of emails:")
        for person, emails in self.email.items():
            print(f"{person}: {', '.join(emails)}")


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        super().pop(name, None)

    def search_note(self, title):
        for record in self.data.values():
            is_note = False
            for note in record.notes:
                for note_title, value in note.data.items():
                    if note_title == title:
                        notes_title_str = note_title
                        notes_str = value
                        contact_name = record.name.value
                        is_note = True
        if is_note:
            return notes_title_str, notes_str, contact_name
        else:
            raise ValueError("No note with such title. Please try again.")

    def get_birthdays_days_interval(self, days):
        birthdays_per_days_interval = defaultdict(list)
        today = datetime.today().date()

        for record in self.data.values():
            # check if the record object has the attribute birthday before attempting to access its value.
            if hasattr(record, "birthday"):
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday_date.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days

                if 0 <= delta_days <= days:
                    day_of_week = (today + timedelta(days=delta_days)).strftime("%A")
                    if day_of_week in ["Saturday", "Sunday"]:
                        day_of_week = "Monday"

                    birthdays_per_days_interval[day_of_week].append(record.name.value)

        return birthdays_per_days_interval

    def birthdays(self, days):
        birthdays_in_interval = self.get_birthdays_days_interval(days)
        if birthdays_in_interval:
            return "\n".join(
                [f"{name}: {', '.join(birthday)}" for name, birthday in birthdays_in_interval.items()]
            )
        else:
            return "No upcoming birthdays."

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                data = pickle.load(file)
                self.data = data
        else:
            self.data = {}



