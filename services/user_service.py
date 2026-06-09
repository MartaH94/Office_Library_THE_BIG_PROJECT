"""
________________________________________________________________________
services.user_service.py
========================================================================
Managing users operations
________________________________________________________________________

This module defines the UserService class, which provides methods for managing user-related operations in the library management system. The UserService interacts with the UsersJsonFileService to perform CRUD operations on user data stored in a JSON file. It includes methods for adding users, retrieving users by various criteria, updating user information, and validating user existence. The service ensures that user data is handled correctly and that appropriate exceptions are raised for invalid operations or data.


file status: done

"""

from datetime import datetime

import exceptions as exc
from database.user_json_file_service import UsersJsonFileService
from models.user import User, valid_roles
from utils.helpers import validate_email


class UserService:
    """
    The UserService class provides methods for managing user-related operations in the library management system. It interacts with the UsersJsonFileService to perform CRUD operations on user data stored in a JSON file. The service includes methods for adding users, retrieving users by various criteria, updating user information, and validating user existence.

    Attributes:
        users_json_service (UsersJsonFileService): An instance of the UsersJsonFileService for interacting with the user data storage.
    """

    def __init__(self, users_json_service: UsersJsonFileService):
        self.users_json_service = users_json_service

    def add_user(self, user: User):
        """This method allows adding a new user to the system. It takes a User object as input, converts it to a dictionary, and then uses the UsersJsonFileService to add the user data to the JSON file storage.

        Args:
            user (User): An instance of the User class containing the user's information to be added to the system.
        """

        user_dict = user.__dict__
        self.users_json_service.add_user_data(user_dict)

    ### SEARCH / RETRIEVE USER:

    def get_all_users(self):
        """This method retrieves all user records from the JSON file storage using the UsersJsonFileService. It returns a list of user dictionaries representing all users in the system."""

        return self.users_json_service.get_all_users_list()

    def get_user_by_id(self, user_id):
        """This method retrieves a user by their unique user ID. It takes an integer user_id as input, validates it, and then searches through the list of all users to find a matching user ID. If a user with the specified ID is found, it returns a User object created from the user's data. If no matching user is found, it raises a UserNotFoundError.

        Args:
            user_id (int): The unique identifier of the user to be retrieved."""

        if not isinstance(user_id, int):
            raise exc.DataTypeError(
                "Please provide correct type of user ID to retrieve user data."
            )

        if user_id is None:
            raise exc.DataError("Please provide user ID to retrieve user data.")

        all_users = self.get_all_users()

        for user in all_users:
            if user_id == user.get("user_id"):
                return User(**user)

        raise exc.UserNotFoundError(f"User with ID: {user_id} not found in database.")

    def get_user_by_username(self, user_name):
        """This method retrieves a user by their username. It takes a string user_name as input, validates it, and then searches through the list of all users to find a matching username in the user_profile. If a user with the specified username is found, it returns a User object created from the user's data. If no matching user is found, it raises a UserNotFoundError.

        Args:
            user_name (str): The username of the user to be retrieved."""

        if not isinstance(user_name, str):
            raise exc.DataTypeError(
                "Please provide correct type of user name to retrieve data."
            )

        if not user_name or not user_name.strip():
            raise exc.DataError("Please provide user name to retrieve data.")

        all_users = self.get_all_users()

        user_name = user_name.strip().lower()

        for user in all_users:
            stored_user_name = user.get("user_profile", {}).get("user_name", "").lower()
            if user_name == stored_user_name:
                return User(**user)

        raise exc.UserNotFoundError(
            f"User with name: {user_name} not found in database."
        )

    def get_user_by_email(self, email):
        """This method retrieves a user by their email address. It takes a string email as input, validates it using the validate_email function, and then searches through the list of all users to find a matching email in the user_profile. If a user with the specified email is found, it returns a User object created from the user's data. If no matching user is found, it raises a UserNotFoundError.

        Args:
            email (str): The email address of the user to be retrieved."""

        if not isinstance(email, str):
            raise exc.DataTypeError("Please provide correct type of email address.")

        if not email or not email.strip():
            raise exc.DataError("Please provide email address to retrieve data.")

        validate_email(email)
        email = email.strip().lower()

        all_users = self.get_all_users()

        for user in all_users:
            stored_email = user.get("user_profile", {}).get("email", "").lower()
            if email == stored_email:
                return User(**user)

        raise exc.UserNotFoundError(f"User with email: {email} not found in database.")

    ### USER EXISTENCE CHECKS:

    def user_exists_by_username(self, user_name):
        """This method checks if a user exists in the system based on their username. It takes a string user_name as input and returns a boolean value indicating whether a user with the specified username exists in the database. The method uses the get_user_by_username method to attempt to retrieve the user, and if a UserNotFoundError is raised, it returns False; otherwise, it returns True.

        Args:
            user_name (str): The username to check for existence in the system."""

        try:
            self.get_user_by_username(user_name)
            return True
        except exc.UserNotFoundError:
            return False

    def user_exists_by_email(self, email):
        """This method checks if a user exists in the system based on their email address. It takes a string email as input and returns a boolean value indicating whether a user with the specified email exists in the database. The method uses the get_user_by_email method to attempt to retrieve the user, and if a UserNotFoundError is raised, it returns False; otherwise, it returns True.

        Args:
            email (str): The email address to check for existence in the system."""

        try:
            self.get_user_by_email(email)
            return True
        except exc.UserNotFoundError:
            return False

    def ensure_user_exists(self, user_id):
        """This method ensures that a user with the specified user ID exists in the system. It takes an integer user_id as input and attempts to retrieve the user using the get_user_by_id method. If the user is found, it returns the User object; if no user with the specified ID exists, it raises a UserNotFoundError."""

        self.get_user_by_id(user_id)

    ### USER DATA UPDATES:

    def update_user_data(self, user_id, field, new_value):
        """This method updates a specific field of a user's data based on their user ID. It takes an integer user_id, a string field representing the field to be updated, and the new value to be set for that field. The method first ensures that the user exists using the ensure_user_exists method, then validates the input parameters, and finally uses the UsersJsonFileService to perform the update in the JSON file storage. If the update is successful, it returns the updated user data."""

        self.ensure_user_exists(user_id)

        if not isinstance(field, str):
            raise exc.DataTypeError("Field name must be a string value type.")

        if not field or not field.strip():
            raise exc.ValidationError("Selected field to update is an empty value.")

        if new_value is None:
            raise exc.ValidationError("New value to update cannot be an empty value.")

        updated_user_data = self.users_json_service.update_user_data(
            user_id=user_id, field=field, new_value=new_value
        )

        return updated_user_data

    def update_user_role(self, user_id, new_role):
        """This method updates the role of a user based on their user ID. It takes an integer user_id and a string new_role as input. The method first ensures that the user exists using the ensure_user_exists method, then validates that the new_role is one of the valid roles defined in the system. If the new_role is valid, it uses the UsersJsonFileService to update the user's role in the JSON file storage. If the update is successful, it returns the updated user data."""

        self.ensure_user_exists(user_id)

        if new_role not in valid_roles:
            raise exc.UserValidationError(f"{new_role}: The role is not available.")

        user_data_with_updated_role = self.users_json_service.update_user_data(
            user_id=user_id, field="role", new_value=new_role
        )

        return user_data_with_updated_role

    def update_user_status(self, user_id, new_status):
        """This method updates the active status of a user based on their user ID. It takes an integer user_id and a boolean new_status as input. The method first ensures that the user exists using the ensure_user_exists method, then validates that the new_status is a boolean value. If the new_status is valid, it uses the UsersJsonFileService to update the user's active status in the JSON file storage. If the update is successful, it returns the updated user data."""

        self.ensure_user_exists(user_id)

        if not isinstance(new_status, bool):
            raise exc.DataTypeError("The field 'is_active' must be a bool value.")

        user_data_with_updated_status = self.users_json_service.update_user_data(
            user_id=user_id, field="is_active", new_value=new_status
        )

        return user_data_with_updated_status

    def update_last_login_date(self, user_id):
        """This method updates the last login date of a user based on their user ID. It takes an integer user_id as input. The method first ensures that the user exists using the ensure_user_exists method, then gets the current date and formats it as an ISO string. It uses the UsersJsonFileService to update the user's last login date in the JSON file storage. If the update is successful, it returns the updated user data."""

        self.ensure_user_exists(user_id)

        now = datetime.now().date().isoformat()

        user_data_with_updated_login_date = self.users_json_service.update_user_data(
            user_id=user_id, field="last_login", new_value=now
        )

        return user_data_with_updated_login_date

    ### UTILS:

    def delete_user(self, user_id):
        """This method deletes a user from the system based on their user ID. It takes an integer user_id as input, ensures that the user exists using the ensure_user_exists method, and then uses the UsersJsonFileService to delete the user data from the JSON file storage. If the deletion is successful, it returns a confirmation message or the deleted user data."""

        self.ensure_user_exists(user_id)

        return self.users_json_service.delete_user_by_id(user_id)

    ### HELPERS:

    def get_user_role(self, user_id):
        """This method retrieves the role of a user based on their user ID. It takes an integer user_id as input, ensures that the user exists using the ensure_user_exists method, and then retrieves the user's data to return the role associated with that user."""

        user = self.get_user_by_id(user_id)

        return user.role

    def is_user_active(self, user_id):
        """This method checks if a user is active based on their user ID. It takes an integer user_id as input, ensures that the user exists using the ensure_user_exists method, and then retrieves the user's data to return the active status (is_active) associated with that user."""

        user = self.get_user_by_id(user_id)

        return user.is_active

    def get_user_profile(self, user_id):
        """This method retrieves the user profile information of a user based on their user ID. It takes an integer user_id as input, ensures that the user exists using the ensure_user_exists method, and then retrieves the user's data to return the user_profile dictionary associated with that user."""

        user = self.get_user_by_id(user_id)

        return user.user_profile
