"""
This module contains security helpers like password hashing and verification.
"""

import hashlib
import exceptions as exc


def hash_password(password: str):
    """This function takes a user's password and returns a hashed version of it using SHA-256 algorithm."""
    if not password:
        raise exc.SecurityError("Password cannot be an empty value.")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def verify_password(password, password_hash):
    """This function takes a user's password and a hashed password, hashes the input password, and compares it to the hashed version to verify if they match."""
    hashed_password = hash_password(password)

    if not password or not password_hash:
        return False

    return hashed_password == password_hash


def validate_password_strength(password):
    if not password:
        raise exc.PasswordValidationError("Password cannot be an empty value.")

    if len(password) < 8:
        raise exc.PasswordValidationError(
            "Password must be at least 8 characters long."
        )

    if not any(letter.isupper() for letter in password):
        raise exc.PasswordValidationError(
            "Password must contain at least one uppercase letter."
        )

    if not any(character.isdigit() for character in password):
        raise exc.PasswordValidationError("Password must contain at least one digit.")

    return True
