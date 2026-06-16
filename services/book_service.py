"""
________________________________________________________
services.book_service
========================================================
Service for managing book-related operations.
________________________________________________________

This module defines the `BookService` class responsible for handling all operations
related to books in the system. It interacts with the storage layer (e.g. JSON service)
to perform CRUD operations and provides high-level methods for working with book data.


file status: in progress
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

    def get_book_by_id(self, book_id):

        if book_id is None:
            raise exc.DataError("Please provide book ID to retrieve book data.")

        if not isinstance(book_id, int):
            raise exc.DataTypeError(
                "Please provide correct type of book ID to retrieve book data."
            )

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
            raise exc.BookValidationError("Publication year is required.")

        if not isinstance(book.publication_year, int):
            raise exc.BookValidationError("Year must be an integer.")

        if book.publication_year < 1200 or book.publication_year > 2050:
            raise exc.BookValidationError("Year must be a valid year.")

        all_books = self.get_all_books()

        book_id = generate_book_id(all_books)

        book.book_id = book_id

        return self.book_json_service.add_book_data(book.to_dict())

    def update_book_data(self, book_id, field, new_value):
        self.ensure_book_exists(book_id)

        if not isinstance(field, str):
            raise exc.DataTypeError("Field name must be a string value type.")

        if not field.strip():
            raise exc.ValidationError("Selected field to update is an empty value.")

        if new_value is None:
            raise exc.ValidationError("New value to update cannot be an empty value.")

        updated_book_data = self.book_json_service.update_book_data(
            book_id=book_id, field=field, new_value=new_value
        )

        return updated_book_data

    def delete_book(self, book_id):
        self.ensure_book_exists(book_id)

        return self.book_json_service.delete_book_by_id(book_id)

    ### SEARCH

    def get_books_by_keyword(self, keyword):
        """MAIN SEARCH METHOD"""
        if not isinstance(keyword, str):
            raise exc.DataTypeError(
                "Please provide correct type of keyword to retrieve data."
            )

        if not keyword.strip():
            raise exc.DataError("Please provide keyword to retrieve data.")

        searched_keyword = keyword.strip().lower()
        all_books = self.get_all_books()

        search_results = []

        for book in all_books:
            stored_book_title = book.get("title", "").lower()
            stored_book_author = book.get("author", "").lower()
            if (
                searched_keyword in stored_book_title
                or searched_keyword in stored_book_author
            ):
                search_results.append(Book(**book))

        if not search_results:
            raise exc.BookNotFoundError(
                f"No books found matching keyword: {searched_keyword}"
            )

        return search_results

    def get_books_by_year(self, year):
        if not isinstance(year, int):
            raise exc.DataTypeError(
                "Please provide correct type of year to retrieve data."
            )

        if year < 1200 or year > 2050:
            raise exc.DataError(
                "Please provide valid year of publication to retrieve data."
            )

        all_books = self.get_all_books()
        search_results = []

        for book in all_books:

            stored_book_year = book.get("publication_year")

            if year == stored_book_year:
                search_results.append(Book(**book))

        if not search_results:
            raise exc.BookNotFoundError(f"No books found published in year: {year}")

        return search_results

    def get_books_by_category(self, category):
        if not isinstance(category, str):
            raise exc.DataTypeError(
                "Please provide correct type of category to retrieve data."
            )

        if not category.strip():
            raise exc.DataError("Please provide category to retrieve data.")

        all_books = self.get_all_books()

        search_results = []
        searched_category = category.strip().lower()

        for book in all_books:
            stored_book_categories = book.get("category", [])

            for stored_category in stored_book_categories:
                if searched_category == stored_category.lower():
                    search_results.append(Book(**book))
                    break

        if not search_results:
            raise exc.BookNotFoundError(f"No books found in category: {category}")

        return search_results

    ### AVAILABILITY

    def is_book_available(self, book_id):

        book = self.get_book_by_id(book_id)

        return book.book_status == "available"

    def get_available_books(self):

        all_books = self.get_all_books()

        available_books = []

        for book in all_books:
            if book.get("book_status", "") == "available":
                available_books.append(Book(**book))

        if not available_books:
            raise exc.BookNotAvailableError("No books are available.")

        return available_books
