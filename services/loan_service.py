# managing loan operations like: borrow, return, view loans, check book availability

"""
________________________________________________________
services.loan_service
========================================================
Service for managing loans-related operations.
________________________________________________________

file status: in progress

"""

from datetime import datetime

import exceptions as exc
from database.book_json_file_service import BookJsonFileService
from database.database_schemes import (
    book_schema,
    loan_schema,
    reservation_schema,
    user_schema,
)
from database.json_files_major_services import JsonFilesService
from database.loan_json_file_service import LoanJsonFileService
from database.user_json_file_service import UsersJsonFileService
from models.book import Book
from models.loan import Loan, Reservation
from models.user import User
from services.authorisation_service import UserAuthorisation
from services.book_service import BookService
from services.user_service import UserService
from utils.config import (
    LOANS_LIST_FILE_PATH,
    PROGRAM_USERS_FILE_PATH,
    RESERVATIONS_LIST_FILE_PATH,
    THE_LIBRARY_FILE_PATH,
)


class LoanService:
    def __init__(self, loan_json_service=None):

        # JSON file services

        loan_file_json_service = JsonFilesService(
            file_path=LOANS_LIST_FILE_PATH, schema=loan_schema
        )
        reservation_file_json_service = JsonFilesService(
            file_path=RESERVATIONS_LIST_FILE_PATH, schema=reservation_schema
        )

        book_file_json_service = JsonFilesService(
            file_path=THE_LIBRARY_FILE_PATH, schema=book_schema
        )
        user_file_json_service = JsonFilesService(
            file_path=PROGRAM_USERS_FILE_PATH, schema=user_schema
        )

        # Data layer service handling loan records stored in JSON file
        self.loan_data_service = loan_json_service or LoanJsonFileService(
            json_service=loan_file_json_service, file_path=LOANS_LIST_FILE_PATH
        )

        # Data layer service handling reservation records stored in JSON file
        self.reservation_data_service = LoanJsonFileService(
            json_service=reservation_file_json_service,
            file_path=RESERVATIONS_LIST_FILE_PATH,
        )

        # Book service (business layer)
        self.book_service = BookService(
            BookJsonFileService(
                json_service=book_file_json_service, file_path=THE_LIBRARY_FILE_PATH
            )
        )

        # User Service (business layer)
        self.user_service = UserService(
            UsersJsonFileService(
                json_service=user_file_json_service, file_path=PROGRAM_USERS_FILE_PATH
            )
        )

        # Authorisation Service
        self.user_authorisation_service = UserAuthorisation()

    ### CORE

    def borrow_book(self, user_id, book_id):
        """This method description"""

        if not user_id:
            raise exc.UserValidationError(
                "Please provide user ID to proceed borrowing the book."
            )

        if not isinstance(user_id, int):
            raise exc.UserValidationError("User ID must be a number.")

        if not book_id:
            raise exc.BookValidationError(
                "Please provide book ID to proceed borrowing the book."
            )

        if not isinstance(book_id, int):
            raise exc.BookValidationError("Book ID must be a number.")

        # available_books = self.book_service.get_available_books()
        # I AM HERE

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
