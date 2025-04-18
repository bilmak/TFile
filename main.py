import argparse
import typing
from venv import logger
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Header:
    field_id = "01"
    name: str
    surname: str
    patronymic: str
    address: str

    def __init__(self, name: str, surname: str, patronymic: str, address: str) -> None:
        self.name = name.strip()
        if len(self.name) > 28:
            raise ValueError("exceeds 28 characters")
        self.surname = surname.strip()
        if len(self.surname) > 30:
            raise ValueError("exceeds 30 characters")
        self.patronymic = patronymic.strip()
        if len(self.patronymic) > 30:
            raise ValueError("exceeds 30 characters")
        self.address = address.strip()
        if len(self.address) > 30:
            raise ValueError("exceeds 30 characters")

    def __str__(self):
        return f"Header(name={self.name}, surname={self.surname}, patronymic={self.patronymic}, address={self.address}"

    def __eq__(self, other):
        if not isinstance(other, Header):
            return False
        return self.name == other.name \
            and self.surname == other.surname \
            and self.patronymic == other.patronymic \
            and self.address == other.address

    @classmethod
    def interpretation_from_file_text(cls, text: str) -> "Header":
        return cls(
            name=text[2:30],
            surname=text[30:60],
            patronymic=text[60:90],
            address=text[90:120],
        )

    def format_to_text(self) -> str:
        return f"{self.field_id}{self.name:28}{self.surname:30}{self.patronymic:30}{self.address:30}"


class Transaction:
    field_id = "02"
    counter: int | None
    amount: int
    currency: str

    def __init__(self, counter: int | None, amount: int, currency: str) -> None:
        self.counter = counter
        if self.counter and self.counter > 20000:
            raise ValueError("exceeds 20 000 characters")
        self.amount = amount
        if len(str(self.amount)) > 12:
            raise ValueError("exceeds 12 characters")
        self.currency = currency
        if len(self.currency) > 3:
            raise ValueError("exceeds 3 characters")

    def __str__(self):
        return f"Transaction(counter={self.counter}, amount={self.amount}, currency={self.currency})"

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return False
        return self.counter == other.counter \
            and self.amount == other.amount \
            and self.currency == other.currency\


    @classmethod
    def from_text(cls, text: str) -> "Transaction":
        return cls(
            counter=int(text[2:8]),
            amount=int(text[8:20]),
            currency=text[20:23],
        )

    def format_to_text(self) -> str:
        return f"{self.field_id}{self.counter:06}{self.amount:012}{self.currency:3}"


class Footer:
    field_id = "03"
    total_counter: int
    control_sum: int

    def __init__(self, total_counter: int, control_sum: int) -> None:
        self.total_counter = total_counter
        if len(str(self.total_counter)) > 6:
            raise ValueError("exceeds 6 characters")
        self.control_sum = control_sum
        if len(str(self.control_sum)) > 12:
            raise ValueError("exceeds 12 characters")

    def __str__(self):
        return f"Footer(total counter={self.total_counter}, control sum={self.control_sum})"

    def __eq__(self, other):
        if not isinstance(other, Footer):
            return False
        return self.total_counter == other.total_counter \
            and self.control_sum == other.control_sum \


    @classmethod
    def from_text(cls, text: str) -> "Footer":
        return cls(
            total_counter=int(text[2:8]),
            control_sum=int(text[8:20]),
        )

    def format_to_text(self) -> str:
        return f"{self.field_id}{self.total_counter:06}{self.control_sum:012}"


class Storage:
    class_transactions: dict[str, Transaction] = {}

    def __init__(self, file: typing.BinaryIO) -> None:
        self.file = file
        self.counter = 0
        self.header = self.read_header()
        self.read_transactions()
        self.footer = self.read_footer()

    def create_increment_transaction(self) -> int:
        lenght_transactions = len(self.class_transactions)
        self.counter = lenght_transactions + 1
        if self.counter > 20000:
            raise ValueError("Maximum number of transactions reached")
        return self.counter

    def read_header(self) -> Header:
        self.file.seek(0, 0)
        raw_header = self.file.readline().decode("utf-8")
        header = Header.interpretation_from_file_text(raw_header[0:120])

        return header

    def read_transactions(self):
        self.file.seek(121, 0)
        lines = self.file.readlines()
        transactions = lines[:-1]
        for k in transactions:
            transaction = Transaction.from_text(k.decode("utf-8"))
            self.class_transactions[transaction.counter] = transaction

    def read_footer(self) -> Footer:
        self.file.seek(-120, os.SEEK_END)
        raw_footer = self.file.readline().decode("utf-8")
        footer = Footer.from_text(raw_footer)
        return footer

    def save_transaction(self, transaction: Transaction):
        if transaction.counter is None:
            transaction.counter = self.create_increment_transaction()
        self.class_transactions[self.counter] = transaction

    def save_footer(self) -> Footer:
        footer = Footer(0, 0)
        if self.class_transactions is None:
            raise Exception("You dont have any transactions")
        lenght_transactions = len(self.class_transactions)
        footer.total_counter = lenght_transactions
        sum_of_amount = 0
        for k, v in self.class_transactions.items():
            sum_of_amount += v.amount
        footer.total_counter = lenght_transactions
        footer.control_sum = sum_of_amount
        # print(f"\nFooter Information: \nFooter ID:{footer.field_id}, Total Counter:{footer.total_counter}, Control Sum:{footer.control_sum}")
        return footer

    def flush(self):
        self.file.seek(0,0)
        self.file.write((self.header.format_to_text()+"\n").encode("utf-8"))
        for k, v in self.class_transactions.items():
            self.file.write((v.format_to_text()+"\n").encode("utf-8"))
        self.file.write(
            (self.save_footer().format_to_text()+"\n").encode("utf-8"))


with open("first.db", "rb+")as file1:
    storage = Storage(file1)
    transac = Transaction(None, 8000, "PLN")
    storage.save_transaction(transac)
    

    fl = storage.flush()
