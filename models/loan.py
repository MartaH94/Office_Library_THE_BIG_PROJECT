# loan class with attributes and methods (who borrowed the book, when it was borrowed, when it was returned)

"""
To do:
- update module docstring
- buil Loan model
- implement method to dict


"""

from datetime import datetime

import exceptions as exc
from models.book import Book
from models.user import User


class Loan:
    def __init__(
        self, user_id: int, book_id: int, loan_date: str, return_date: str | None = None
    ):
        self.user_id = user_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date

        loan_id = None

    def to_dict(self):
        pass


class Reservation:
    def __init__(
        self,
        user_id: int,
        book_id: int,
        reservation_date: str,
    ):
        self.reservation_id: int | None = None

        self.user_id = user_id
        self.book_id = book_id
        self.reservation_date = reservation_date
