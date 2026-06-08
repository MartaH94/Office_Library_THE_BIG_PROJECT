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


class UserService:
    def __init__(self, users_json_service: UsersJsonFileService):
        self.users_json_service = users_json_service

    def add_user(self, user: User):
        user_dict = user.__dict__
        self.users_json_service.add_user_data(user_dict)

    def get_all_users(self):
        return self.users_json_service.get_all_users_list()

    def get_user_by_id(self, user_id):

        if user_id is None:
            raise exc.UserError("Please provide user ID to retrieve user data.")

        if not isinstance(user_id, int):
            raise exc.UserError(
                "Please provide correct type of user ID to retrieve user data."
            )

        all_users = self.get_all_users()

        for user in all_users:
            if user_id == user.get("user_id"):
                return User(**user)

        raise exc.UserNotFoundError(f"User with ID: {user_id} not found in database.")
