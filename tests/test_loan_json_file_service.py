"""
________________________________________________________
tests.test_loan_json_file_service.py
========================================================
Test for the file loan_json_file_service.py
________________________________________________________

Test classes: 5
Test cases total: 21

current status: in progress
Total number of done test cases:
"""

import json
import tempfile
import unittest
from pathlib import Path

import exceptions as exc
from database.json_files_major_services import JsonFilesService
from database.database_schemes import loan_schema
from database.loan_json_file_service import LoanJsonFileService


class TestLoanJsonFileServiceGetLoanData(unittest.TestCase):  # 0/3
    """Method under test: get_loan_data
    Number of TestCases: 3
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.valid_loan_list = [
            {
                "loan_id": 9001,
                "user_id": 112233,
                "book_id": 1001,
                "loan_date": "2026-05-05",
            },
            {
                "loan_id": 9002,
                "user_id": 112244,
                "book_id": 1002,
                "loan_date": "2026-04-05",
            },
            {
                "loan_id": 9003,
                "user_id": 112255,
                "book_id": 1003,
                "loan_date": "2025-05-15",
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_loan_list, f)

        self.major_json_service = JsonFilesService(file_path=self.test_json_file_path)
        self.loan_service = LoanJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_loan_id_is_none(self):
        """excpected behavior: ValidationError is raised when loan_id is None or empty value"""
        pass

    def test_returns_loan_when_loan_id_exists(self):
        """excpected behavior: The matching loan record is returned when loan_id exists in the database"""
        pass

    def test_raises_loan_not_found_error_when_loan_id_not_found(self):
        """excpected behavior: LoanNotFoundError is raised when loan_id does not exist in the database"""
        pass


class TestLoanJsonFileServiceAddLoanData(unittest.TestCase):  # 0/5
    """Method under test: add_loan_data
    Number of TestCases: 5
    Done TestCases:

    Reminder for later implementation:
    - Use only required fields in valid loan data
    - Use valid "YYYY-MM-DD" strings for dates
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.valid_loan_list = [
            {
                "loan_id": 9001,
                "user_id": 112233,
                "book_id": 1001,
                "loan_date": "2026-05-05",
            },
            {
                "loan_id": 9002,
                "user_id": 112244,
                "book_id": 1002,
                "loan_date": "2026-04-05",
            },
            {
                "loan_id": 9003,
                "user_id": 112255,
                "book_id": 1003,
                "loan_date": "2025-05-15",
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_loan_list, f)

        self.major_json_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=loan_schema
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_loan_data_is_missing(self):
        """excpected behavior: ValidationError is raised when loan_data is missing or empty value"""
        pass

    def test_raises_data_type_error_when_loan_data_is_not_dict(self):
        """excpected behavior: DataTypeError is raised when loan_data is not a dict type"""
        pass

    def test_raises_loan_error_when_loan_id_already_exists(self):
        """excpected behavior: LoanError is raised when loan_id in loan data already exists in the database"""
        pass

    def test_raises_loan_validation_error_when_schema_validation_raises_validation_error(
        self,
    ):
        """excpected behavior: LoanValidationError is raised when loan_data fails schema validation"""
        pass

    def test_writes_json_and_returns_success_message_when_data_is_valid(self):
        """excpected behavior: When loan_data is valid, it is added to the database and a success message is returned"""
        pass


class TestLoanJsonFileServiceGetAllLoansList(unittest.TestCase):  # 0/3
    """Method under test: get_all_loans_list
    Number of TestCases: 3
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.major_json_service = JsonFilesService(file_path=self.test_json_file_path)
        self.loan_service = LoanJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_returns_all_loans_valid_loan_dicts_as_list(self):
        """excpected behavior: A list of all loan records is returned when the database contains valid loan entries"""
        pass

    def test_raises_loan_not_found_error_when_database_is_empty(self):
        """excpected behavior: LoanNotFoundError is raised when the database is empty and contains no loan records"""
        pass

    def test_raises_loan_not_found_error_when_no_valid_loan_entries_exist(self):
        """excpected behavior: LoanNotFoundError is raised when the database contains entries but no valid loan records exist"""
        pass


class TestLoanJsonFileServiceUpdateLoanData(unittest.TestCase):  # 0/7
    """Method under test: update_loan_data
    Number of TestCases: 7
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.valid_loan_list = [
            {
                "loan_id": 9001,
                "user_id": 112233,
                "book_id": 1001,
                "loan_date": "2026-05-05",
            },
            {
                "loan_id": 9002,
                "user_id": 112244,
                "book_id": 1002,
                "loan_date": "2026-04-05",
            },
            {
                "loan_id": 9003,
                "user_id": 112255,
                "book_id": 1003,
                "loan_date": "2025-05-15",
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_loan_list, f)

        self.major_json_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=loan_schema
        )

        self.loan_service = LoanJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_loan_id_is_none(self):
        """excpected behavior: ValidationError is raised when loan_id is None or empty value"""
        pass

    def test_raises_validation_error_when_field_is_none(self):
        """excpected behavior: ValidationError is raised when field name is None or empty value"""
        pass

    def test_raises_validation_error_when_new_value_is_none(self):
        """excpected behavior: ValidationError is raised when new value is None or empty value"""
        pass

    def test_raises_validation_error_when_field_not_in_loan(self):
        """excpected behavior: ValidationError is raised when the field to update is not a valid field in the loan record"""
        pass

    def test_raises_loan_not_found_error_when_loan_id_not_found(self):
        """excpected behavior: LoanNotFoundError is raised when loan_id does not exist in the database"""
        pass

    def test_raises_book_validation_error_when_updated_loan_data_fails_schema_validation(
        self,
    ):
        """excpected behavior: LoanValidationError is raised when the updated loan record fails schema validation after the field value is updated"""
        pass

    def test_updates_loan_field_and_writes_json_when_data_is_valid(self):
        """excpected behavior: When the updated field value is valid and the updated loan record passes schema validation, the loan data is updated in the database and a success message is returned"""
        pass


class TestLoanJsonFileServiceDeleteLoanDataFromFile(unittest.TestCase):  # 0/3
    """Method under test: delete_loan_data
    Number of TestCases: 3
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.valid_loan_list = [
            {
                "loan_id": 9001,
                "user_id": 112233,
                "book_id": 1001,
                "loan_date": "2026-05-05",
            },
            {
                "loan_id": 9002,
                "user_id": 112244,
                "book_id": 1002,
                "loan_date": "2026-04-05",
            },
            {
                "loan_id": 9003,
                "user_id": 112255,
                "book_id": 1003,
                "loan_date": "2025-05-15",
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_loan_list, f)

        self.major_json_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=loan_schema
        )

        self.loan_service = LoanJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_loan_id_is_none(self):
        """excpected behavior: ValidationError is raised when loan_id is None or empty value"""
        pass

    def test_raises_loan_not_found_error_when_loan_id_not_found(self):
        """excpected behavior: LoanNotFoundError is raised when loan_id does not exist in the database"""
        pass

    def test_removes_loan_and_writes_file_when_loan_id_exists(self):
        """excpected behavior: When loan_id exists in the database, the matching loan record is removed and the updated data is written to the JSON file"""
        pass
