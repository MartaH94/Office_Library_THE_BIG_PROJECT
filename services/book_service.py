"""
________________________________________________________
services.book_service
========================================================
Service for managing book-related operations.
________________________________________________________

This module defines the `BookService` class responsible for handling all operations
related to books in the system. It interacts with the storage layer (JSON service)
to perform CRUD operations and provides high-level methods for working with book data.


file status:
all methods are done
TO DO: Update docstrings
________________________________________________________


"""

import exceptions as exc
from database.book_json_file_service import BookJsonFileService
from models.book import Book
from utils.helpers import generate_book_id


class BookService:
    """This class provides methods to manage book-related operations, including retrieval, addition, updating, deletion, and searching of books. It interacts with the `BookJsonFileService` for data persistence."""

    def __init__(self, book_json_service: BookJsonFileService):
        self.book_json_service = book_json_service

    ### CORE

    def get_all_books(self):
        """This method retrieves all books from the storage layer and returns them as a list of dictionaries."""

        return self.book_json_service.get_all_books_list()

    def get_book_by_id(self, book_id):
        """This method retrieves a book by its ID. It raises exceptions if the ID is not provided, is of incorrect type, or if the book is not found. This method is useful for fetching specific book details based on the unique identifier."""

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
        """This method checks if a book exists by its ID. It returns True if the book exists, and False otherwise. It raises exceptions if the ID is not provided or is of incorrect type. This method is used for conditional checks when the program needs to decide what to do depending on whether the book exists.
        It does not raise an exception if the book is missing.
        """

        try:
            self.get_book_by_id(book_id)
            return True
        except exc.BookNotFoundError:
            return False

    def ensure_book_exists(self, book_id):
        """This method ensures that a book with the given ID exists. This method is used before operations that require the book to be present (e.g update, delete). It enforces correctness by raising an exception if the book is missing."""

        self.get_book_by_id(book_id)

    ### CORE

    def add_book(self, book: Book):
        """This method adds a new book to the storage layer. It performs validation checks on the provided `Book` object, ensuring that all required fields are present and valid. If the book is valid, it generates a unique book ID and saves the book data using the `BookJsonFileService`. It raises exceptions for invalid data types, missing fields, or invalid publication years."""

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
        """This method updates a specific field of a book identified by its ID. It performs validation checks on the provided `book_id`, `field`, and `new_value`. If the book exists and the inputs are valid, it updates the book data using the `BookJsonFileService`. It raises exceptions for invalid data types, missing fields, or if the book does not exist."""

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

    def mark_book_as_borrowed(self, book_id, user_id, due_date, loan_date):
        """This method marks a book as borrowed by updating its status and related fields. It takes the `book_id`, `user_id`, `due_date`, and `loan_date` as parameters. It first ensures that the book exists, then updates the relevant fields in the book's data to reflect that it has been borrowed. The method raises exceptions if the book does not exist or if any of the inputs are invalid."""

        self.ensure_book_exists(book_id)

        self.update_book_data(book_id, "borrower_id", user_id)
        self.update_book_data(book_id, "due_date", due_date)
        self.update_book_data(book_id, "last_loan_date", loan_date)
        self.update_book_data(book_id, "book_status", "borrowed")

    def delete_book(self, book_id):
        """This method deletes a book from the storage layer based on its ID. It first ensures that the book exists, then calls the `delete_book_by_id` method of the `BookJsonFileService` to remove the book data. It raises exceptions if the book does not exist or if the provided ID is invalid."""

        self.ensure_book_exists(book_id)

        return self.book_json_service.delete_book_by_id(book_id)

    ### SEARCH

    def get_books_by_keyword(self, keyword):
        """This method searches for books based on a provided keyword. It checks if the keyword is a valid string and not empty. The method retrieves all books and filters them based on whether the keyword is present in the book's title or author. It returns a list of matching `Book` objects. If no matches are found, it raises a `BookNotFoundError` exception."""

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
        """This method searches for books based on a provided publication year. It checks if the year is a valid integer and within a reasonable range (1200 to 2050). The method retrieves all books and filters them based on whether their publication year matches the provided year. It returns a list of matching `Book` objects. If no matches are found, it raises a `BookNotFoundError` exception."""

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
        """This method searches for books based on a provided category. It checks if the category is a valid string and not empty. The method retrieves all books and filters them based on whether their categories include the provided category. It returns a list of matching `Book` objects. If no matches are found, it raises a `BookNotFoundError` exception."""

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
        """This method checks if a book is available for borrowing based on its ID. It retrieves the book using the `get_book_by_id` method and checks its status. If the book is available, it returns True; otherwise, it returns False. It raises exceptions if the book does not exist or if the provided ID is invalid."""

        book = self.get_book_by_id(book_id)

        return book.book_status == "available"

    def get_available_books(self):
        """This method retrieves all books that are currently available for borrowing. It filters the list of all books based on their status and returns a list of `Book` objects that are marked as available. If no books are available, it raises a `BookNotAvailableError` exception."""

        all_books = self.get_all_books()

        available_books = []

        for book in all_books:
            if book.get("book_status", "") == "available":
                available_books.append(Book(**book))

        if not available_books:
            raise exc.BookNotAvailableError("No books are available.")

        return available_books
