"""
________________________________________________________
services.book_service
========================================================
Service for managing book-related operations.
________________________________________________________

This module defines the `BookService` class responsible for handling all operations
related to books in the system. It interacts with the storage layer (e.g. JSON service)
to perform CRUD operations and provides high-level methods for working with book data.

The service focuses ONLY on book data and does NOT handle borrowing, reservations,
or user interactions. These responsibilities belong to LoanService.

file status: in progress
________________________________________________________

CHECKLIST - METHODS TO IMPLEMENT
========================================================

[CORE]
--------------------------------------------------------
1. add_book(book: Book)
2. get_all_books()

--------------------------------------------------------

[SEARCH / RETRIEVE]
--------------------------------------------------------

3.  get_book_by_id(book_id)
- get_books_by_title(title)
- get_books_by_keyword(keyword)
- get_books_by_year(year)
7. get_books_by_category(category)

--------------------------------------------------------

[EXISTENCE CHECKS]
--------------------------------------------------------
8.  book_exists_by_id(book_id) -> bool
- book_exists_by_title(title) -> bool
10. ensure_book_exists(book_id)

--------------------------------------------------------

[AVAILABILITY]
--------------------------------------------------------
11. is_book_available(book_id) -> bool
12. get_available_books()
13. get_unavailable_books()

--------------------------------------------------------

[UPDATE – GENERIC]
--------------------------------------------------------


--------------------------------------------------------

[UPDATE – DOMAIN SPECIFIC]
--------------------------------------------------------
14. update_book_data(book_id, field, new_value)
- update_book_title(book_id, new_title)
- update_book_author(book_id, new_author)
- update_book_year(book_id, new_year)
- update_book_category(book_id, new_category)
19. update_book_quantity(book_id, new_quantity)

--------------------------------------------------------
[DELETE]
--------------------------------------------------------
20. - delete_book(book_id)

[FILTERING / LISTING]
--------------------------------------------------------
- get_books_by_author(author)
- get_books_by_category(category)

--------------------------------------------------------

[HELPERS]
--------------------------------------------------------
- get_book_title(book_id)
- get_book_author(book_id)
- get_book_category(book_id)
- get_book_year(book_id)

--------------------------------------------------------

IMPORTANT DESIGN RULES
========================================================

- BookService handles ONLY book data.
- BookService does NOT:
    * borrow books
    * return books
    * manage reservations
    * assign books to users

→ These responsibilities belong to LoanService.

- Authorisation (permissions) is NOT handled here.
→ It must be checked BEFORE calling BookService methods.

- Following the same structure and patterns as UserService:
    * get_* → returns data or raises exception
    * exists_* → returns True / False
    * ensure_* → raises exception
    * update_* → validates and delegates to storage layer

________________________________________________________
"""

import exceptions as exc
from database.book_json_file_service import BookJsonFileService
from models.book import Book
from utils.helpers import generate_book_id


class BookService:
    def __init__(self, book_json_service: BookJsonFileService):
        self.book_json_service = book_json_service

    ### CORE

    def get_all_books(self):
        return self.book_json_service.get_all_books_list()

    def add_book(self, book: Book):
        """
        Add validation of: type book (if it is a correct book object), title, author, year
        """

        if not isinstance(book, Book):
            raise exc.DataTypeError("Please provide book as a book object")

        if not book.title or not book.title.strip():
            raise exc.BookValidationError("Please provide book title.")

        if not book.author or not book.author.strip():
            raise exc.BookValidationError("Please provide book author.")

        if book.publication_year is None:
            if not isinstance(book.publication_year, int):
                raise exc.BookValidationError("Year must be an integer.")

            if book.publication_year < 1200 or book.publication_year > 2050:
                raise exc.BookValidationError("Year must be a valid year.")

        all_books = self.get_all_books()

        book_id = generate_book_id(all_books)

        book.book_id = book_id

        return self.book_json_service.add_book_data(book.to_dict())

    # 3.  get_book_by_id(book_id)
    # - get_books_by_title(title)
    # - get_books_by_keyword(keyword)
    # - get_books_by_year(year)
    # 7. get_books_by_category(category)

    ### SEARCH / RETRIEVE

    def get_book_by_id(self, book_id):
        if not isinstance(book_id, int):
            raise exc.DataTypeError(
                "Please provide correct type of book ID to retrieve book data."
            )

        if book_id is None:
            raise exc.DataError("Please provide book ID to retrieve book data.")

        all_books = self.get_all_books()

        for book in all_books:
            if book_id == book.get("book_id"):
                return Book(**book)

        raise exc.BookNotFoundError(f"Book with ID: {book_id} not found in database.")

    def get_books_by_title(self):
        pass

    def get_books_by_keyword(self):
        pass

    def get_books_by_year(self):
        pass

    def get_books_by_category(self):
        pass
