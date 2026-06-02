"""
________________________________________________________
tests.test_json_files_major_service.py
========================================================
Test for the file json_files_major_services.py
________________________________________________________

Test classes: 11
Test cases total: 59
current status: Done

"""

import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

""" from unittest.mock import patch - imports a testing utility that lets you temporarily replace objects (like functions, classes, or directory paths) during tests"""

import exceptions as exc
import utils.config as config
from database.json_files_major_services import JsonFilesService


# -------------------------
# File I/O helpers | Test cases: 11
# -------------------------
class TestJsonFileServiceFileExistsChecking(unittest.TestCase):  # 3/3
    """Method under test: file_exists_checking
    Number of TestCases: 4
    Done TestCases: 4
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

        self.path_to_non_existent_file = (
            Path(self.temporary_dir.name) / "non_existent_file.json"
        )

        self.path_to_empty_file = Path(self.temporary_dir.name) / "empty_file.json"

        self.path_to_empty_file.write_text("", encoding="utf-8")

        self.path_to_file_with_content = (
            Path(self.temporary_dir.name) / "file_with_content.json"
        )

        self.path_to_file_with_content.write_text("[]", encoding="utf-8")

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_creates_file_when_missing(self):
        """expected behavior: file_exists_checking creates a new file if it doesn't exist and initializes it with an empty list as JSON content"""
        self.json_service = JsonFilesService(file_path=self.path_to_non_existent_file)
        file_to_check = self.path_to_non_existent_file
        self.json_service.file_exists_checking()
        with open(file_to_check, encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertIsInstance(file_content, list)

    def test_initializes_list_in_empty_file(self):
        """expected behavior: file_exists_checking initializes an empty file with an empty list as JSON content"""
        self.json_service = JsonFilesService(file_path=self.path_to_empty_file)
        file_to_check = self.path_to_empty_file
        self.json_service.file_exists_checking()
        with open(file_to_check, encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertEqual(file_content, [])

    def test_no_action_when_file_has_content(self):
        """expected behavior: file_exists_checking does not modify the file if it already has content. The content of the file remains unchanged after the method is called"""
        self.json_service = JsonFilesService(file_path=self.path_to_file_with_content)
        file_to_check = self.path_to_file_with_content

        with open(file_to_check, encoding="utf-8") as f:
            before_content = json.load(f)

        self.json_service.file_exists_checking()
        with open(file_to_check, encoding="utf-8") as f:
            after_content = json.load(f)

        self.assertEqual(before_content, after_content)


class TestJsonFileServiceLoadJsonFile(unittest.TestCase):  # 4/4
    """Method under test: load_json_file
    Number of TestCases: 4
    Done TestCases: 4
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

        """ Paths to test files """
        self.valid_json_file_path = self.temporary_dir_path / "valid_file.json"
        self.invalid_json_file_path = self.temporary_dir_path / "invalid_file.json"
        self.empty_json_file_path = self.temporary_dir_path / "empty_file.json"
        self.missing_json_file_path = self.temporary_dir_path / "missing_file.json"

        """ Service under test """
        self.load_service = JsonFilesService(file_path=self.valid_json_file_path)

        """ Test data
        load_json_file expects a list in valid JSON file """
        self.valid_file_data = [
            {"service": "loan", "enabled": True},
            {"user_id": 112233, "enabled": True},
        ]
        self.invalid_file_data = {"book_id": 212121, "enabled": False}

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_reads_existing_list_from_file(self):
        with self.valid_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_file_data, f)

        self.load_service.file_path = self.valid_json_file_path
        test_result = self.load_service.load_json_file()
        self.assertEqual(test_result, self.valid_file_data)

    def test_returns_empty_list_when_json_file_is_empty(self):
        """expected behavior: json_load_file returns an JSON content as an empty list in case file to load is empty"""
        with self.empty_json_file_path.open("w", encoding="utf-8"):
            pass

        self.load_service.file_path = self.empty_json_file_path
        test_result = self.load_service.load_json_file()
        self.assertEqual(test_result, [])

    def test_raises_error_when_json_file_is_invalid(self):
        """expected behavior: json.JSONDecodeError is caught and exc.FileError is raised in case JSON file is corrupted"""
        self.invalid_json_file_path.write_text(
            '{"book_id": 212121, "enabled": False"', encoding="utf-8"
        )

        self.load_service.file_path = self.invalid_json_file_path
        with self.assertRaises(exc.FileError) as cm:
            self.load_service.load_json_file()

        self.assertIn("Cannot read the file", str(cm.exception))

    def test_raises_error_when_json_file_type_is_not_list(self):
        """expected behavior: raising exc.FileError when JSON file doesn't consist of list of items and has incorrect data type"""
        with self.invalid_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.invalid_file_data, f)

        self.load_service.file_path = self.invalid_json_file_path

        with self.assertRaises(
            exc.FileError
        ) as cm:  # cm stands for: context manager result (the captured exception)
            self.load_service.load_json_file()

        self.assertIn("File should be a list", str(cm.exception))


class TestJsonFileServiceWriteJsonData(unittest.TestCase):  # 4/4
    """Method under test: write_json_data
    Number of TestCases: 4
    Done TestCases: 4
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

        """ Path to test file. We need this file to have a file to write data in it.
        Also preparing test file"""
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"
        self.test_json_file_path.write_text("[]", encoding="utf-8")

        """ valid data must match schema and validator expectations"""
        self.test_schema = {
            "service": str,
            "enabled": bool,
            "fields": {"service": str, "enabled": bool},
            "required": ["service", "enabled"],
        }
        self.valid_data = [
            {"service": "loan", "enabled": True},
            {"user_id": 112233, "enabled": True},
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_data, f, ensure_ascii=True, indent=4, sort_keys=True)

        """ Service under test """
        self.write_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=self.test_schema
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_file_error_if_data_is_none(self):
        """expected behavior: Raises exc.FileError in case the data to save in file is missing or it's an empty value"""
        self.data_to_write = None
        with self.assertRaises(exc.FileError) as cm:
            self.write_service.write_json_data(self.data_to_write)
        self.assertIn("Cannot save empty data", str(cm.exception))

    def test_raises_file_error_if_data_is_not_list(self):
        """expected behavior: Raises exc.FileError in case the data to save in file is not a type of list"""
        self.data_to_write = {"book_id": 123321, "enabled": True}
        with self.assertRaises(exc.FileError) as cm:
            self.write_service.write_json_data(self.data_to_write)
        self.assertIn("Data is not a list", str(cm.exception))

    def test_writes_valid_list_to_file(self):
        """expected behavior: Data is correct and is saved in JSON file. Return message with confirmation is displayed"""
        self.data_to_write = [{"service": "loan", "enabled": True}]
        test_result = self.write_service.write_json_data(self.data_to_write)

        self.assertEqual(test_result, "Success. Data have been saved in the file.")
        self.assertTrue(self.test_json_file_path.exists())

        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertEqual(file_content, self.data_to_write)

    def test_raises_validation_error_for_invalid_record(self):
        """expected behavior: Raises exc.ValidationError in case the data doesn't match schema"""
        self.data_to_write = ["service", "loan", "enabled=True"]
        with self.assertRaises(exc.ValidationError) as cm:
            self.write_service.write_json_data(self.data_to_write)
        self.assertIn("Expected data type is dict", str(cm.exception))


# -------------------------
# CRUD operations | Test cases: 4
# -------------------------


class TestJsonFileServiceAppendDataToFile(unittest.TestCase):  # 4/4
    """Method under test: append_data_to_file
    Number of TestCases: 4
    Done TestCases: 4
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        # Schema format expected by validate_against_schema method.
        self.test_schema = {
            "fields": {"service": str, "enabled": bool},
            "required": ["service", "enabled"],
        }

        # File must contain a JSON list because append_data_to_file method calls .append()
        self.valid_data = [
            {"service": "loan", "enabled": True},
            {"service": "return", "enabled": True},
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_data, f, ensure_ascii=True, indent=4, sort_keys=True)

        self.data_to_append = {"service": "reservation", "enabled": False}

        """ Service under test """
        self.append_data_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=self.test_schema
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_if_data_is_none(self):
        """expected behavior: Raises exc.ValidationError in case the data to append in file is missing or it's an empty value"""
        self.data_to_append = None
        with self.assertRaises(exc.ValidationError) as cm:
            self.append_data_service.append_data_to_file(self.data_to_append)

        self.assertIn("New data is missig or it's an empty value.", str(cm.exception))

    def test_raises_validation_error_if_data_is_not_dict(self):
        """expected behavior: Raises exc.ValidationError in case the data to append in file is not a type of dict"""
        self.data_to_append = ["service", "reservation", "enabled=False"]
        with self.assertRaises(exc.ValidationError) as cm:
            self.append_data_service.append_data_to_file(self.data_to_append)

        self.assertIn("Incorrect type of data to append", str(cm.exception))

    def test_appends_valid_record_to_file(self):
        """expected behavior: Data is correct and is appended to JSON file. Return message with confirmation is displayed"""
        self.append_data_service.append_data_to_file(self.data_to_append)
        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertIn(self.data_to_append, file_content)

    def test_raises_validation_error_for_invalid_record(self):
        """expected behavior: Raises exc.ValidationError in case the data doesn't match schema"""
        self.data_to_append = {"user_id": 123321, "enabled": True}
        with self.assertRaises(exc.ValidationError) as cm:
            self.append_data_service.append_data_to_file(self.data_to_append)

        self.assertIn("Required key is missing", str(cm.exception))


# -------------------------
# Core validation | Test cases: 24
# -------------------------


class TestJsonFileServiceValidateAgainstSchema(unittest.TestCase):  # 21/21
    """Method under test: validate_against_schema
    Number of TestCases: 21
    Done TestCases: 21
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

        # file_path is not used by validate_against_schema method, but it's required to create an instance of JsonFilesService, so we need to prepare it
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.test_schema = {
            "fields": {"service": str, "enabled": bool},
            "required": ["service", "enabled"],
        }

        """ service under test """
        self.validation_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=self.test_schema
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    # ---------------------------------------------------------------------------
    # Guard clauses / early validation
    # - Validate presence of schema
    # - Validate presence of data
    # - Allow None values only when explicitly permitted by schema
    # ---------------------------------------------------------------------------

    def test_raises_validation_error_if_schema_is_empty(self):
        """expected behavior: Raises exc.ValidationError in case the schema to validate against is missing or it's an empty value"""
        data_to_validate = {"service": "loan", "enabled": True}
        empty_test_schema = {}

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                data_to_validate, empty_test_schema
            )

        self.assertIn("Cannot validate against empty schema", str(cm.exception))

    def test_returns_none_if_data_is_none_and_schema_allows_none(self):
        """expected behavior: Returns None in case the data to validate is None and None value is allowed by the schema."""
        data_to_validate = None
        test_schema_allowing_none = type(None)
        test_result = self.validation_service.validate_against_schema(
            data_to_validate, test_schema_allowing_none
        )
        self.assertIsNone(test_result)

    def test_returns_data_if_optional_field_value_is_none(self):
        """expected behavior: Returns data with None value for optional field if the schema allows None values for that field. It means that the field is optional and can be empty."""
        data_to_validate = {"service": None}
        test_schema_with_none_field = {
            "fields": {"service": (str, type(None))},
            "required": ["service"],
        }
        test_result = self.validation_service.validate_against_schema(
            data_to_validate, test_schema_with_none_field
        )

        self.assertEqual(test_result, data_to_validate)

    def test_raises_validation_error_if_data_is_none(self):
        """expected behavior: Raises exc.ValidationError in case the data to validate is missing or it's an empty value."""
        self.data_to_validate = None
        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                self.data_to_validate, self.test_schema
            )

        self.assertIn("Data to validate is missing", str(cm.exception))

    # ---------------------------------------------------------------------------
    # Dict-based schema validation (main schema type)
    # - Data must be a dictionary
    # - Required keys must be present
    # - Field values must match declared field types
    # - Schema dict structure itself must be valid
    # ---------------------------------------------------------------------------

    def test_raises_validation_error_if_data_is_not_dict(self):
        """expected behavior: Raises exc.ValidationError in case the data to validate is not a type of dict"""
        self.data_to_validate = ["service", "return", False]

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                self.data_to_validate, self.test_schema
            )

        self.assertIn("Provided data has wrong type", str(cm.exception))

    def test_raises_validation_error_if_required_key_is_missing(self):
        """expected behavior: Raises exc.ValidationError in case the data to validate is missing required key(s) defined in schema"""
        self.data_to_validate = {"user_id": 123321, "enabled": True}
        # "user_id" is the missing key in the schema

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                self.data_to_validate, self.test_schema
            )

        self.assertIn("Required key is missing", str(cm.exception))

    def test_raises_validation_error_if_field_type_is_wrong(self):
        """expected behavior: Raises exc.ValidationError in case the data to validate has wrong data type for field(s) defined in schema"""
        self.data_to_validate = {"service": 123455, "enabled": "True"}

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                self.data_to_validate, self.test_schema
            )

        self.assertIn("Wrong type of data", str(cm.exception))

    def test_returns_data_if_schema_matches(self):
        """expected behavior: Returns the data if it matches the schema. No exception is raised."""
        self.data_to_validate = {"service": "reserve", "enabled": True}
        result = self.validation_service.validate_against_schema(
            self.data_to_validate, self.test_schema
        )

        self.assertEqual(result, self.data_to_validate)

    def test_raises_validation_error_if_schema_dict_missing_fields_key(self):
        """expected behavior: Raises exc.ValidationError in case the expected key for required fields is missing in the schema."""
        test_schema_without_fields_key = {"required": ["service", "enabled"]}
        data_to_validate = {"service": "loan", "enabled": True}
        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                data_to_validate, test_schema_without_fields_key
            )

        self.assertIn(
            "Format of the schema is invalid",
            str(cm.exception),
        )

    # ---------------------------------------------------------------------------
    # Tuple-based schema validation
    # - "one_of" schema: value must be in allowed set
    # - Alternative schemas: value must match at least one option
    # ---------------------------------------------------------------------------

    def test_returns_data_if_one_of_schema_value_is_allowed(self):
        """expected behavior:  Data is returned in case the value matches to "one_of" the values allowed by the schema."""
        test_schema_with_one_of = {
            "fields": {"service": ("one_of", ["loan", "return", "reservation"])},
            "required": ["service"],
        }
        data_to_validate = {"service": "loan"}

        test_result = self.validation_service.validate_against_schema(
            data_to_validate, test_schema_with_one_of
        )

        self.assertEqual(test_result, data_to_validate)

    def test_raises_validation_error_if_one_of_schema_value_is_not_allowed(self):
        """expected behavior: raises exc.ValidationEror in case the value does not match to "one_of" the values allowed by the schema."""
        test_schema_with_one_of = {
            "fields": {"service": ("one_of", ["loan", "return", "reservation"])},
            "required": ["service"],
        }
        data_to_validate = {"service": "cancel"}

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                data_to_validate, test_schema_with_one_of
            )

        self.assertIn(
            "Provided value of the field is not valid",
            str(cm.exception),
        )

    def test_returns_data_if_tuple_schema_matches_any_option(self):
        """expected behavior: Data is returned in case the value matches to at least one of the options defined in tuple schema."""
        test_schema_with_tuple_options = {
            "fields": {"service": ("one_of", ["loan", "return", "reservation"])},
            "required": ["service"],
        }
        data_to_validate = {"service": "return"}

        test_result = self.validation_service.validate_against_schema(
            data_to_validate, test_schema_with_tuple_options
        )

        self.assertEqual(test_result, data_to_validate)

    def test_raises_validation_error_if_tuple_schema_matches_no_option(self):
        """expected behavior: raises exc.ValidationEror in case the value does not match any of the schema options in a tuple."""
        test_schema_with_tuple = {
            "fields": {"service": (int, bool)},
            "required": ["service"],
        }
        data_to_validate = {"service": "loan"}

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                data_to_validate, test_schema_with_tuple
            )

        self.assertIn(
            "Provided value does not match any of the options in the schema",
            str(cm.exception),
        )

    # ---------------------------------------------------------------------------
    # String-based schema validation: "date"
    # - Value must be a string
    # - Value must follow YYYY-MM-DD format
    # ---------------------------------------------------------------------------

    def test_raises_validation_error_if_schema_date_and_data_is_not_string(self):
        """expected behavior: Raises exc.ValidationError in case the date data is not a string value."""
        test_schema_with_date = {
            "fields": {"loan_date": str},
            "required": ["loan_date"],
        }
        data_to_validate = {"loan_date": 20260417}

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                data_to_validate, test_schema_with_date
            )

        self.assertIn("Wrong type of data", str(cm.exception))

    def test_raises_validation_error_if_schema_date_and_format_is_invalid(self):
        """expected behavior: Raises exc.ValidationError in case the date data does not follow the expected YYYY-MM-DD format."""
        test_schema_with_date = {
            "fields": {"loan_date": "date"},
            "required": ["loan_date"],
        }
        data_to_validate = {"loan_date": "2026/04/17"}

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                data_to_validate, test_schema_with_date
            )

        self.assertIn("Invalid date format", str(cm.exception))

    def test_returns_data_if_schema_date_and_format_is_valid(self):
        """expected behavior: Returns the data in case the date data is a string value and follows the expected format."""
        test_schema_with_date = {
            "fields": {"loan_date": "date"},
            "required": ["loan_date"],
        }
        data_to_validate = {"loan_date": "2026-04-17"}

        test_result = self.validation_service.validate_against_schema(
            data_to_validate, test_schema_with_date
        )

        self.assertEqual(test_result, data_to_validate)

    # ---------------------------------------------------------------------------
    # String-based schema validation: "datetime"
    # - Value must be a string
    # - Value must follow ISO datetime format
    # ---------------------------------------------------------------------------

    def test_raises_validation_error_if_schema_datetime_and_data_is_not_string(self):
        """expected behavior: Raises exc.ValidationError in case the datetime data is not a string value."""
        test_schema_with_datetime = {
            "fields": {"loging_date": str},
            "required": ["loging_date"],
        }
        data_to_validate = {"loging_date": 20260417}

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                data_to_validate, test_schema_with_datetime
            )

        self.assertIn("Wrong type of data", str(cm.exception))

    def test_raises_validation_error_if_schema_datetime_and_format_is_invalid(self):
        """expected behavior: Raises exc.ValidationError in case the datetime data does not follow the expected ISO datetime format. (YYYY-MM-DDTHH:MM:SS)"""
        test_schema_with_datetime = {
            "fields": {"loging_date": "datetime"},
            "required": ["loging_date"],
        }
        data_to_validate = {"loging_date": "2026/04/17T12-16-00"}

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                data_to_validate, test_schema_with_datetime
            )

        self.assertIn("Invalid datetime format", str(cm.exception))

    def test_returns_data_if_schema_datetime_and_format_is_valid(self):
        """expected behavior: Returns the data in case the datetime data is a string value and follows the expected ISO datetime format."""
        test_schema_with_datetime = {
            "fields": {"loging_date": "datetime"},
            "required": ["loging_date"],
        }
        data_to_validate = {"loging_date": "2026-04-17T12:16:00"}

        test_result = self.validation_service.validate_against_schema(
            data_to_validate, test_schema_with_datetime
        )

        self.assertEqual(test_result, data_to_validate)

    # ---------------------------------------------------------------------------
    # Unsupported schema definitions
    # - Unsupported string schema
    # - Unsupported schema type
    # ---------------------------------------------------------------------------

    def test_raises_validation_error_if_schema_is_unsupported_string(self):
        """expected behavior: Raises exc.ValidationError in case that defined schema is unsupported string other than "date" or "datetime"."""
        test_schema_with_unsupported_string = {
            "fields": {"loan_date": "loan_date"},
            "required": ["loan_date"],
        }
        data_to_validate = {"loan_date": "2026-04-17"}

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                data_to_validate, test_schema_with_unsupported_string
            )

        self.assertIn("Unsupported string schema", str(cm.exception))

    def test_raises_validation_error_if_schema_type_is_unsupported(self):
        """expected behavior: Raises exc.ValidationError in case that defined schema is unsupported type other than dict, tuple, or string."""
        test_schema_with_unsupported_type = {
            "fields": {"service": int},
            "required": ["service"],
        }
        data_to_validate = {"service": "loan"}

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                data_to_validate, test_schema_with_unsupported_type
            )

        self.assertIn("Wrong type of data", str(cm.exception))


class TestJsonFileServiceValidateFileData(unittest.TestCase):
    """Method under test: validate_file_data
    Number of TestCases: 4
    Done TestCases: 4

    Test cases with errors:
    - test_raises_validation_error_if_record_does_not_match_schema
    - test_returns_true_if_all_records_are_valid
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.test_schema = {
            "service": str,
            "enabled": bool,
            "fields": {"service": str, "enabled": bool},
            "required": ["service", "enabled"],
        }

        self.validation_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=self.test_schema
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_if_file_is_empty(self):
        """expected behavior: Raises exc.ValidationError in case the file to validate is empty. The file should contain a list of records to be valid."""
        self.test_file = self.test_json_file_path
        self.test_file.write_text("", encoding="utf-8")

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_file_data()

        self.assertIn("Cannot validate fields in an empty file", str(cm.exception))

    def test_raises_validation_error_if_record_is_not_dict(self):
        """expected behavior: Raises exc.ValidationError in case the file to validate contains record(s) that are not of type dict. Each record in the file should be a dict to be valid."""
        self.test_file = self.test_json_file_path

        self.test_file_data = ["service", "enabled", True]

        with self.test_file.open("w", encoding="utf-8") as f:
            json.dump(
                self.test_file_data, f, ensure_ascii=True, indent=4, sort_keys=True
            )

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_file_data()

        self.assertIn("not a dictionary.", str(cm.exception))

    def test_raises_validation_error_if_record_does_not_match_schema(
        self,
    ):  # tc to repair
        """expected behavior: Raises exc.ValidationError in case the file to validate contains record(s) that do not match the defined schema. Each record in the file should conform to the schema to be valid."""
        self.test_file = self.test_json_file_path

        self.test_file_data = [{"service": 123456, "enabled": "True"}]

        with self.test_file.open("w", encoding="utf-8") as f:
            json.dump(
                self.test_file_data, f, ensure_ascii=True, indent=4, sort_keys=True
            )

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_file_data()

        self.assertIn("Wrong type of data", str(cm.exception))

    def test_returns_true_if_all_records_are_valid(self):  # tc to repair
        """expected behavior: Returns True if all records in the file are valid according to the defined schema. No exception is raised."""
        self.test_file = self.test_json_file_path

        self.test_file_data = [{"service": "loan", "enabled": True}]

        with self.test_file.open("w", encoding="utf-8") as f:
            json.dump(
                self.test_file_data, f, ensure_ascii=True, indent=4, sort_keys=True
            )

        result = self.validation_service.validate_file_data()

        self.assertTrue(result)


# -------------------------
# Backup helpers | Test cases: 9
# -------------------------


class TestJsonFileServiceGetOrCreateBackupDir(unittest.TestCase):  # 2/2
    """Method under test: get_or_create_backup_dir
    Number of TestCases: 2
    Done TestCases: 2
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.backup_files_service = JsonFilesService(file_path=self.test_json_file_path)

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_creates_backup_directory_if_missing(self):
        """expected behavior: get_or_create_backup_dir creates a backup directory if it doesn't exist and returns the path to the created directory. The method should ensure that the backup directory is created successfully and is ready for use."""
        self.expected_backup_dir = (
            config.BACKUP_FILES_DIRECTORY / self.test_json_file_path.stem
        )

        result = self.backup_files_service.get_or_create_backup_dir()

        self.assertTrue(self.expected_backup_dir.exists())
        self.assertEqual(result, self.expected_backup_dir)

    def test_returns_existing_backup_directory(self):
        """expected behavior: get_or_create_backup_dir returns the path to the existing backup directory if it already exists. The method should recognize that the backup directory is already present and return its path without attempting to create a new one."""
        self.existing_backup_dir = (
            config.BACKUP_FILES_DIRECTORY / self.test_json_file_path.stem
        )

        self.existing_backup_dir.mkdir(parents=True, exist_ok=True)
        result = self.backup_files_service.get_or_create_backup_dir()

        self.assertEqual(result, self.existing_backup_dir)


class TestJsonFileServiceBuildBackupFileName(unittest.TestCase):  # 3/3
    """Method under test: build_backup_file_name
    Number of TestCases: 3
    Done TestCases: 3
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.backup_service = JsonFilesService(file_path=self.test_json_file_path)

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_backup_name_has_correct_name(self):
        """expected behavior: build_backup_file_name generates a backup file name that includes the alias stem and a timestamp. The generated file name should follow the expected format and contain the relevant information to identify the backup."""
        alias = config.PROJECT_ALIAS
        name = self.test_json_file_path.stem
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self.expected_backup_file_name = f"{alias}_{name}_{timestamp}.json"
        result = self.backup_service.build_backup_file_name()
        self.assertIn(self.expected_backup_file_name, result)

    def test_backup_name_contains_timestamp(self):
        """expected behavior: build_backup_file_name generates a backup file name that includes a timestamp. The generated file name should contain a timestamp that indicates when the backup was created, allowing for easy identification and organization of backup files."""
        timestamp_before = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        result = self.backup_service.build_backup_file_name()
        timestamp_after = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self.assertTrue(timestamp_before in result or timestamp_after in result)

    def test_backup_name_has_json_extension(self):
        """expected behavior: build_backup_file_name generates a backup file name that has a .json extension. The generated file name should end with the .json extension, indicating that it is a JSON file and can be easily recognized as such."""
        result = self.backup_service.build_backup_file_name()
        self.assertTrue(result.endswith(".json"))


class TestJsonFileServiceCreateBackupFile(unittest.TestCase):  # 4/4
    """Method under test: create_backup_file
    Number of TestCases: 4
    Done TestCases: 4
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

        self.test_backup_root_directory = self.temporary_dir_path / "backups"

        """ Temporarily changing the backup working directory path in config to use the temporary directory for testing """
        self.backup_directory_patch = patch(
            "utils.config.BACKUP_FILES_DIRECTORY", self.test_backup_root_directory
        )
        self.backup_directory_patch.start()

        """ Preparing test file with valid data to create backup from the file. The file must exist and have valid data to create backup successfully."""
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"
        self.test_file_data = [{"service": "loan", "enabled": True}]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(
                self.test_file_data, f, ensure_ascii=False, indent=4, sort_keys=True
            )

        self.test_schema = {"service": str, "enabled": bool}

        """ service under test"""
        self.create_backup_service = JsonFilesService(
            self.test_json_file_path, schema=self.test_schema
        )

    def tearDown(self):
        self.backup_directory_patch.stop()
        self.temporary_dir.cleanup()

    def test_creates_backup_file_and_returns_path(self):
        """expected behavior: create_backup_file creates a backup file with the correct name and returns the path to the created backup file. The method should successfully create the backup file and provide the correct path for reference."""

        self.test_backup_file_path = self.create_backup_service.create_backup_file()
        """ calling method under the test and storing the returned value"""

        self.assertIsInstance(self.test_backup_file_path, Path)
        """ confirming that the method create_backup_file returns a Path"""

        self.assertTrue(self.test_backup_file_path.exists())
        """ veryfing the the returned path actually exists in the file system"""

        self.assertTrue(self.test_backup_file_path.is_file())
        """ confirming that the returned path is a file, not a directory"""

        self.assertTrue(self.test_json_file_path.exists())
        """ confirming that the source file was not removed or overwritten during the backup file creation process"""

    def test_backup_file_contains_same_data_as_source_file(self):
        """expected behavior: create_backup_file creates a backup file that contains the same data as the source file. The method should ensure that the content of the backup file matches the content of the source file, providing an accurate copy for backup purposes."""
        self.test_backup_file_path = self.create_backup_service.create_backup_file()
        with self.test_backup_file_path.open("r", encoding="utf-8") as f:
            backup_data = json.load(f)

        self.assertEqual(backup_data, self.test_file_data)

    def test_creates_backup_directory_if_missing(self):
        """expected behavior: create_backup_file creates a backup directory if it doesn't exist before creating the backup file. The method should ensure that the backup directory is created successfully if it is missing, allowing for proper organization of backup files."""
        self.expected_backup_directory_path = (
            config.BACKUP_FILES_DIRECTORY / self.test_json_file_path.stem
        )

        self.assertFalse(self.expected_backup_directory_path.exists())

        self.test_backup_file_path = self.create_backup_service.create_backup_file()

        self.assertTrue(self.expected_backup_directory_path.exists())
        self.assertTrue(self.expected_backup_directory_path.is_dir())

        self.assertEqual(
            self.test_backup_file_path.parent, self.expected_backup_directory_path
        )

    def test_backup_file_name_contains_alias_stem_and_timestamp(self):
        """expected behavior: create_backup_file generates a backup file name that includes the alias stem and a timestamp. The generated file name should follow the expected format and contain the relevant information to identify the backup, including the alias stem and the timestamp."""
        self.test_backup_file_path = self.create_backup_service.create_backup_file()
        self.backup_file_name = self.test_backup_file_path.name

        self.assertTrue(self.test_backup_file_path.name.endswith(".json"))
        self.assertIn(config.PROJECT_ALIAS, self.backup_file_name)

        self.assertIn(self.test_json_file_path.stem, self.backup_file_name)


# -------------------------
# Remove/Update operations | Test cases: 10
# -------------------------


class TestJsonFileServiceRemoveFromFile(unittest.TestCase):  # 5/5
    """Method under test: remove_from_file
    Number of TestCases: 5
    Done TestCases: 5
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.test_file_data = [
            {"service": "loan", "enabled": True},
            {"service": "return", "enabled": False},
            {"service": "login", "enabled": True},
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.test_file_data, f, ensure_ascii=False, indent=4)

        self.test_schema = {
            "service": str,
            "enabled": bool,
            "fields": {"service": str, "enabled": bool},
            "required": ["service", "enabled"],
        }

        self.remove_service = JsonFilesService(
            self.test_json_file_path, schema=self.test_schema
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_if_key_name_is_none(self):
        """expected behavior: Raises exc.ValidationError in case the key name to identify record(s) for removal is missing or it's an empty value. The method should validate the input and ensure that a valid key name is provided for the removal operation."""
        self.test_key_name = None
        self.test_key_value = "return"

        with self.assertRaises(exc.ValidationError) as cm:
            self.remove_service.remove_from_file(
                self.test_key_name, self.test_key_value
            )

        self.assertIn("Key name is missing", str(cm.exception))

    def test_raises_validation_error_if_key_value_is_none(self):
        """expected behavior: Raises exc.ValidationError in case the key value to identify record(s) for removal is missing or it's an empty value. The method should validate the input and ensure that a valid key value is provided for the removal operation."""
        self.test_key_name = "service"
        self.test_key_value = None

        with self.assertRaises(exc.ValidationError) as cm:
            self.remove_service.remove_from_file(
                self.test_key_name, self.test_key_value
            )

        self.assertIn("Key value is missing", str(cm.exception))

    def test_raises_invalid_field_error_if_key_not_in_schema(self):
        """expected behavior: Raises exc.InvalidFieldError in case the key name provided for removal is not defined in the schema. The method should validate the key name against the schema and ensure that it is a valid field for identifying records to remove."""
        self.test_key_name = "book_title"
        self.test_key_value = "The Iliad"

        with self.assertRaises(exc.InvalidFieldError) as cm:
            self.remove_service.remove_from_file(
                self.test_key_name, self.test_key_value
            )

        self.assertIn("is not present in file schema", str(cm.exception))

    def test_raises_database_error_if_no_matching_record_found(self):
        """expected behavior: Raises exc.DatabaseError in case no record matching the provided key name and value is found in the file. The method should search for records based on the provided key and value, and if no matching record is found, it should raise an appropriate error to indicate that the removal operation cannot be performed."""
        self.test_key_name = "service"
        self.test_key_value = "The Iliad"

        with self.assertRaises(exc.DatabaseError) as cm:
            self.remove_service.remove_from_file(
                self.test_key_name, self.test_key_value
            )

        self.assertIn("No matching elements to key", str(cm.exception))

    def test_removes_matching_records_and_saves_file(self):  # tc to repair
        """expected behavior: Removes all records matching the provided key name and value from the file and saves the updated file. The method should successfully identify and remove the matching records, and then save the changes to the file, ensuring that the file reflects the removal of the specified records."""
        self.test_key_name = "service"
        self.test_key_value = "login"

        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            test_file_content = json.load(f)

        self.assertIn({"service": "login", "enabled": True}, test_file_content)

        self.remove_service.remove_from_file(self.test_key_name, self.test_key_value)

        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            updated_file_content = json.load(f)

        self.assertNotIn({"service": "login", "enabled": True}, updated_file_content)


class TestJsonFileServiceUpdateDataInFile(unittest.TestCase):
    """Method under test: update_data_in_file
    Number of TestCases: 5
    Done TestCases: 5

    Test case with errors:
    - test_updates_existing_field_and_saves_file
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.test_file_data = [
            {"service": "loan", "enabled": True},
            {"service": "return", "enabled": False},
            {"service": "login", "enabled": True},
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(
                self.test_file_data, f, ensure_ascii=False, indent=4, sort_keys=True
            )

        self.test_schema = {
            "service": str,
            "enabled": bool,
            "fields": {"service": str, "enabled": bool},
            "required": ["service", "enabled"],
        }

        self.update_service = JsonFilesService(
            self.test_json_file_path, schema=self.test_schema
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_file_error_if_item_is_none(self):
        """expected behavior: Raises exc.FileError in case the item to update is missing or it's an empty value. The method should validate the input and ensure that a valid item is provided for the update operation."""
        self.test_item_to_update = None
        self.new_value = "logout"
        self.match_key = "service"
        self.match_value = "loan"

        with self.assertRaises(exc.FileError) as cm:
            self.update_service.update_data_in_file(
                self.test_item_to_update,
                self.new_value,
                self.match_key,
                self.match_value,
            )

        self.assertIn("Item to update can't be empty value.", str(cm.exception))

    def test_raises_invalid_field_error_if_item_not_in_schema(self):
        """expected behavior: Raises exc.InvalidFieldError in case the item provided for update is not defined in the schema. The method should validate the item against the schema and ensure that all fields in the item are valid according to the defined schema."""
        self.test_item_to_update = "book_title"
        self.new_value = "The Iliad"
        self.match_key = "service"
        self.match_value = "loan"

        with self.assertRaises(exc.InvalidFieldError) as cm:
            self.update_service.update_data_in_file(
                self.test_item_to_update,
                self.new_value,
                self.match_key,
                self.match_value,
            )

        self.assertIn("is not present in file schema", str(cm.exception))

    def test_raises_validation_error_if_new_data_is_none(self):
        """expected behavior: Raises exc.ValidationError in case the new data for update is missing or it's an empty value. The method should validate the input and ensure that valid new data is provided for the update operation."""
        self.test_item_to_update = "service"
        self.new_value = None
        self.match_key = "service"
        self.match_value = "loan"

        with self.assertRaises(exc.ValidationError) as cm:
            self.update_service.update_data_in_file(
                self.test_item_to_update,
                self.new_value,
                self.match_key,
                self.match_value,
            )

        self.assertIn("New data is missing", str(cm.exception))

    def test_raises_database_error_if_item_not_found_in_records(self):
        """expected behavior: Raises exc.DatabaseError in case No record matches the selection criteria (match_key == match_value). The method should search for the item in the file based on the provided data, and if the item is not found, it should raise an appropriate error to indicate that the update operation cannot be performed."""
        self.test_schema = {
            "service": str,
            "enabled": bool,
            "status": str,
        }
        self.test_item_to_update = "status"
        self.new_value = "active"
        self.match_key = "service"
        self.match_value = "reservation"

        update_service = JsonFilesService(self.test_json_file_path, self.test_schema)

        with self.assertRaises(exc.DatabaseError) as cm:
            update_service.update_data_in_file(
                self.test_item_to_update,
                self.new_value,
                self.match_key,
                self.match_value,
            )

        self.assertIn("No matching element", str(cm.exception))

    def test_updates_existing_field_and_saves_file(self):  # tc to repair
        """expected behavior: Updates an existing field in the item with new data and saves the updated file. The method should successfully identify the item to update, apply the new data to the existing field, and then save the changes to the file, ensuring that the file reflects the updated information for the specified item."""
        self.test_item_to_update = "service"
        self.new_value = "logout"
        self.match_key = "service"
        self.match_value = "login"

        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            test_file_content = json.load(f)

        self.assertIn({"service": "login", "enabled": True}, test_file_content)

        self.update_service.update_data_in_file(
            self.test_item_to_update, self.new_value, self.match_key, self.match_value
        )

        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            new_file_content = json.load(f)

        self.assertIn({"service": "loan", "enabled": True}, new_file_content)
        self.assertIn({"service": "return", "enabled": False}, new_file_content)


if __name__ == "__main__":
    unittest.main(verbosity=0)
