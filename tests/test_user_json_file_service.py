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


class TestUserServiceGetUserData(unittest.TestCase):  # 0/3
    """Method under test: get_user_data
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
        pass

    def test_returns_user_data_when_id_exists(self):
        pass

    def test_raises_user_not_found_error_when_user_id_not_found(self):
        pass


class TestUserServiceAddUserData(unittest.TestCase):  # 0/5
    """Method under test: add_user_data
    Number of TestCases: 5
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

    def test_raises_validation_error_when_user_data_is_missing(self):
        pass

    def test_raises_data_type_error_when_user_data_is_not_dict(self):
        pass

    def test_raises_user_error_when_user_id_already_exists(self):
        pass

    def test_raises_user_validation_error_when_schema_validation_raises_validation_error(
        self,
    ):
        pass

    def test_writes_json_and_returns_success_message_when_data_is_valid(self):
        pass


class TestUserServiceGetAllUsersList(unittest.TestCase):  # 0/3
    """Method under test: get_all_users_list
    Number of TestCases: 3
    Done TestCases:
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

    def test_raises_user_not_found_error_when_database_is_empty(self):
        pass

    def test_raises_user_not_found_error_when_no_valid_user_entries_exist(self):
        pass


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
        pass

    def test_raises_validation_error_when_field_is_none(self):
        pass

    def test_raises_validation_error_when_new_value_is_none(self):
        pass

    def test_raises_validation_error_when_field_not_in_user(self):
        pass

    def test_raises_user_not_found_error_when_user_id_not_found(self):
        pass

    def test_raises_user_validation_error_when_updated_user_data_fails_schema_validation(
        self,
    ):
        pass

    def test_updates_user_field_and_writes_json_when_data_is_valid(self):
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
        pass

    def test_raises_user_not__found_error_when_user_id_not_found(self):
        pass

    def test_removes_user_and_writes_json_when_user_id_exists(self):
        pass
