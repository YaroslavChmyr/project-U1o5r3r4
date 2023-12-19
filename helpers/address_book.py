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


class Note(Field):
    pass


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


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.notes = []
        # Assume only one address
        self.addresss = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_note(self, note):
        self.notes.append(Note(note))

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

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        birthdays_per_week = defaultdict(list)
        today = datetime.today().date()

        for record in self.data.values():
            # check if the record object has the attribute birthday before attempting to access its value.
            if hasattr(record, "birthday"):
                birthday_date = datetime.strptime(
                    record.birthday.value, "%d.%m.%Y"
                ).date()
                birthday_this_year = birthday_date.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days

                if delta_days < 7:
                    day_of_week = (today + timedelta(days=delta_days)).strftime("%A")
                    if day_of_week in ["Saturday", "Sunday"]:
                        day_of_week = "Monday"

                    birthdays_per_week[day_of_week].append(record.name.value)

        return birthdays_per_week

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
