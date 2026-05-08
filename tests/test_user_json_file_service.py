"""
________________________________________________________
tests.test_user_json_file_service.py
========================================================
Test for the file user_json_file_service.py
________________________________________________________

Test classes: 5
Test cases total: 21

current status: In progress
Total number of done test cases:

"""

import json
import tempfile
import unittest
from pathlib import Path

import exceptions as exc
from database.user_json_file_service import UsersJsonFileService
from database.database_schemes import user_schema
from database.json_files_major_services import JsonFilesService


class TestUserServiceGetUserData(unittest.TestCase):  # 3/3
    """Method under test: get_user_data
    Number of TestCases: 3
    Done TestCases: 3
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.valid_user_list = [
            {
                "user_id": 112233,
                "role": "reader",
                "user_profile": {
                    "user_name": "test_user",
                    "email": "testuser@test.com",
                    "phone_number": 111222333,
                    "password_hash": "password",
                },
                "is_active": True,
            },
            {
                "user_id": 112244,
                "role": "guest",
                "user_profile": {
                    "user_name": "test_librarian_guest",
                    "email": "testuser@test.com",
                    "phone_number": 111222334,
                    "password_hash": "password",
                },
                "is_active": True,
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_user_list, f)

        self.major_json_service = JsonFilesService(file_path=self.test_json_file_path)

        self.user_service = UsersJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_user_id_is_none(self):
        """expected behavior: raises ValidationError when user_id is None"""
        with self.assertRaises(exc.ValidationError) as cm:
            self.user_service.get_user_data(None)

        self.assertIn("User ID is missing", str(cm.exception))

    def test_returns_user_data_when_id_exists(self):
        """expected behavior: returns user data dict when user_id exists in database"""
        expected_user_data = self.valid_user_list[0]
        test_result = self.user_service.get_user_data(112233)
        self.assertEqual(test_result, expected_user_data)

    def test_raises_user_not_found_error_when_user_id_not_found(self):
        """expected behavior: raises UserNotFoundError when user_id does not exist in database"""
        with self.assertRaises(exc.UserNotFoundError) as cm:
            self.user_service.get_user_data(101010)

        self.assertIn("does not exist in database", str(cm.exception))


class TestUserServiceAddUserData(unittest.TestCase):  # 5/5
    """Method under test: add_user_data
    Number of TestCases: 5
    Done TestCases: 5
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.valid_user_list = [
            {
                "user_id": 112233,
                "role": "reader",
                "user_profile": {
                    "user_name": "test_user",
                    "email": "testuser@test.com",
                    "phone_number": 111222333,
                    "password_hash": "password",
                },
                "is_active": True,
            },
            {
                "user_id": 112244,
                "role": "librarian",
                "user_profile": {
                    "user_name": "test_librarian",
                    "email": "testuser@test.com",
                    "phone_number": 111222334,
                    "password_hash": "password",
                },
                "is_active": True,
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_user_list, f)

        self.major_json_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=user_schema
        )

        self.user_service = UsersJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_user_data_is_missing(self):
        """expected behavior: raises ValidationError when user_data is missing or it's an empty value"""
        with self.assertRaises(exc.ValidationError) as cm:
            self.user_service.add_user_data(None)

        self.assertIn("User data to add is missing", str(cm.exception))

    def test_raises_data_type_error_when_user_data_is_not_dict(self):
        """expected behavior: raises DataTypeError when user_data is not a dict"""
        data_to_add = [112277, "reader", "testuser1", True]

        with self.assertRaises(exc.DataTypeError) as cm:
            self.user_service.add_user_data(data_to_add)

        self.assertIn("User data type is incorrect", str(cm.exception))

    def test_raises_user_error_when_user_id_already_exists(self):
        """expected behavior: raises UserError when user_id in user_data already exists in database"""
        data_to_add = {
            "user_id": 112233,
            "role": "reader",
            "user_profile": {
                "user_name": "test_user",
                "email": "testuser@test.com",
                "phone_number": 111222333,
                "password_hash": "password",
            },
            "is_active": True,
        }

        with self.assertRaises(exc.UserError) as cm:
            self.user_service.add_user_data(data_to_add)

        self.assertIn("User ID must be unique value", str(cm.exception))

    def test_raises_user_validation_error_when_schema_validation_raises_validation_error(
        self,
    ):
        """expected behavior: raises UserValidationError when user_data doesn't match database file schema and schema validation raises Validation Error"""
        data_to_add = {
            "user_id": 112288,
            "role": "reader",
            "user_profile": {
                "user_name": "test_user3",
                "email": "testuser3@test.com",
                "phone_number": 111222388,
                "password_hash": "password",
            },
        }

        with self.assertRaises(exc.UserValidationError) as cm:
            self.user_service.add_user_data(data_to_add)

        self.assertIn("Validation failed", str(cm.exception))

    def test_writes_json_and_returns_success_message_when_data_is_valid(self):
        """expected behavior: writes user_data to json file and returns success message when data is valid"""
        data_to_add = {
            "user_id": 112277,
            "role": "reader",
            "user_profile": {
                "user_name": "test_user4",
                "email": "testuser4@test.com",
                "phone_number": 111222345,
                "password_hash": "password",
            },
            "is_active": True,
        }

        result = self.user_service.add_user_data(data_to_add)

        self.assertIn("Added new user to database", result)

        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            self.assertIn(data_to_add, json.load(f))


class TestUserServiceGetAllUsersList(unittest.TestCase):  # 3/3
    """Method under test: get_all_users_list
    Number of TestCases: 3
    Done TestCases: 3
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.major_json_service = JsonFilesService(file_path=self.test_json_file_path)

        self.user_service = UsersJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_returns_all_users_list_for_valid_user_dicts(self):
        """expected behavior: returns list of all user dicts when valid user entries exist in database"""
        valid_user_list = [
            {
                "user_id": 112233,
                "role": "reader",
                "user_profile": {
                    "user_name": "test_user",
                    "email": "testuser@test.com",
                    "phone_number": 111222333,
                    "password_hash": "password",
                },
                "is_active": True,
            },
            {
                "user_id": 112244,
                "role": "guest",
                "user_profile": {
                    "user_name": "test_librarian_guest",
                    "email": "testuser@test.com",
                    "phone_number": 111222334,
                    "password_hash": "password",
                },
                "is_active": True,
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(valid_user_list, f)

        expected_result = valid_user_list
        test_result = self.user_service.get_all_users_list()

        self.assertEqual(test_result, expected_result)

    def test_raises_user_not_found_error_when_database_is_empty(self):
        """expected behavior: raises UserNotFoundError when no user entries exist in database"""
        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump([], f)

        with self.assertRaises(exc.UserNotFoundError) as cm:
            self.user_service.get_all_users_list()

        self.assertIn("No user found in the database", str(cm.exception))

    def test_raises_user_not_found_error_when_no_valid_user_entries_exist(self):
        """expected behavior: raises UserNotFoundError when no valid user entries exist in database"""
        invalid_user_list = ["testuser1", "testuser2", "testuser3"]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(invalid_user_list, f)

        with self.assertRaises(exc.UserNotFoundError) as cm:
            self.user_service.get_all_users_list()

        self.assertIn("No user found in the database", str(cm.exception))


class TestUserServiceUpdateUserData(unittest.TestCase):  # 0/7
    """Method under test: update_user_data
    Number of TestCases: 7
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.valid_user_list = [
            {
                "user_id": 112233,
                "role": "reader",
                "user_profile": {
                    "user_name": "test_user",
                    "email": "testuser@test.com",
                    "phone_number": 111222333,
                    "password_hash": "password",
                },
                "is_active": True,
            },
            {
                "user_id": 112244,
                "role": "guest",
                "user_profile": {
                    "user_name": "test_librarian_guest",
                    "email": "testuser@test.com",
                    "phone_number": 111222334,
                    "password_hash": "password",
                },
                "is_active": True,
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_user_list, f)

        self.major_json_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=user_schema
        )

        self.user_service = UsersJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_user_id_is_none(self):
        """expected behavior: raises ValidationError when user_id is None"""
        with self.assertRaises(exc.ValidationError) as cm:
            self.user_service.update_user_data(
                user_id=None, field="user_name", new_value="user_for_test"
            )

        self.assertIn("User ID is missing", str(cm.exception))

    def test_raises_validation_error_when_field_is_none(self):
        """expected behavior: raises ValidationError when field is None"""
        with self.assertRaises(exc.ValidationError) as cm:
            self.user_service.update_user_data(
                user_id=112233, field=None, new_value="new_value"
            )

        self.assertIn("Field value is missing", str(cm.exception))

    def test_raises_validation_error_when_new_value_is_none(self):
        """expected behavior: raises ValidationError when new_value is None"""
        with self.assertRaises(exc.ValidationError) as cm:
            self.user_service.update_user_data(
                user_id=112233, field="user_name", new_value=None
            )

        self.assertIn("New value to update data is missing", str(cm.exception))

    # def test_raises_validation_error_when_field_not_in_user(self):
    #     """expected behavior: raises ValidationError when field is not a valid user field"""
    #     with self.assertRaises(exc.ValidationError) as cm:
    #         self.user_service.update_user_data(
    #             user_id=112233, field="status", new_value="active"
    #         )

    #     self.assertIn("missing in this user entry", str(cm.exception))

    def test_raises_user_not_found_error_when_user_id_not_found(self):
        """expected behavior: raises UserNotFoundError when user_id does not exist in database"""
        with self.assertRaises(exc.UserNotFoundError) as cm:
            self.user_service.update_user_data(
                user_id=112200, field="role", new_value="librarian"
            )

        self.assertIn("not found in database", str(cm.exception))

    def test_raises_user_validation_error_when_updated_user_data_fails_schema_validation(
        self,
    ):
        """expected behavior: raises UserValidationError when updated user data fails schema validation"""
        pass

    def test_updates_user_field_and_writes_json_when_data_is_valid(self):
        """expected behavior: updates user field with new value and writes updated data to json file when data is valid"""
        pass


class TestUserServiceDeleteUserById(unittest.TestCase):  # 0/3
    """Method under test: delete_user_by_id
    Number of TestCases: 3
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.valid_user_list = [
            {
                "user_id": 112233,
                "role": "reader",
                "user_profile": {
                    "user_name": "test_user",
                    "email": "testuser@test.com",
                    "phone_number": 111222333,
                    "password_hash": "password",
                },
                "is_active": True,
            },
            {
                "user_id": 112244,
                "role": "guest",
                "user_profile": {
                    "user_name": "test_librarian_guest",
                    "email": "testuser@test.com",
                    "phone_number": 111222334,
                    "password_hash": "password",
                },
                "is_active": True,
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_user_list, f)

        self.major_json_service = JsonFilesService(file_path=self.test_json_file_path)

        self.user_service = UsersJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_user_id_is_none(self):
        """expected behavior: raises ValidationError when user_id is None"""
        pass

    def test_raises_user_not__found_error_when_user_id_not_found(self):
        """expected behavior: raises UserNotFoundError when user_id does not exist in database"""
        pass

    def test_removes_user_and_writes_json_when_user_id_exists(self):
        """expected behavior: removes user entry from database and writes updated data to json file when user_id exists in database"""
        pass


if __name__ == "__main__":
    unittest.main(verbosity=0)
