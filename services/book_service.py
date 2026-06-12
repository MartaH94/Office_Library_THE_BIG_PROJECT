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


CHECKLIST – METHODS TO IMPLEMENT
========================================================

[CORE – CRUD]
--------------------------------------------------------
- add_book(book: Book) - done
- get_all_books() - done
- get_book_by_id(book_id) - done
- update_book_data(book_id, field, new_value)
- delete_book(book_id)

--------------------------------------------------------

[EXISTENCE CHECKS]
--------------------------------------------------------
- book_exists_by_id(book_id) -> bool
- ensure_book_exists(book_id)

--------------------------------------------------------

[SEARCH]
--------------------------------------------------------
- get_books_by_keyword(keyword)
    → main search method (title, author, category, etc.)

- get_books_by_year(year)
    → separate because year is exact-match data

--------------------------------------------------------

[AVAILABILITY]
--------------------------------------------------------
- is_book_available(book_id) -> bool
- get_available_books()

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

    ### EXISTENCE CHECKS

    def book_exists_by_id(self, book_id):

        try:
            self.get_book_by_id(book_id)
            return True
        except exc.BookNotFoundError:
            return False

    def ensure_book_exists(self, book_id):

        self.get_book_by_id(book_id)

    ### CRUD

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

    def update_book_data(self, book_id, field, new_value):
        pass

    def delete_book(self, book_id):
        pass

    ### SEARCH

    def get_books_by_keyword(self):
        """MAIN SEARCH METHOD"""
        pass

    def get_books_by_year(self):
        pass

    def get_books_by_title(self, title):
        """This method will be removed and replaced with searching by keyword."""

        if not isinstance(title, str):
            raise exc.DataTypeError(
                "Please provide correct type of book title to retrieve data."
            )

        if not title.strip():
            raise exc.DataError("Please provide book title to retrieve data.")

        searched_title = title.strip().lower()
        all_books = self.get_all_books()

        search_result = []

        for book in all_books:
            stored_book_title = book.get("title", "").lower()
            if searched_title in stored_book_title:
                search_result.append(Book(**book))

        if not search_result:
            raise exc.BookNotFoundError(
                f"No books found matching title: {searched_title}"
            )

        return search_result

    ### AVAILABILITY

    def is_book_available(self, book_id):
        pass

    def get_available_books(self):
        pass
