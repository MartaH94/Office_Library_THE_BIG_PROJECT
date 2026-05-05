"""
________________________________________________________
tests.test_book_json_file_service.py
========================================================
Test for the file book_json_file_service.py
________________________________________________________

Test classes: 5
Test cases total: 21
Done test cases: 21

current status: Done
"""

import json
import tempfile
import unittest
from pathlib import Path

import exceptions as exc
from database.book_json_file_service import BookJsonFileService
from database.database_schemes import book_schema
from database.json_files_major_services import JsonFilesService


class TestBookJsonFileServiceGetBookData(unittest.TestCase):  # 3/3
    """Method under test: get_book_data
    Number of TestCases: 3
    Done TestCases: 3
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.valid_book_list = [
            {
                "book_id": 1001,
                "author": "Stephen King",
                "title": "It",
                "publication_year": 1986,
            },
            {
                "book_id": 1002,
                "author": "Frank Herbert",
                "title": "Dune",
                "publication_year": 1965,
            },
            {
                "book_id": 1003,
                "author": "Jane Austen",
                "title": "Emma",
                "publication_year": 1815,
            },
            {
                "book_id": 1004,
                "author": "Peter Benchley",
                "title": "Jaws",
                "publication_year": 1974,
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_book_list, f)

        self.major_json_service = JsonFilesService(file_path=self.test_json_file_path)

        self.book_service = BookJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_book_id_is_none(self):
        """expected behavior: raises ValidationError when book_id is None"""
        with self.assertRaises(exc.ValidationError) as cm:
            self.book_service.get_book_data(None)

        self.assertIn("Book ID is missing", str(cm.exception))

    def test_returns_book_when_book_id_exists(self):
        """expected behavior: returns book data when book_id exists in the database"""
        expected_book_data = self.valid_book_list[0]
        test_result = self.book_service.get_book_data(1001)
        self.assertEqual(test_result, expected_book_data)

    def test_raises_book_not_found_error_when_book_id_not_found(self):
        """expected behavior: raises BookNotFoundError when book_id is not found in the database"""
        with self.assertRaises(exc.BookNotFoundError) as cm:
            self.book_service.get_book_data(1006)

        self.assertIn("not exists in database", str(cm.exception))


class TestBookJsonFileServiceAddBookData(unittest.TestCase):  # 5/5
    """Method under test: add_book_data
    Number of TestCases: 5
    Done TestCases: 5
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.valid_book_list = [
            {
                "book_id": 1001,
                "author": "Stephen King",
                "title": "It",
                "publication_year": 1986,
            },
            {
                "book_id": 1002,
                "author": "Frank Herbert",
                "title": "Dune",
                "publication_year": 1965,
            },
            {
                "book_id": 1003,
                "author": "Jane Austen",
                "title": "Emma",
                "publication_year": 1815,
            },
            {
                "book_id": 1004,
                "author": "Peter Benchley",
                "title": "Jaws",
                "publication_year": 1974,
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_book_list, f)

        self.major_json_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=book_schema
        )

        self.book_service = BookJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_book_data_is_missing(self):
        """expected behavior: raises ValidationError when book data is missing or it's an empty value"""
        with self.assertRaises(exc.ValidationError) as cm:
            self.book_service.add_book_data(None)

        self.assertIn("Book data to save is missing.", str(cm.exception))

    def test_raises_data_type_error_when_book_data_is_not_dict(self):
        """expected behavior: raises DataTypeError when book data is not a dict type"""
        data_to_add = [1005, "William Shakespeare", "Macbeth", 1606]

        with self.assertRaises(exc.DataTypeError) as cm:
            self.book_service.add_book_data(data_to_add)

        self.assertIn("Book data type is incorrect.", str(cm.exception))

    def test_raises_book_error_when_book_id_already_exists(self):
        """expected behavior: raises BookError when book_id already exists in the database"""
        data_to_add = {
            "book_id": 1001,
            "author": "William Shakespeare",
            "title": "Macbeth",
            "publication_year": 1606,
        }

        with self.assertRaises(exc.BookError) as cm:
            self.book_service.add_book_data(data_to_add)

        self.assertIn("Book ID number must be unique value", str(cm.exception))

    def test_raises_book_validation_error_when_schema_validation_raises_validation_error(
        self,
    ):
        """expected behavior: raises BookValidationError when book data doesn't match database file schema and schema validation raises ValidationError"""
        data_to_append = {
            "book_id": 1005,
            "author": "William Shakespeare",
            "title": "Macbeth",
        }

        with self.assertRaises(exc.BookValidationError) as cm:
            self.book_service.add_book_data(data_to_append)

        self.assertIn("Book data doesn't match database file schema", str(cm.exception))

    def test_writes_json_and_returns_success_message_when_data_is_valid(self):
        """expected behavior: writes new book data to json file and returns success message when book data is valid"""
        data_to_append = {
            "book_id": 1005,
            "author": "William Shakespeare",
            "title": "Macbeth",
            "publication_year": 1606,
        }

        result = self.book_service.add_book_data(data_to_append)

        self.assertIn("Added new book to data base", result)

        with self.test_json_file_path.open() as f:
            self.assertIn(data_to_append, json.load(f))


class TestBookJsonFileServiceGetAllBooksList(unittest.TestCase):  # 3/3
    """Method under test: get_all_books_list
    Number of TestCases: 3
    Done TestCases: 3
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.major_json_service = JsonFilesService(file_path=self.test_json_file_path)
        self.book_service = BookJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_returns_all_books_valid_book_dicts_as_list(self):
        """expected behavior: returns a list of all books in the database."""

        self.valid_book_list = [
            {
                "book_id": 1001,
                "author": "Stephen King",
                "title": "It",
                "publication_year": 1986,
            },
            {
                "book_id": 1002,
                "author": "Frank Herbert",
                "title": "Dune",
                "publication_year": 1965,
            },
            {
                "book_id": 1003,
                "author": "Jane Austen",
                "title": "Emma",
                "publication_year": 1815,
            },
            {
                "book_id": 1004,
                "author": "Peter Benchley",
                "title": "Jaws",
                "publication_year": 1974,
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_book_list, f)

        expected_result = self.valid_book_list
        test_result = self.book_service.get_all_books_list()

        self.assertEqual(test_result, expected_result)

    def test_raises_book_not_found_error_when_database_is_empty(self):
        """expected behavior: raises BookNotFoundError when there are no books in the database."""

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump([], f)

        with self.assertRaises(exc.BookNotFoundError) as cm:
            self.book_service.get_all_books_list()

        self.assertIn("No book found in the database", str(cm.exception))

    def test_raises_book_not_found_error_when_no_valid_book_entries_exist(self):
        """expected behavior: raises BookNotFoundError when there are no valid book entries in the database."""
        invalid_book_list = ["Jane Austen", "Emma", "Peter Benchley", "Jaws"]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(invalid_book_list, f)

        with self.assertRaises(exc.BookNotFoundError) as cm:
            self.book_service.get_all_books_list()

        self.assertIn("No book found in the database", str(cm.exception))


class TestBookJsonFileServiceUpdateBookData(unittest.TestCase):  # 7/7
    """Method under test: update_book_data
    Number of TestCases: 7
    Done TestCases: 7
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.valid_book_list = [
            {
                "book_id": 1001,
                "author": "Stephen King",
                "title": "It",
                "publication_year": 1986,
            },
            {
                "book_id": 1002,
                "author": "Frank Herbert",
                "title": "Dune",
                "publication_year": 1965,
            },
            {
                "book_id": 1003,
                "author": "Jane Austen",
                "title": "Emma",
                "publication_year": 1815,
            },
            {
                "book_id": 1004,
                "author": "Peter Benchley",
                "title": "Jaws",
                "publication_year": 1974,
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_book_list, f)

        self.major_json_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=book_schema
        )
        self.book_service = BookJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_book_id_is_none(self):
        """expected behavior: raises ValidationError when book_id is missing or it's an empty value."""

        with self.assertRaises(exc.ValidationError) as cm:
            self.book_service.update_book_data(
                book_id=None, field="book_id", new_value=1006
            )

        self.assertIn("Book ID is missing or it's an empty value", str(cm.exception))

    def test_raises_validation_error_when_field_is_none(self):
        """expected behavior: raises ValidationError when field name is missing or it's an empty value."""
        with self.assertRaises(exc.ValidationError) as cm:
            self.book_service.update_book_data(
                book_id=1001, field=None, new_value="The Hobbit"
            )

        self.assertIn(
            "The field value is missing or it's an empty value", str(cm.exception)
        )

    def test_raises_validation_error_when_new_value_is_none(self):
        """expected behavior: raises ValidationError when new value to update book record is missing or it's an empty value."""
        with self.assertRaises(exc.ValidationError) as cm:
            self.book_service.update_book_data(
                book_id=1001, field="title", new_value=None
            )

        self.assertIn(
            "New value to update book record is incorrect or is empty value",
            str(cm.exception),
        )

    def test_raises_validation_error_when_field_not_in_book(self):
        """expected behavior: raises ValidationError when the field to update is not present in the book record."""
        with self.assertRaises(exc.ValidationError) as cm:
            self.book_service.update_book_data(
                book_id=1001, field="status", new_value="reserved"
            )

        self.assertIn("missing in this book entry", str(cm.exception))

    def test_raises_book_not_found_error_when_book_id_not_found(self):
        """expected behavior: raises BookNotFoundError when book_id is not found in the database."""
        with self.assertRaises(exc.BookNotFoundError) as cm:
            self.book_service.update_book_data(
                book_id=1010, field="titile", new_value="The Hobbit"
            )

        self.assertIn("not found in database", str(cm.exception))

    def test_raises_book_validation_error_when_updated_book_data_fails_schema_validation(
        self,
    ):
        """expected behavior: raises BookValidationError when updated book data doesn't match database file schema."""
        with self.assertRaises(exc.BookValidationError) as cm:
            self.book_service.update_book_data(
                book_id=1001, field="title", new_value=1234
            )

        self.assertIn("Validation failed", str(cm.exception))

    def test_updates_book_field_and_writes_json_when_data_is_valid(self):
        """expected behavior: updates specified field of the book record with new value and writes updated data to json file when book_id exists and data is valid."""
        test_result = self.book_service.update_book_data(
            book_id=1001, field="title", new_value="The Hobbit"
        )

        self.assertIn("New data value has been saved", str(test_result))

        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            updated_book_data = json.load(f)

        for book in updated_book_data:
            if book.get("book_id") == 1001:
                self.assertEqual(book.get("title"), "The Hobbit")
                break


class TestBookJsonFileServiceDeleteBookById(unittest.TestCase):  # 3/3
    """Method under test: delete_book_by_id
    Number of TestCases: 3
    Done TestCases: 3
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.valid_book_list = [
            {
                "book_id": 1001,
                "author": "Stephen King",
                "title": "It",
                "publication_year": 1986,
            },
            {
                "book_id": 1002,
                "author": "Frank Herbert",
                "title": "Dune",
                "publication_year": 1965,
            },
            {
                "book_id": 1003,
                "author": "Jane Austen",
                "title": "Emma",
                "publication_year": 1815,
            },
            {
                "book_id": 1004,
                "author": "Peter Benchley",
                "title": "Jaws",
                "publication_year": 1974,
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_book_list, f)

        self.major_json_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=book_schema
        )
        self.book_service = BookJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_book_id_is_none(self):
        """expected behavior: raises ValidationError when book_id is missing or it's an empty value."""
        with self.assertRaises(exc.ValidationError) as cm:
            self.book_service.delete_book_by_id(book_id=None)

        self.assertIn("Book ID is missing", str(cm.exception))

    def test_raises_book_not_found_error_when_book_id_not_found(self):
        """expected behavior: raises BookNotFoundError when book_id is not found in the database."""
        with self.assertRaises(exc.BookNotFoundError) as cm:
            self.book_service.delete_book_by_id(book_id=2222)

        self.assertIn("could not be removed", str(cm.exception))

    def test_removes_book_and_writes_json_when_book_id_exists(self):
        """expected behavior: removes book record from the database and writes updated data to json file when book_id exists in the database."""
        test_result = self.book_service.delete_book_by_id(book_id=1001)

        self.assertIn("has been deleted from the database", str(test_result))

        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            updated_book_data = json.load(f)

        self.assertEqual(len(updated_book_data), 3)

        for book in updated_book_data:
            self.assertNotEqual(book.get("book_id"), 1001)


if __name__ == "__main__":
    unittest.main(verbosity=0)
