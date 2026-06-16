# small functions used across the project, eg. generating book IDs, date formatting, etc.

"""
TO DO HERE:
- update module docstring
- implement function generate loan id
- implement function generate reservation id
- implement function normalize username
- implement function format date


"""

import random

import exceptions as exc


# ID generation functions
def generate_user_id(users):
    """This function generates a unique user ID by creating a random 6-digit number and checking it against existing user IDs in the database to ensure uniqueness. It takes a list of existing users as input and returns a unique user ID.
    Args:
        users (list): A list of existing user records, where each record is a dictionary containing user information, including the user ID.
    Returns:
        int: A unique user ID that does not exist in the provided list of users.
    """
    while True:
        user_id = random.randint(100000, 999999)
        exists = False

        for user in users:
            if user["user_id"] == user_id:
                exists = True
                break

        if not exists:
            return user_id


def generate_book_id(books):
    while True:
        book_id = random.randint(1000000, 9999999)
        exists = False

        for book in books:
            if book["book_id"] == book_id:
                exists = True
                break
        if not exists:
            return book_id


def generate_loan_id():
    pass


def generate_reservation_id():
    pass


# Validation functions


def validate_email(email: str) -> bool:
    if not email:
        raise exc.ValidationError("Please provide your email address.")

    if "@" not in email:
        raise exc.ValidationError("Please provide a valid email format.")

    email_parts = email.split("@")

    if len(email_parts) != 2:
        raise exc.ValidationError("Please provide a valid email format.")

    username_part, domain = email_parts

    if not username_part:
        raise exc.ValidationError(
            "Please provide a username before '@' in the email address."
        )

    if not domain:
        raise exc.ValidationError("Please provide a domain in email address.")

    if "." not in domain or domain.startswith("."):
        raise exc.ValidationError("Please provide a valid domain value.")

    return True


def normalize_username(username):
    pass


def format_date(date):
    pass
