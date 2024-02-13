from datetime import datetime
import pickle

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

    def validate(self, value):
        return True


class Phone(Field):
    def validate(self, value):
        return all(char.isdigit() or char in "+-()" for char in value)


class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False


class Name(Field):
    def validate(self, value):
        return all(char.isalpha() or char in " -" for char in value)


class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Name(name)
        self.phone = Phone(phone) if phone else None
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if not self.birthday:
            return None
        now = datetime.now()
        current_year = now.year
        birthday = datetime.strptime(self.birthday.value, '%Y-%m-%d')
        birthday = birthday.replace(year=current_year)
        if birthday < now:
            birthday = birthday.replace(year=current_year + 1)
        return (birthday - now).days


class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def __iter__(self):
        return iter(self.records)

    def paginate_records(self, page_size):
        return [self.records[i:i + page_size] for i in range(0, len(self.records), page_size)]

    def save_address_book(self,filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.records, file)
    def search_contacts(self, query):
        matching_records = []
        for record in self.records:
            if query.lower() in record.name.value.lower() or (record.phone and query in record.phone.value):
                matching_records.append(record)
        return matching_records

def main():
    address_book = AddressBook()
    
    try:
        with open('address_book.pkl', 'rb') as file:
            address_book.records = pickle.load(file)
    except FileNotFoundError:
        print("Address Book file doesn't exist. Making off new Address Book .")

    record1 = Record("John Johnson", "+48 123 456 789", "1980-01-01")
    record2 = Record("Andrew Tim", "+48 123 456 789", "1980-05-15")
    address_book.add_record(record1)
    address_book.add_record(record2)

    address_book.save_address_book('address_book.pkl')

    matching_contacts = address_book.search_contacts('John')
    for contact in matching_contacts:
        print(f"Name: {contact.name}, Phone: {contact.phone}, Birthday: {contact.birthday}")

if __name__ == '__main__':
    main()
