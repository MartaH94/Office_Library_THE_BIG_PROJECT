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

[CORE - CREATE / DELETE]
--------------------------------------------------------
- add_book(book: Book)
- delete_book(book_id)

--------------------------------------------------------

[SEARCH / RETRIEVE]
--------------------------------------------------------
- get_all_books()
- get_book_by_id(book_id)
- get_books_by_title(title)
- get_books_by_keyword(keyword)
- get_books_by_year(year)
- get_books_by_category(category)

--------------------------------------------------------

[EXISTENCE CHECKS]
--------------------------------------------------------
- book_exists_by_id(book_id) -> bool
- book_exists_by_title(title) -> bool
- ensure_book_exists(book_id)

--------------------------------------------------------

[AVAILABILITY]
--------------------------------------------------------
- is_book_available(book_id) -> bool
- get_available_books()
- get_unavailable_books()

--------------------------------------------------------

[UPDATE – GENERIC]
--------------------------------------------------------
- update_book_data(book_id, field, new_value)

--------------------------------------------------------

[UPDATE – DOMAIN SPECIFIC]
--------------------------------------------------------
- update_book_title(book_id, new_title)
- update_book_author(book_id, new_author)
- update_book_year(book_id, new_year)
- update_book_category(book_id, new_category)
- update_book_quantity(book_id, new_quantity)

--------------------------------------------------------

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


class BookService:
    def __init__(self, book_json_service: BookJsonFileService):
        self.book_json_service = book_json_service
