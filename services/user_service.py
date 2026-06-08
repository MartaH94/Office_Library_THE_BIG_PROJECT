"""
________________________________________________________________________
services.user_service.py
========================================================================
Managing users operations e.g.: add, edit, search, sort, delete, display
________________________________________________________________________

file status: in progress


NOW BUILDING SERVICES IN FOLLOWING ORDER:

1. UserService
2. BookService
3. LoanService



METHODS TO IMPLEMENT IN CLASS UserService:

# SEARCH / RETRIEVE:
get_user_by_username(user_name: str)
get_user_by_email(email: str)
get_user_by_id(user_id: int)

# EXISTENCE CHECKS:
user_exists_by_username(user_name: str) -> bool
user_exists_by_email(email: str) -> bool
validate_user_exists(user_id: int)

# CORE UPDATE:
update_user_data(user_id, field, value)
update_user_role(user_id, role)
update_user_status(user_id, is_active)
update_last_login(user_id)

# DELETE:
delete_user(user_id)

# HELPERS:
get_user_role(user_id)
is_user_active(user_id)
get_user_profile(user_id)

"""

import exceptions as exc
from models.user import User
from database.user_json_file_service import UsersJsonFileService
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

    def get_all_users(self):
        """This method retrieves all user records from the JSON file storage using the UsersJsonFileService. It returns a list of user dictionaries representing all users in the system."""

        return self.users_json_service.get_all_users_list()

    def get_user_by_id(self, user_id):
        """This method retrieves a user by their unique user ID. It takes an integer user_id as input, validates it, and then searches through the list of all users to find a matching user ID. If a user with the specified ID is found, it returns a User object created from the user's data. If no matching user is found, it raises a UserNotFoundError.

        Args:
            user_id (int): The unique identifier of the user to be retrieved."""

        if user_id is None:
            raise exc.DataError("Please provide user ID to retrieve user data.")

        if not isinstance(user_id, int):
            raise exc.DataTypeError(
                "Please provide correct type of user ID to retrieve user data."
            )

        all_users = self.get_all_users()

        for user in all_users:
            if user_id == user.get("user_id"):
                return User(**user)

        raise exc.UserNotFoundError(f"User with ID: {user_id} not found in database.")

    def get_user_by_username(self, user_name):
        """This method retrieves a user by their username. It takes a string user_name as input, validates it, and then searches through the list of all users to find a matching username in the user_profile. If a user with the specified username is found, it returns a User object created from the user's data. If no matching user is found, it raises a UserNotFoundError.

        Args:
            user_name (str): The username of the user to be retrieved."""

        if not user_name or not user_name.strip():
            raise exc.DataError("Please provide user name to retrieve data.")

        if not isinstance(user_name, str):
            raise exc.DataTypeError(
                "Please provide correct type of user name to retrieve data."
            )

        all_users = self.get_all_users()

        user_name = user_name.strip().lower()

        for user in all_users:
            stored_user_name = user.get("user_profile", {}).get("user_name").lower()
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
