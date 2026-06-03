# managing book  operations like: add, edit, search, sort, delete, display

"""
________________________________________________________________________
services.book_service.py
========================================================================
Managing book operations e.g.: add, edit, search, sort, delete, display
________________________________________________________________________


TO DO HERE:
- Check if all methods are implemented
- Prepare docstrings.
- Add and verify permissions <-- Related to authorisation service works.


Core:
- dodawanie książki
- edycja danych książki
- usuwanie książki
- pobieranie listy książek

Wyszukiwanie i filtrowanie:
- wyszukiwanie po tytule / autorze / kategorii
- filtrowanie książek (np. dostępne)
- sortowanie (np. alfabetycznie, data dodania)

Stan książki:
- sprawdzanie czy książka istnieje
- sprawdzanie czy książka jest aktywna (np. nieusunięta)

"""

from models.book import Book
import exceptions as exc
from services.authorisation_service import UserAuthorisation


class BookService:
    def __init__(self, auth: UserAuthorisation):
        self.books = []
        self.auth = auth

    def add_book(self, book: Book):
        self.auth.check_permission("add_book")

        if not book.author or not book.title:
            raise exc.InvalidBookDataError(
                'Fields "author" and "title" cannot be empty.'
            )
        self.books.append(book)

    def edit_book(
        self, book: Book, title=None, author=None, year=None
    ):  # Method not done yet.
        self.auth.check_permission("edit_book")
        if book not in self.books:
            raise exc.BookNotFoundError("Book not found in the library")

        if title:
            book.title = title
        if author:
            book.author = author
        if year:
            book.year = year

    def delete_book(self, book: Book):
        self.auth.check_permission("delete_book")
        if book not in self.books:
            raise exc.BookNotFoundError("Book not found in the library")
        self.books.remove(book)

    def search_books(
        self,
        title=None,
        author=None,
        year=None,
        searched_term=None,
        raise_if_not_found=False,
    ):
        self.auth.check_permission("search_book")

        title_normalized = None
        author_normalized = None
        searched_term_normalized = None
        year_normalized = None

        if title:
            title_normalized = title.strip().lower()
        if author:
            author_normalized = author.strip().lower()

        if searched_term is not None:
            searched_term_normalized = str(searched_term).strip().lower()

        if year is not None:
            try:
                year_normalized = int(str(year).strip())
            except ValueError:
                raise exc.BookValidationError("Year must be an 4-digit integer.")

            if year_normalized < 1200 or year_normalized > 2050:
                raise exc.BookValidationError(
                    "Year must be a valid 4-digit year with real year value."
                )

        if not (
            title_normalized
            or author_normalized
            or searched_term_normalized
            or year_normalized
        ):
            raise exc.SearchValueError(
                "At least one search criteria must be provided (title, author, year, or searched_term)"
            )

        results = []

        for book in self.books:
            match = True

            if title_normalized and title_normalized not in book.title.lower():
                match = False

            if author_normalized and author_normalized not in book.author.lower():
                match = False

            if year_normalized is not None and year_normalized != book.year:
                match = False

            if searched_term_normalized:
                if (
                    searched_term_normalized not in book.title.lower()
                    and searched_term_normalized not in book.author.lower()
                    and searched_term_normalized != str(book.year)
                ):
                    match = False

            if match:
                results.append(book)

        if not results and raise_if_not_found:
            raise exc.BookNotFoundError("No books found matching the provided criteria")

        return results

    def get_books_by_category(self, category):
        self.auth.check_permission("view_books")
        books_in_category = []
        for book in self.books:
            if category in book.categories:
                books_in_category.append(book)
        return books_in_category

    def is_book_available(self, book: Book):
        self.auth.check_permission("view_books")
        if book not in self.books:
            raise exc.BookNotFoundError("Book not found in the library")
        return getattr(book, "is_available", True)

    def get_available_books(self):
        self.auth.check_permission("view_books")
        available_books = []
        for book in self.books:
            if getattr(book, "is_available", True):
                available_books.append(book)
        return available_books

    def get_all_books(self):
        self.auth.check_permission("view_books")
        return self.books

    def get_all_categories(self):
        self.auth.check_permission("view_books")
        categories = set()
        for book in self.books:
            categories.update(book.categories)
        return list(categories)
