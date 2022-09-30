from typing import Optional, Generator
import pickle
import os

from .record import Record


class AddressBook:
    def __init__(self) -> None:
        self.root_package: str = "console_bot"
        self.filename = os.path.join(self.root_package, "CONTACTS.dat")

    def add_record(self, record: Record) -> None:
        with open(self.filename, 'ab') as fh:
            pickle.dump(record, fh)

    def get_contact(self, username: str) -> Record | None:
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            return

        for contact in self.iterator(1):
            contact = contact[0]

            if username == contact.name.value:
                return contact

        raise KeyError(username)

    def get_contacts(self, search: Optional[str] = None) -> list[Record]:
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            return []

        contacts = []

        for contact in self.iterator(1):
            contact = contact[0]

            if search is None or search in contact.name.value \
                    or any(search in str(x.value) for x in contact.phones):
                contacts.append(contact)

        return contacts

    # Temporary command due to impossibility to change object in the file
    def change_contact(self, contact: Record, remove: bool = False) -> None:
        temporary_filename = os.path.join(self.root_package, 'old_contacts.dat')
        os.rename(self.filename, temporary_filename)

        self.filename = temporary_filename

        for _contact in self.iterator(1):
            if _contact[0].name.value == contact.name.value:
                if remove:
                    continue

                AddressBook().add_record(contact)

            else:
                AddressBook().add_record(_contact[0])

        os.remove(temporary_filename)

    def iterator(self, count: int = 0) -> 'Generator[list[Record]]':
        count = count if count else "inf"

        records = []

        with open(self.filename, 'rb') as fh:

            while True:
                if len(records) >= count:
                    yield records
                    records = []

                try:
                    records.append(pickle.load(fh))
                except EOFError:
                    break

        if records:
            yield records

    def __repr__(self):
        return "AddressBook({})".format(', '.join([f"{k}={v}" for k, v in self.__dict__.items()]))
