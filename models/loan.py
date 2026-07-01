# loan class with attributes and methods (who borrowed the book, when it was borrowed, when it was returned)

"""
________________________________________________________
models.loan
========================================================
Module for defining the Loan class and Reservation class.
________________________________________________________

This module contains the definition of the Loan class, which represents a loan of a book to a user, and the Reservation class, which represents a reservation of a book by a user. The Loan class includes attributes such as user ID, book ID, loan date, and return date. The Reservation class includes attributes such as user ID, book ID, and reservation date.

"""


class Loan:
    def __init__(
        self, user_id: int, book_id: int, loan_date: str, return_date: str | None = None
    ):

        self.loan_id: int | None = None

        self.user_id = user_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date

    def to_dict(self):
        """This method converts the Loan object into a dictionary representation."""

        return {
            "loan_id": self.loan_id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "loan_date": self.loan_date,
            "return_date": self.return_date,
        }


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

    def to_dict(self):

        return {
            "resrvation_id": self.reservation_id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "reservation_date": self.reservation_date,
        }
