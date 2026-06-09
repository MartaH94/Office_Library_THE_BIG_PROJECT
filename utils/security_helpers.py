"""
This module contains security helpers like password hashing and verification.
"""

import hashlib

import exceptions as exc


def hash_password(password: str) -> str:
    """This function takes a user's password and returns a hashed version of it using SHA-256 algorithm."""
    if not password:
        raise exc.SecurityError("Password cannot be an empty value.")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def verify_password(password: str, password_hash: str) -> bool:
    """This function takes a user's password and a hashed password, hashes the input password, and compares it to the hashed version to verify if they match."""

    if not password or not password_hash:
        return False

    hashed_password = hash_password(password)

    return hashed_password == password_hash


def validate_password_strength(password: str) -> bool:
    """This function checks if the password meets certain strength criteria, such as minimum length, presence of uppercase letters, and digits. It raises a PasswordValidationError if any of the criteria are not met."""
    if not password:
        raise exc.PasswordValidationError("Password cannot be an empty value.")

    if len(password) < 8:
        raise exc.PasswordValidationError(
            "Password must be at least 8 characters long."
        )

    if not any(character.isupper() for character in password):
        raise exc.PasswordValidationError(
            "Password must contain at least one uppercase letter."
        )

    if not any(character.isdigit() for character in password):
        raise exc.PasswordValidationError("Password must contain at least one digit.")

    if not any(not character.isalnum() for character in password):
        raise exc.PasswordValidationError(
            "Password must contain at least one alphanumeric character."
        )

    return True
