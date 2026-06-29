"""
________________________________________________________
exceptions
========================================================
Module for defining custom exceptions used in the library management system.
________________________________________________________

This module contains custom exception classes that are used throughout the library management system. These exceptions are organized into categories based on their purpose, such as book-related exceptions, loan and reservation exceptions, user and authentication exceptions, general utility exceptions, and security exceptions. Each exception class provides a specific error message and can be raised when certain conditions are met in the application.

"""


# ------------------------------
# BASE EXCEPTION FOR THE ENTIRE PROJECT
# ------------------------------
class LibraryError(Exception):
    """Base exception for the entire library system."""

    pass


# ------------------------------
# BOOK-RELATED EXCEPTIONS (BookService)
# ------------------------------
class BookError(LibraryError):
    """Base exception for book operations."""

    pass


# CRUD operations
class InvalidBookDataError(BookError):
    """Raised when user tries to add a book with empty title or author."""

    def __init__(self, message="Field author and title canot be empty", book=None):
        super().__init__(message)
        self.book = book


class SearchValueError(BookError):
    """Raised when no search criteria is provided."""

    def __init__(
        self,
        message="At least one search criteria must be provided (title, author, year, or searched_term)",
    ):
        super().__init__(message)


class BookNotFoundError(BookError):
    """Raised when book not found in the library."""

    def __init__(self, message="Book not found in the library", book=None):
        super().__init__(message)
        self.book = book


class BookAlreadyExistsError(BookError):
    """Book already exists in the library."""

    pass


# Availability
class BookNotAvailableError(BookError):
    """Book is currently unavailable (loaned or reserved)."""

    pass


# Categories
class CategoryNotFoundError(BookError):
    """Category not found."""

    pass


# Validation
class BookValidationError(BookError):
    """Invalid book data."""

    def __init__(self, message="Invalid book data"):
        super().__init__(message)


# ------------------------------
# LOAN AND RESERVATION EXCEPTIONS (LoanService)
# ------------------------------
class LoanError(LibraryError):
    """Base exception for loans and reservations."""

    pass


class LoanNotFoundError(LoanError):
    """Loan record not found in database."""

    def __init__(self, message="Loan ID not found in the loans file"):
        super().__init__(message)

    pass


class ReservationError(LoanError):
    """Error during book reservation."""

    pass


class ReservationValidationError(LoanError):
    """Error during validation reservation data."""

    pass


class ReservationNotFoundError(LoanError):
    """Reservation does not exists in a database."""

    pass


class AlreadyLoanedError(LoanError):
    """Book is already loaned to this user."""

    pass


class LoanValidationError(LoanError):
    """Invalid loan or reservation data."""

    def __init__(self, message="Loan data are invalid or loan data are empty value."):
        super().__init__(message)

    pass


# ------------------------------
# USER AND AUTHENTICATION EXCEPTIONS (AuthService)
# ------------------------------
class UserError(LibraryError):
    """Base exception for user-related operations."""

    pass


class UserNotFoundError(UserError):
    """User not found in database json file."""

    def __init__(self, message="User does not exist in users json file"):
        super().__init__(message)


class AuthenticationError(UserError):
    """Authentication or login error."""

    pass


class PermissionError(UserError):
    """User does not have permission to perform this operation."""

    def __init__(
        self, message="User does not have permission to perform this operation"
    ):
        super().__init__(message)

    pass


class UserValidationError(UserError):
    """Invalid user data."""

    def __init__(self, message="User ID data are invalid or user ID is empty value"):
        super().__init__(message)


class UserInvalidRole(UserError):
    """Invalid user role."""

    pass


# ------------------------------
# GENERAL / UTILITY EXCEPTIONS
# ------------------------------
class ValidationError(LibraryError):
    """General validation error for input data."""

    pass


class DatabaseError(LibraryError):
    """Error related to database operations or data storage."""

    pass


class FileNotFound(LibraryError):
    """File not found in the folder."""

    def __init__(self, message="File doesn't exists in the catalogue."):
        super().__init__(message)


class FileError(LibraryError):
    """Error during file operations (JSON, CSV, etc.)."""

    pass


class InvalidFieldError(FileError):
    """Field to change in json file does not exist."""

    def __init__(self, message="Field does not exists in the json file."):
        super().__init__(message)


class BackupError(FileError):
    """General error for backup file"""

    pass


class BackupPermissionError(FileError):
    """Error during checking permission during creating or reading backup file"""

    pass


class DataError(FileError):
    """Provided data is an empty value."""

    def __init__(self, message="Incorrect data value: data cannot be empty value."):
        super().__init__(message)


class DataTypeError(FileError):
    """Provided data has invalid type."""

    def __init__(self, message="Data has invalid data type"):
        super().__init__(message)


# ------------------------------
# SECURITY EXCEPTIONS
# ------------------------------


class SecurityError(LibraryError):
    """Base exception for security-related issues."""

    pass


class PasswordSecurityError(SecurityError):
    """Error during password hashing or verification."""

    pass


class PasswordValidationError(SecurityError):
    """Password does not meet strength requirements."""

    pass
