"""
________________________________________________________
services.loan_service
========================================================
Service for managing loans-related operations.
________________________________________________________

This module defines the `LoanService` class, which is responsible for handling all operations related to loans and reservations in the system. It interacts with the storage layer (JSON service) to perform CRUD operations and provides high-level methods for working with loan data.


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
    """The LoanService class is responsible for managing all operations related to loans and reservations in the system. It provides methods for borrowing and returning books, checking book availability, retrieving loan and reservation data, and ensuring user permissions. The service interacts with the storage layer (JSON service) to perform CRUD operations on loan and reservation records."""

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

    def get_all_loans(self):  # done
        """This method retrieves all loan records from the database. It interacts with the loan data service to fetch the list of loans. If no loans are found, it raises a `LoanNotFoundError` exception. The method returns a list of loan dictionaries representing all loans in the system."""

        return self.loan_data_service.get_all_loans_list()

    def get_loan_by_id(self, loan_id):  # done
        """This method retrieves a specific loan record by its ID. It checks if the provided loan ID is valid and exists in the database. If the loan is found, it returns a `Loan` object representing the loan data. If the loan ID is not provided or is of an incorrect type, it raises appropriate exceptions. If no loan with the given ID exists, it raises a `LoanNotFoundError` exception."""

        if loan_id is None:
            raise exc.DataError("Please provide loan ID to retrieve loan data.")

        if not isinstance(loan_id, int):
            raise exc.DataTypeError(
                "Please provide correct type of loan ID to retrieve loan data."
            )

        all_loans = self.get_all_loans()

        for loan in all_loans:
            if loan_id == loan.get("loan_id"):
                return Loan(**loan)

        raise exc.LoanNotFoundError(f"Loan with ID: {loan_id} not found in database.")

    ### EXISTENCE CHECKS

    def loan_exists_by_id(self, loan_id):  # done
        """This method checks if a loan with the given ID exists in the database. It attempts to retrieve the loan using the `get_loan_by_id` method. If the loan is found, it returns True; otherwise, it returns False. This method is useful for fetching loan details based on the loan ID."""

        try:
            self.get_loan_by_id(loan_id)
            return True
        except exc.LoanNotFoundError:
            return False

    def ensure_loan_exists(self, loan_id):  # done
        """This method ensures that a loan with the given ID exists. This method is used before the operations that require the loan to exist. It enforces corectness by raising an exception if the loan is missing."""

        self.get_loan_by_id(loan_id)

    ### GLOBAL RETRIEVE

    def get_active_loans(self):  # done
        """This method retrieves all active loans from the database. Active loans are defined as loans where the return date is not set (i.e., the book has not been returned yet). The method fetches all loans and filters them to include only those that are currently active. If no loans are found, it returns an empty list."""

        try:
            all_loans = self.get_all_loans()
        except exc.LoanNotFoundError:
            all_loans = []

        active_loans = []

        for loan in all_loans:
            if loan["return_date"] is None:
                active_loans.append(loan)

        return active_loans

    def get_overdue_books(self):  # done
        """This method retrieves all overdue loans from the database. Overdue loans are defined as active loans where the return date has passed the current date. The method fetches all active loans and checks their return dates against the current date. If a loan is found to be overdue, it is added to the list of overdue loans. The method returns a list of dictionaries representing the overdue loans. If no overdue loans are found, it returns an empty list."""

        active_loans = self.get_active_loans()

        overdue_loans = []

        today = datetime.now().date()

        for loan in active_loans:
            return_date_str = loan["return_date"]
            return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
            if today > return_date:
                overdue_loans.append(loan)

        return overdue_loans

    ### VALIDATION HELPERS

    def ensure_user_has_permission_to_borrow(self):  # done
        """This method checks if the current user has permission to borrow a book. It uses the `UserAuthorisation` service to verify the user's permissions. If the user does not have the required permission, it raises a `PermissionError` exception."""
        self.user_authorisation_service.check_permission("books.borrow_book")

    def ensure_book_available(self, book_id):  # done
        """Veryfing that book status is 'available' and book can be borrowed by user."""

        if not self.book_service.is_book_available(book_id=book_id):
            raise exc.BookNotAvailableError("Book is currently unavailable.")

    ### STATUS CHECKS

    def is_book_borrowed(self, book_id):
        """This method checks if a book is currently borrowed. It retrieves the book by its ID using the `BookService` and checks its status. If the book's status is "borrowed," it returns True; otherwise, it returns False. This method is useful for determining whether a specific book is currently checked out or available for borrowing."""
        book = self.book_service.get_book_by_id(book_id)

        return book.book_status == "borrowed"

    def is_book_overdue(self, book_id):  # done
        """This method checks if a book is currently overdue. It first ensures that the book exists using the `BookService`. Then, it checks if the book is currently borrowed. If the book is not borrowed, it returns False. If the book is borrowed, it retrieves the list of overdue loans and checks if the specific book ID is present in that list. If the book is found in the overdue loans, it returns True; otherwise, it returns False."""

        self.book_service.ensure_book_exists(book_id)

        if not self.is_book_borrowed(book_id):
            return False

        overdue_loans = self.get_overdue_books()

        for loan in overdue_loans:
            if loan["book_id"] == book_id:
                return True

        return False

    ### USER‑FOCUSED RETRIEVE

    def get_books_borrowed_by_user(self, user_id):  # done
        """This method retrieves a list of books currently borrowed by a specific user. It first checks if the provided user ID is valid and exists in the database. Then, it fetches all active loans and filters them to include only those associated with the given user ID. For each loan found, it retrieves the corresponding book details using the `BookService`. The method returns a list of dictionaries representing the books borrowed by the user. If no books are found for the user, it returns an empty list."""

        if user_id is None:
            raise exc.DataError(
                "Please provide user ID to retrieve list with books borrowed by user."
            )

        if not isinstance(user_id, int):
            raise exc.DataTypeError(
                "Please provide correct type of user ID to retrieve list with books borrowed by user."
            )

        active_loans = self.get_active_loans()

        user_loans = []

        for loan in active_loans:
            if loan["user_id"] == user_id:
                user_loans.append(loan)

        user_books = []

        for loan in user_loans:
            book = self.book_service.get_book_by_id(loan["book_id"])
            user_books.append(book)

        return user_books

    def get_user_overdue_books(self, user_id):  # done
        """This method retrieves a list of overdue books for a specific user. It first checks if the provided user ID is valid and exists in the database. Then, it fetches all books borrowed by the user and checks each book to determine if it is overdue using the `is_book_overdue` method. The method returns a list of dictionaries representing the overdue books for the user. If no overdue books are found, it returns an empty list."""

        if user_id is None:
            raise exc.DataError("Please provide user ID to retrieve user overdue books")

        if not isinstance(user_id, int):
            raise exc.DataTypeError(
                "Please provide user ID to retrieve user overdue books"
            )

        user_borrowed_books = self.get_books_borrowed_by_user(user_id)

        overdue_books = []

        for book in user_borrowed_books:
            if self.is_book_overdue(book["book_id"]):
                overdue_books.append(book)

        return overdue_books

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

        if book_id is None:
            raise exc.BookValidationError(
                "Please provide book ID to proceed borrowing the book."
            )

        if not isinstance(book_id, int):
            raise exc.BookValidationError("Book ID must be a number.")

        current_user = self.user_authorisation_service.get_current_user()

        if not current_user:
            raise exc.PermissionError("User must be logged in to borrow a book.")

        self.ensure_user_has_permission_to_borrow()

        self.ensure_book_available(book_id)

        now = datetime.now()

        loan_date = now.strftime("%Y-%m-%d")
        return_date = (now + timedelta(days=21)).strftime("%Y-%m-%d")

        new_loan = Loan(
            user_id=current_user.user_id,
            book_id=book_id,
            loan_date=loan_date,
            return_date=return_date,
        )

        try:
            all_loans = self.get_all_loans()
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
