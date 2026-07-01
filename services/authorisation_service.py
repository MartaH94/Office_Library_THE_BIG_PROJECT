"""
________________________________________________________
services.authorisation_service
========================================================
Service for managing user authorisation.
________________________________________________________

This module defines the `UserAuthorisation` class for handling user login, logout, and permission checks based on user roles. It also includes functions for user registration and login, which interact with the `UsersJsonFileService` to manage user data stored in a JSON file. The module uses a predefined permissions structure to determine what actions each role is allowed to perform within the library management system.


!!! Update and verification of registration and logging functios
 as the users, books and loans services are growing !!!

"""

from datetime import datetime

import exceptions as exc
from database.user_json_file_service import UsersJsonFileService
from models.user import User
from services.user_service import UserService
from utils.helpers import generate_user_id, validate_email
from utils.security_helpers import (
    hash_password,
    validate_password_strength,
    verify_password,
)

# managing registration, login, permissions and authorisation of users

user_permissions = {
    "reader": {
        "books": {
            "borrow_book": True,
            "return_book": True,
            "reserve_book": True,
            "cancel_reservation": True,
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
            "view_reservations": False,
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
            "cancel_reservation": True,
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
            "view_reservations": True,
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
            "cancel_reservation": True,
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
            "view_reservations": True,
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
            "reserve_book": False,
            "cancel_reservation": False,
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
            "view_reservations": False,
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
            "cancel_reservation": True,
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
            "view_reservations": True,
            "manage_users": False,
            "view_logs": True,
            "generate_reports": True,
            "delegate_permissions": False,
            "delete_data": False,
            "edit_data": True,
        },
        "sensitive_users_data": {
            "view_data": True,
            "edit_data": False,
            "delete_data": False,
        },
    },
}


def user_registration(
    user_service: UserService,
    user_name: str,
    email: str,
    password: str,
):
    """This function handles user registration.

    Args:
        user_name (str): Unique username for the user, which will be used for login
        email (str): User's email address.
        password (str): User's password, which will be hashed and stored securely.
    """

    if not user_name or not user_name.strip():
        raise exc.ValidationError("Please provide a username for registration.")

    if not email:
        raise exc.ValidationError("Please provide an email address for registration.")

    if not password:
        raise exc.ValidationError("Please provide a password for registration.")

    validate_email(email)
    validate_password_strength(password)

    try:
        all_users = user_service.get_all_users()
    except exc.UserNotFoundError:
        all_users = []

    email = email.strip().lower()
    user_name = user_name.strip().lower()

    for user in all_users:
        stored_username = user.get("user_profile", {}).get("user_name").lower()

        if stored_username == user_name:
            raise exc.UserError(
                f"Username: {user_name} already exists. Please choose a different username."
            )

        stored_email = user.get("user_profile", {}).get("email").lower()

        if stored_email == email:
            raise exc.DataError(
                f"User with email: {email} is already registered. Please use a different email address."
            )
    user_id = generate_user_id(all_users)

    password_hash = hash_password(password)
    new_user = User(
        user_id=user_id,
        role="reader",
        is_active=True,
        last_login=None,
        user_profile={
            "user_name": user_name,
            "email": email,
            "password_hash": password_hash,
        },
    )

    user_service.add_user(new_user)

    return f"Dear {user_name}! Welcome in Library. Your account has been successfully created with user ID: {user_id}."


def user_login(user_service: UsersJsonFileService, user_name, password):
    """This funtion handles user login. It checks if the provided username and password are correct, and if so, it logs the user in and updates their last login date.

    Args:
        user_name (str): The username provided by the user for login.
        password (str): The password provided by the user for login.

    Returns:
        User: The logged-in user object."""

    if not user_name or not user_name.strip():
        raise exc.UserError("Please provide your username to login.")

    if not password or not password.strip():
        raise exc.UserError("Please provide your password to login.")

    try:
        all_users = user_service.get_all_users_list()
    except exc.UserNotFoundError:
        raise exc.UserError("No users are registered.")

    user_found = False

    user_name = user_name.strip().lower()

    for user in all_users:
        stored_username = user.get("user_profile", {}).get("user_name", "").lower()
        if stored_username == user_name:
            user_found = True
            break

    if not user_found:
        raise exc.UserNotFoundError(f"No user with username '{user_name}' found.")

    stored_hashed_password = user.get("user_profile", {}).get("password_hash")

    verified_password = verify_password(password, stored_hashed_password)

    if not verified_password:
        raise exc.SecurityError("Provided password is invalid.")

    user_id = user.get("user_id")

    now = datetime.now().date().isoformat()

    user_service.update_user_data(user_id=user_id, field="last_login", new_value=now)

    logged_user = User(**user)

    return logged_user


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
    return permissions is True


class UserAuthorisation:
    """This class handles user authorisation, including login, logout, and permission checks.
    Authorised user can perform actions based on their role and associated permissions. User must be logged in to perform any action.
    This class logs user in and out, and checks if the logged-in user has permission to perform specific actions.
    """

    def __init__(self):
        self.logged_in_user = None

    def login(self, user: User):
        self.logged_in_user = user

    def logout(self):
        self.logged_in_user = None

    def check_permission(self, action):
        """This method checks the permission of the user. If user us not logged in, it sets the user role to 'guest'. Then the method checks if the user with its role has permission to perform the action. If not, it raises a PermissionError. If the user has permission, it returns True."""

        role = self.logged_in_user.role if self.logged_in_user else "guest"

        if not has_permission(role, action):
            raise exc.PermissionError(
                f"User with role: {role} cannot perform action '{action}'"
            )

        return True

    def get_current_user(self):
        """This method returns the currently logged-in user. If no user is logged in, it returns None."""
        return self.logged_in_user
