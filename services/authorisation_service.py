"""
Docstring for services.authorisation_service
This module handles user authorisation, including login, logout, and permission checks.

TO DO HERE:
- Class UserAuthorisation review. Check if it may need more methods.
- Function has_permission review. Check if it covers all needed cases.
- Make sure that nested permissions are handled correctly.
- Split permissions for books, loans, user account actions.
- build functions to register and to login users.

"""

import exceptions as exc
from models.user import User
from utils.security_helpers import (
    hash_password,
    verify_password,
    validate_password_strength,
)

# managing registration, login, permissions and authorisation of users

user_permissions = {
    "reader": {
        "books": {
            "borrow_book": True,
            "return_book": True,
            "reserve_book": True,
            "add_book": False,
            "edit_book": False,
            "delete_book": False,
            "search_book": True,
            "view_books": True,
        },
        "account": {
            "update_account": False,
            "update_own_data": True,
            "reset_password": False,
            "view_borrow_history": True,
        },
        "actions": {
            "approve_reservations": False,
            "manage_users": False,
            "view_logs": False,
            "generate_reports": False,
            "delegate_permissions": False,
            "delete_data": False,
            "edit_data": False,
        },
        "sensitive_users_data": {
            "view_data": False,
            "edit_data": False,
            "delete_data": False,
        },
    },
    "admin": {
        "books": {
            "borrow_book": False,
            "return_book": False,
            "reserve_book": True,
            "add_book": True,
            "edit_book": True,
            "delete_book": True,
            "search_book": True,
            "view_books": True,
        },
        "account": {
            "update_account": True,
            "update_own_data": True,
            "reset_password": True,
            "view_borrow_history": True,
        },
        "actions": {
            "approve_reservations": False,
            "manage_users": True,
            "view_logs": True,
            "generate_reports": True,
            "delegate_permissions": True,
            "delete_data": True,
            "edit_data": True,
        },
        "sensitive_users_data": {
            "view_data": True,
            "edit_data": True,
            "delete_data": True,
        },
    },
    "librarian": {
        "books": {
            "borrow_book": False,
            "return_book": False,
            "reserve_book": True,
            "add_book": True,
            "edit_book": True,
            "delete_book": True,
            "search_book": True,
            "view_books": True,
        },
        "account": {
            "update_account": True,
            "update_own_data": True,
            "reset_password": False,
            "view_borrow_history": True,
        },
        "actions": {
            "approve_reservations": True,
            "manage_users": False,
            "view_logs": False,
            "generate_reports": True,
            "delegate_permissions": False,
            "delete_data": True,
            "edit_data": True,
        },
        "sensitive_users_data": {
            "view_data": True,
            "edit_data": True,
            "delete_data": False,
        },
    },
    "guest": {
        "books": {
            "borrow_book": False,
            "return_book": False,
            "reserve_book": True,
            "add_book": False,
            "edit_book": False,
            "delete_book": False,
            "search_book": True,
            "view_books": True,
        },
        "account": {
            "update_account": False,
            "update_own_data": False,
            "reset_password": False,
            "view_borrow_history": False,
        },
        "actions": {
            "approve_reservations": False,
            "manage_users": False,
            "view_logs": False,
            "generate_reports": False,
            "delegate_permissions": False,
            "delete_data": False,
            "edit_data": False,
        },
        "sensitive_users_data": {
            "view_data": False,
            "edit_data": False,
            "delete_data": False,
        },
    },
    "moderator": {
        "books": {
            "borrow_book": False,
            "return_book": False,
            "reserve_book": False,
            "add_book": True,
            "edit_book": True,
            "delete_book": False,
            "search_book": True,
            "view_books": True,
        },
        "account": {
            "update_account": False,
            "update_own_data": True,
            "reset_password": False,
            "view_borrow_history": True,
        },
        "actions": {
            "approve_reservations": False,
            "manage_users": False,
            "view_logs": True,
            "generate_reports": True,
            "delegate_permissions": False,
            "delete_data": False,
            "edit_data": True,
        },
    },
    "sensitive_users_data": {
        "view_data": True,
        "edit_data": False,
        "delete_data": True,
    },
}


### I am here
def user_registration(
    user_id, email, role, user_name, first_name, last_name, phone_number, password
):
    """This function is made for registering new users.

    Args:
        user_id (int): Unique identifier for the user.
        email (str): User's email address.
        role (str): User's role (e.g., "reader", "admin").
        user_name (str): User's username.
        first_name (str): User's first name.
        last_name (str): User's last name.
        phone_number (int): User's phone number.
        password (str): User's password.
    """
    pass


def user_login(user_name, password):
    pass


def has_permission(role: str, action_path: str) -> bool:
    """This function checks if a specific role has permission to perform a specific action.

    Args:
        role (str): The role name (e.g., "admin", "reader").
        action_path (str): Dot-separated path to the permission (e.g., "books.borrow_book").

    Returns:
        bool: True if the role has permission, False otherwise.
    """
    permissions = user_permissions.get(role, {})
    keys = action_path.split(".")
    for key in keys:
        if not isinstance(permissions, dict):
            return False
        permissions = permissions.get(key, None)
        if permissions is None:
            return False
    return bool(permissions)


class UserAuthorisation:
    """This class handles user authorisation, including login, logout, and permission checks.
    Authorised user can perform actions based on their role and associated permissions. User must be logged in to perform any action.
    This class logs user in and out, and checks if the logged-in user has permission to perform specific actions.
    """

    def __init__(self, user):
        self.logged_in_user = None
        self.user = user

    def login(self, user: User):
        self.logged_in_user = user

    def logout(self):
        self.logged_in_user = None

    def check_permission(self, action):
        if not self.logged_in_user:
            raise exc.PermissionError("No logged in user.")
        if not has_permission(self.logged_in_user.role, action):
            raise exc.PermissionError(
                f"User: {self.logged_in_user.role} cannot perform action '{action}'"
            )

        return True
