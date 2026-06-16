# class user to represent a user in te library or administrator
"""This module defines the User class for representing users in the library management system.

TO DO:
-update module docstring
- implement method to_dict() to convert data to dictionary.

"""

import exceptions as exc

valid_roles = ["reader", "admin", "librarian", "guest", "moderator"]


class User:
    def __init__(self, user_id, role, is_active, last_login, user_profile):
        self.user_id = user_id
        self.role = role
        self.is_active = is_active
        self.last_login = last_login
        self.user_profile = user_profile

        if not isinstance(user_profile, dict):
            raise exc.UserError(
                "User profile must be a dictionary containing user details."
            )

        if self.role not in valid_roles:
            raise exc.UserInvalidRole(f"The {role} is not available.")

    def __repr__(self):
        """Return a string representation of the User object for debugging purposes."""
        return f"User(user_id={self.user_id}, role='{self.role}', is_active={self.is_active}, last_login='{self.last_login}'"
