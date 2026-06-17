# managing loan operations like: borrow, return, view loans, check book availability

"""
________________________________________________________
services.loan_service
========================================================
Service for managing loans-related operations.
________________________________________________________

file status: on hold
on hold due to required implementation reservation logic in loan_json_file_service


"""

from datetime import datetime

import exceptions as exc
from database.loan_json_file_service import LoanJsonFileService
from models.book import Book
from models.loan import Loan, Reservation
from models.user import User
from services.authorisation_service import UserAuthorisation
from services.book_service import BookService
from services.user_service import UserService


class LoanService:
    def __init__(self, loan_json_service=LoanJsonFileService):
        self.loan_json_service = loan_json_service

    ### CORE

    def borrow_book(self, user_id, book_id):
        pass

    def return_book(self, loan_id):
        pass

    ### VALIDATION

    def ensure_book_available(self, book_id):
        pass

    def ensure_user_can_borrow(self, user_id):
        pass

    ### STATUS CHECKS

    def is_book_borrowed(self, book_id):
        pass

    def is_book_overdue(self, book_id):
        pass

    ### RETRIEVE

    def get_all_loans(self):
        pass

    def get_active_loans(self):
        pass

    def get_loan_by_id(self, loan_id):
        pass

    def get_books_borrowed_by_user(self, user_id):
        pass

    def get_overdue_books(self):
        pass

    ### RESERVATIONS

    def reserve_book(self, user_id, book_id):
        pass

    def cancel_reservation(self, reservation_id):
        pass

    def get_all_reservations(self):
        pass

    def get_reservation_by_id(self):
        pass

    def get_books_reserved_by_user(self, user_id):
        pass
