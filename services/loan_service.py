# managing loan operations like: borrow, return, view loans, check book availability

"""
________________________________________________________
services.loan_service
========================================================
Service for managing loans-related operations.
________________________________________________________

file status: on hold
until: loan model is rebuilt


Methods to implement:

### CORE
- borrow_book(user_id, book_id)
- return_book(book_id)

### VALIDATION
- validate_book_available(book_id)
- validate_user_can_borrow(user_id

### RETRIEVE
- get_borrowed_books()
- get_books_borrowed_by_user(user_id)
- get_overdue_books()

### STATUS CHECKS
- is_book_borrowed(book_id) -> bool
- is_book_overdue(book_id) -> bool

### OTHER
- get_overdue_books()

"""

import exceptions as exc
from models.book import Book
from models.user import User
from services.authorisation_service import UserAuthorisation
from services.book_service import BookService


class LoanService:
    def __init__(
        self,
        user_id,
        book_id,
        borrow_date,
        return_date,
        borrowed_by,
        authorisation: UserAuthorisation,
    ):
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.borrowed_by = borrowed_by
        self.authorisation = authorisation

    def loan_book(self):
        pass
        # this method is not done yet. I need manage JSON files first.
        # self.logged_user = User(user_id=self.user_id)
        # self.authorisation.login()

        # # if self.logged_user not in users:

        # if not self.logged_user:
        #     raise exc.UserError("User is not logged into system.")

        # self.book_to_loan = Book()
        # self.authorisation.check_permission("borrow_book")

        # user_permission = False

        # if self.logged_user: # if logged user permission is true
        #     BookService.is_book_available(book=self.book_to_loan)

    def return_book(self):
        self.authorisation.check_permission("return_book")
        pass

    def reserve_book(self):
        self.authorisation.check_permission("book_the_book")
        pass
