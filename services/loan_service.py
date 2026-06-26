# managing loan operations like: borrow, return, view loans, check book availability

"""
________________________________________________________
services.loan_service
========================================================
Service for managing loans-related operations.
________________________________________________________

file status: in progress

"""

from datetime import datetime, timedelta

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
from utils.helpers import generate_loan_id, generate_reservation_id


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

    ### VALIDATION HELPERS

    def ensure_user_has_permission_to_borrow(self):
        """Veryfing that the currently logged-in user have permissions to borrow the book."""
        self.user_authorisation_service.check_permission("books.borrow_book")

    def ensure_book_available(self, book_id):
        """Veryfing that book status is 'available' and book can be borrowed by user."""

        if not self.book_service.is_book_available(book_id=book_id):
            raise exc.BookNotAvailableError("Book is currently unavailable.")

    def ensure_loan_exists(self, loan_id):
        """This method is for veryfing if the loan entry exists in database."""

        try:
            self.get_loan_by_id(loan_id)
            return True
        except exc.LoanNotFoundError:
            return False

    ### GLOBAL RETRIEVE

    def get_all_loans(self):
        """Method to retrieve all loans list from database"""

        return self.loan_data_service.get_all_loans_list()

    def get_active_loans(self):
        """Method to retrieve loans list that are currently active"""

        try:
            all_loans = self.get_all_loans()
        except exc.LoanNotFoundError:
            all_loans = []

        active_loans = []

        for loan in all_loans:
            if loan["return_date"] is None:
                active_loans.append(loan)

        return active_loans

    def get_loan_by_id(self, loan_id):
        """Method to retrieve loan details by loan id"""
        pass

    def get_overdue_books(self):
        """Method to retrieve the list of all books that are borrowed and its return date has gone."""
        pass

    ### STATUS CHECKS

    def is_book_borrowed(self, book_id):
        """
        METHOD NOT FINISHED YET

        Checking if the book is borrowed to quickly confirm its status

        retrurns True if book is borrwed and False if book is available

        """
        book = self.book_service.get_book_by_id(book_id)

        return book.book_status == "borrowed"

    def is_book_overdue(self, book_id):
        """Checking if the book is overdue. Checking is for single book in library and it is checked by book id."""

        self.book_service.ensure_book_exists(book_id)

        if not self.is_book_borrowed(book_id):
            return False

        active_loans = self.get_active_loans()

        return_date = None

        today = datetime.now().date()

        for loan in active_loans:
            if loan["book_id"] == book_id:
                return_date = loan["return_date"]
                break

        if not return_date:
            return False

        return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

        if today > return_date:
            return True

        return False

    ### USER‑FOCUSED RETRIEVE

    def get_books_borrowed_by_user(self, user_id):
        """Method to retrieve the list of books borrowed by current user"""
        pass

    def get_user_overdue_books(self):
        pass

    ### CORE ACTIONS

    def borrow_book(self, book_id):
        """This method requires refactoring!

        This method allows a user to borrow a book by its ID. It checks for the book's availability, the user's permissions, and creates a new loan record if all conditions are met. It updates the book's status to indicate that it is currently borrowed and sets return date for the loan.

        Book can be borrowed only if it's status is 'available'. Books which are 'reserved' cannot be borrowed by user who is not the user who reserved the book.

        Book reserved by particular user can be borrowed by this user.

        Args:
            book_id (int): The ID of the book to be borrowed.

        Returns:
            Loan: A Loan object representing the newly created loan record.
        """

        if not book_id:
            raise exc.BookValidationError(
                "Please provide book ID to proceed borrowing the book."
            )

        if not isinstance(book_id, int):
            raise exc.BookValidationError("Book ID must be a number.")

        current_user = self.user_authorisation_service.get_current_user()

        if not current_user:
            raise exc.PermissionError("User must be logged in to borrow a book.")

        # I have method ensure_user_can_borrow. I want to replace line below with calling this helper method.
        self.user_authorisation_service.check_permission("books.borrow_book")

        self.book_service.ensure_book_exists(book_id)

        if not self.book_service.is_book_available(book_id):
            raise exc.BookNotAvailableError("Book is currently unavailable.")

        now = datetime.now()

        new_loan = Loan(
            user_id=current_user.user_id,
            book_id=book_id,
            loan_date=now.strftime("%Y-%m-%d"),
            return_date=(now + timedelta(days=21)).strftime("%Y-%m-%d"),
        )

        try:
            all_loans = self.loan_data_service.get_all_loans_list()
        except exc.LoanNotFoundError:
            all_loans = []

        loan_id = generate_loan_id(all_loans)

        new_loan.loan_id = loan_id

        self.loan_data_service.add_loan_data(new_loan.to_dict())

        self.book_service.mark_book_as_borrowed(
            book_id=book_id,
            user_id=new_loan.user_id,
            due_date=new_loan.return_date,
            loan_date=new_loan.loan_date,
        )

        return new_loan

    def return_book(self, loan_id):
        """Method to enable user return the borrowed books. It also verifies if the loan exits before further actions."""
        pass

    ### RESERVATIONS

    def reserve_book(self, user_id, book_id):
        """Method that enables user to reserve a book."""
        pass

    def borrow_reserved_book(self):
        """Method that enables user to borrow the book which was reserved by user earlier."""
        pass

    def cancel_reservation(self, reservation_id):
        """Method that enables user to cancel the book reservation."""
        pass

    def get_all_reservations(self):
        """Method that allows to retrieve a list with all reservations from database."""
        pass

    def get_reservation_by_id(self):
        """Method that allows to retrieve data about particular reservation by reservation id"""
        pass

    def get_books_reserved_by_user(self, user_id):
        """Method to get the list with all acvtive reservations of books by particular user."""
        pass
