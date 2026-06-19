"""
________________________________________________________
tests.test_loan_json_file_service.py
========================================================
Test for the file loan_json_file_service.py
________________________________________________________

Test classes: 5 -->
Test cases total: 21 -->

current status: Done --> Update
Total number of done test cases: 21 -->

FILE UPDATE
Needed implementation of unit test for reservation methods

"""

import json
import tempfile
import unittest
from pathlib import Path

import exceptions as exc
from database.database_schemes import loan_schema
from database.json_files_major_services import JsonFilesService
from database.loan_json_file_service import LoanJsonFileService


class TestLoanJsonFileServiceGetLoanData(unittest.TestCase):  # 3/3
    """Method under test: get_loan_data
    Number of TestCases: 3
    Done TestCases: 3
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
        with self.assertRaises(exc.ValidationError) as cm:
            self.loan_service.get_loan_data(loan_id=None)

        self.assertIn("Loan ID is missing", str(cm.exception))

    def test_returns_loan_when_loan_id_exists(self):
        """excpected behavior: The matching loan record is returned when loan_id exists in the database"""
        expected_result = self.valid_loan_list[0]
        test_result = self.loan_service.get_loan_data(9001)
        self.assertEqual(test_result, expected_result)

    def test_raises_loan_not_found_error_when_loan_id_not_found(self):
        """excpected behavior: LoanNotFoundError is raised when loan_id does not exist in the database"""
        with self.assertRaises(exc.LoanNotFoundError) as cm:
            self.loan_service.get_loan_data(9874)

        self.assertIn("does not exists in database", str(cm.exception))


class TestLoanJsonFileServiceAddLoanData(unittest.TestCase):  # 5/5
    """Method under test: add_loan_data
    Number of TestCases: 5
    Done TestCases: 5

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

        self.loan_service = LoanJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_loan_data_is_missing(self):
        """excpected behavior: ValidationError is raised when loan_data is missing or empty value"""
        with self.assertRaises(exc.ValidationError) as cm:
            self.loan_service.add_loan_data(None)

        self.assertIn("Loan data to save is missing", str(cm.exception))

    def test_raises_data_type_error_when_loan_data_is_not_dict(self):
        """excpected behavior: DataTypeError is raised when loan_data is not a dict type"""
        data_to_add = [9010, 112298, 1033, "2026-05-07"]

        with self.assertRaises(exc.DataTypeError) as cm:
            self.loan_service.add_loan_data(data_to_add)

        self.assertIn("data type is incorrect", str(cm.exception))

    def test_raises_loan_error_when_loan_id_already_exists(self):
        """excpected behavior: LoanError is raised when loan_id in loan data already exists in the database"""
        data_to_add = {
            "loan_id": 9003,
            "user_id": 112256,
            "book_id": 1004,
            "loan_date": "2025-01-15",
        }

        with self.assertRaises(exc.LoanError) as cm:
            self.loan_service.add_loan_data(data_to_add)

        self.assertIn("ID number must be unique value", str(cm.exception))

    def test_raises_loan_validation_error_when_schema_validation_raises_validation_error(
        self,
    ):
        """excpected behavior: LoanValidationError is raised when loan_data fails schema validation"""
        data_to_append = {"loan_id": 9003, "user_id": 112256, "book_id": 1004}

        with self.assertRaises(exc.LoanValidationError) as cm:
            self.loan_service.add_loan_data(data_to_append)

        self.assertIn("Loan data doesn't match database file schema", str(cm.exception))

    def test_writes_json_and_returns_success_message_when_data_is_valid(self):
        """excpected behavior: When loan_data is valid, it is added to the database and a success message is returned"""
        data_to_add = {
            "loan_id": 9006,
            "user_id": 112256,
            "book_id": 1004,
            "loan_date": "2025-01-15",
        }

        result = self.loan_service.add_loan_data(data_to_add)

        self.assertIn("Added new loan to data base", result)

        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            self.assertIn(data_to_add, json.load(f))


class TestLoanJsonFileServiceGetAllLoansList(unittest.TestCase):  # 3/3
    """Method under test: get_all_loans_list
    Number of TestCases: 3
    Done TestCases: 3
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

        expected_result = self.valid_loan_list
        test_result = self.loan_service.get_all_loans_list()

        self.assertEqual(test_result, expected_result)

    def test_raises_loan_not_found_error_when_database_is_empty(self):
        """excpected behavior: LoanNotFoundError is raised when the database is empty and contains no loan records"""
        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump([], f)

        with self.assertRaises(exc.LoanNotFoundError) as cm:
            self.loan_service.get_all_loans_list()

        self.assertIn("No loan found", str(cm.exception))

    def test_raises_loan_not_found_error_when_no_valid_loan_entries_exist(self):
        """excpected behavior: LoanNotFoundError is raised when the database contains entries but no valid loan records exist"""
        invalid_loan_list = [9008, 112277, 1001, "2025-01-01"]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(invalid_loan_list, f)

        with self.assertRaises(exc.LoanNotFoundError) as cm:
            self.loan_service.get_all_loans_list()

        self.assertIn("No loan found", str(cm.exception))


class TestLoanJsonFileServiceUpdateLoanData(unittest.TestCase):  # 7/7
    """Method under test: update_loan_data
    Number of TestCases: 7
    Done TestCases: 7
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
        with self.assertRaises(exc.ValidationError) as cm:
            self.loan_service.update_loan_data(
                loan_id=None, field="loan_id", new_value=9874
            )

        self.assertIn("Loan ID is missing", str(cm.exception))

    def test_raises_validation_error_when_field_is_none(self):
        """excpected behavior: ValidationError is raised when field name is None or empty value"""
        with self.assertRaises(exc.ValidationError) as cm:
            self.loan_service.update_loan_data(loan_id=9001, field=None, new_value=9889)

        self.assertIn("The field value is missing", str(cm.exception))

    def test_raises_validation_error_when_new_value_is_none(self):
        """excpected behavior: ValidationError is raised when new value is None or empty value"""
        with self.assertRaises(exc.ValidationError) as cm:
            self.loan_service.update_loan_data(
                loan_id=9001, field="loan_id", new_value=None
            )

        self.assertIn("New value to update loan data is missing", str(cm.exception))

    def test_raises_validation_error_when_field_not_in_loan(self):
        """excpected behavior: ValidationError is raised when the field to update is not a valid field in the loan record"""
        with self.assertRaises(exc.ValidationError) as cm:
            self.loan_service.update_loan_data(
                loan_id=9001, field="status", new_value="reserved"
            )

        self.assertIn("missing in this loan record entry", str(cm.exception))

    def test_raises_loan_not_found_error_when_loan_id_not_found(self):
        """excpected behavior: LoanNotFoundError is raised when loan_id does not exist in the database"""
        with self.assertRaises(exc.LoanNotFoundError) as cm:
            self.loan_service.update_loan_data(
                loan_id=9999, field="loan_id", new_value=9633
            )

        self.assertIn("not found in database", str(cm.exception))

    def test_raises_book_validation_error_when_updated_loan_data_fails_schema_validation(
        self,
    ):
        """excpected behavior: LoanValidationError is raised when the updated loan record fails schema validation after the field value is updated"""
        with self.assertRaises(exc.LoanValidationError) as cm:
            self.loan_service.update_loan_data(
                loan_id=9001, field="loan_id", new_value="9888"
            )

        self.assertIn("Validation failed while updating loan data", str(cm.exception))

    def test_updates_loan_field_and_writes_json_when_data_is_valid(self):
        """excpected behavior: When the updated field value is valid and the updated loan record passes schema validation, the loan data is updated in the database and a success message is returned"""
        test_result = self.loan_service.update_loan_data(
            loan_id=9001, field="loan_date", new_value="2026-01-01"
        )

        self.assertIn("New data value has been saved for loan", test_result)

        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            updated_loan_data = json.load(f)

        for loan in updated_loan_data:
            if loan.get("loan_id") == 9001:
                self.assertEqual(loan.get("loan_date"), "2026-01-01")
                break


class TestLoanJsonFileServiceDeleteLoanDataFromFile(unittest.TestCase):  # 3/3
    """Method under test: delete_loan_data
    Number of TestCases: 3
    Done TestCases: 3
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
        with self.assertRaises(exc.ValidationError) as cm:
            self.loan_service.delete_loan_data_from_file(loan_id=None)

        self.assertIn("Loan ID is missing", str(cm.exception))

    def test_raises_loan_not_found_error_when_loan_id_not_found(self):
        """excpected behavior: LoanNotFoundError is raised when loan_id does not exist in the database"""
        with self.assertRaises(exc.LoanNotFoundError) as cm:
            self.loan_service.delete_loan_data_from_file(loan_id=9999)

        self.assertIn("could not be removed", str(cm.exception))

    def test_removes_loan_and_writes_file_when_loan_id_exists(self):
        """excpected behavior: When loan_id exists in the database, the matching loan record is removed and the updated data is written to the JSON file"""
        test_result = self.loan_service.delete_loan_data_from_file(loan_id=9001)

        self.assertIn("has been deleted from database", str(test_result))

        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            updated_loan_data = json.load(f)

        self.assertEqual(len(updated_loan_data), 2)

        for loan in updated_loan_data:
            self.assertNotEqual(loan.get("loan_id"), 9001)


### TESTS FOR RESERVATION METHODS


class TestLoanJsonFileServiceAddReservationData(unittest.TestCase):

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()


class TestLoanJsonFileServiceGetreservationData(unittest.TestCase):

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()


class TestLoanJsonFileServiceGetAllReservationList(unittest.TestCase):

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()


class TestLoanJsonFileServiceDeleteReservationData(unittest.TestCase):

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()


if __name__ == "__main__":
    unittest.main(verbosity=0)
