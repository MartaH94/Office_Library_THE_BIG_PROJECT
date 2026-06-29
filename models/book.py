"""
________________________________________________________
models.book
========================================================
Module for defining the Book class and BookCategory class.
________________________________________________________

This module contains the definition of the Book class, which represents a book in the library system, and the BookCategory class, which represents a category of books. The Book class includes attributes such as author, title, publication year, ISBN, category, language, status, borrower ID, due date, and last loan date. The BookCategory class allows for grouping books into categories.

"""


class Book:
    def __init__(
        self,
        author: str,
        title: str,
        publication_year: int,
        isbn: str | None = None,
        category: list[str] | None = None,
        language: str | None = None,
    ):

        self.book_id: int | None = None

        self.author = author
        self.title = title
        self.publication_year = publication_year

        self.isbn = isbn
        self.category: list[str] = category or []
        self.language = language

        self.book_status = "available"
        self.borrower_id: int | None = None
        self.due_date: str | None = None
        self.last_loan_date: str | None = None

    def to_dict(self):
        """This method converts the Book object into a dictionary representation."""

        return {
            "book_id": self.book_id,
            "author": self.author,
            "title": self.title,
            "publication_year": self.publication_year,
            "isbn": self.isbn,
            "category": self.category,
            "language": self.language,
            "book_status": self.book_status,
            "borrower_id": self.borrower_id,
            "due_date": self.due_date,
            "last_loan_date": self.last_loan_date,
        }


class BookCategory:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        """This method adds a book to the category's list of books. It takes a Book object as an argument and appends it to the books list of the category."""

        self.books.append(book)
