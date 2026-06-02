# small functions used across the project, eg. generating book IDs, date formatting, etc.

import random


def generate_user_id(users):
    while True:
        user_id = random.randint(100000, 999999)
        exists = False

        for user in users:
            if user["user_id"] == user_id:
                exists = True
                break

        if not exists:
            return user_id


def generate_book_id():
    pass


def generate_loan_id():
    pass


def generate_reservation_id():
    pass


def normalize_username(username):
    pass


def format_date(date):
    pass
