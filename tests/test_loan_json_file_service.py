"""
________________________________________________________
tests.test_loan_json_file_service.py
========================================================
Test for the file loan_json_file_service.py
________________________________________________________

Test classes: 5
Test cases total: 21

current status: not started
Total number of done test cases:
"""

import json
import tempfile
import unittest
from pathlib import Path

import exceptions as exc
from database.json_files_major_services import JsonFilesService
from database.loan_json_file_service import LoanJsonFileService


class TestLoanJsonFileServiceGetLoanData(unittest.TestCase):  # 0/3
    """Method under test: get_loan_data
    Number of TestCases: 3
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_loan_id_is_none(self):
        pass

    def test_returns_loan_when_loan_id_exists(self):
        pass

    def test_raises_loan_not_found_error_when_loan_id_not_found(self):
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

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_loan_data_is_missing(self):
        pass

    def test_raises_data_type_error_when_loan_data_is_not_dict(self):
        pass

    def test_raises_loan_error_when_loan_id_already_exists(self):
        pass

    def test_raises_loan_validation_error_when_schema_validation_raises_validation_error(
        self,
    ):
        pass

    def test_writes_json_and_returns_success_message_when_data_is_valid(self):
        pass


class TestLoanJsonFileServiceGetAllLoansList(unittest.TestCase):  # 0/3
    """Method under test: get_all_loans_list
    Number of TestCases: 3
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_returns_all_loans_valid_loan_dicts_as_list(self):
        pass

    def test_raises_loan_not_found_error_when_database_is_empty(self):
        pass

    def test_raises_loan_not_found_error_when_no_valid_loan_entries_exist(self):
        pass


class TestLoanJsonFileServiceUpdateLoanData(unittest.TestCase):  # 0/7
    """Method under test: update_loan_data
    Number of TestCases: 7
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_loan_id_is_none(self):
        pass

    def test_raises_validation_error_when_field_is_none(self):
        pass

    def test_raises_validation_error_when_new_value_is_none(self):
        pass

    def test_raises_validation_error_when_field_not_in_loan(self):
        pass

    def test_raises_loan_not_found_error_when_loan_id_not_found(self):
        pass

    def test_raises_book_validation_error_when_updated_loan_data_fails_schema_validation(
        self,
    ):
        pass

    def test_updates_loan_field_and_writes_json_when_data_is_valid(self):
        pass


class TestLoanJsonFileServiceDeleteLoanDataFromFile(unittest.TestCase):  # 0/3
    """Method under test: delete_loan_data
    Number of TestCases: 3
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_loan_id_is_none(self):
        pass

    def test_raises_loan_not_found_error_when_loan_id_not_found(self):
        pass

    def test_removes_loan_and_writes_file_when_loan_id_exists(self):
        pass
