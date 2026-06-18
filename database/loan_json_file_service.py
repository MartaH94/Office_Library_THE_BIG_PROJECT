"""
__________________________________________________________
database.loan_json_file_service
==========================================================
Service class for managing book loan data in a JSON file.
__________________________________________________________

Loan JSON storage service.

This module provides a high-level interface for managing book loan records stored in
a JSON file. It supports adding new loans, retrieving individual records, listing
loans, updating loan details, and deleting loan entries. All I/O operations and schema
validation are delegated to JsonFilesService, ensuring consistent data handling across
the application.

module status: requires refactor !!!

TO DO:
- build reservation service by adding reservation methods to class LoanJsonFileService
- prepare reservation_list_file_path


# RESERVATION METHODS TO IMPLEMENT:
get_reservation_data()
add_reservation_data()
get_all_reservations_list()
delete_reservation_data()


"""

import database.database_schemes as schema
import exceptions as exc
from database.json_files_major_services import JsonFilesService
from utils.config import LOANS_LIST_FILE_PATH, RESERVATIONS_LIST_FILE_PATH


class LoanJsonFileService:
    """High-level operations for loan records stored in a JSON file.

    Provides helper methods to load, modify, validate, and delete loan entries.
    Works together with JsonFilesService to maintain correct structure and data integrity.
    """

    def __init__(self, json_service: JsonFilesService, file_path=LOANS_LIST_FILE_PATH):
        self.json_service = json_service
        self.file_path = file_path

    def get_loan_data(self, loan_id):
        """Return a single loan record by its ID.
        Args:
            loan_id (int): ID of the loan to retrieve.
        Returns:
            loan_data (dict): The matching loan record.
        """
        current_data = self.json_service.load_json_file()
        loan_found = False
        loan_data = None

        if loan_id is None:
            raise exc.ValidationError(
                "Loan ID is missing or it's an empty value. Getting loan record data is not possible."
            )

        for loan in current_data:
            if loan["loan_id"] == loan_id:
                loan_data = loan
                loan_found = True
                break

        if not loan_found:
            raise exc.LoanNotFoundError(
                f"Loan with {loan_id} does not exists in database."
            )

        return loan_data

    def add_loan_data(self, loan_data):
        """Add a new loan record to the JSON file.
        Args:
            loan_data (dict): The loan data to add.
        Returns:
            str: Message with confirmation of success.
        """
        current_data = self.json_service.load_json_file()

        if not loan_data:
            raise exc.ValidationError("Loan data to save is missing or it's incorrect.")

        if not isinstance(loan_data, dict):
            raise exc.DataTypeError(
                "Loan data type is incorrect. Loan data must be a dictionary"
            )

        try:
            validated_loan_data = self.json_service.validate_against_schema(
                loan_data, schema.loan_schema
            )
        except exc.ValidationError as e:
            raise exc.LoanValidationError(
                f"Validation failed. Loan data doesn't match database file schema: {e}"
            )

        if not isinstance(validated_loan_data, dict):
            raise exc.LoanValidationError("Validated loan data is not a dictionary.")

        loan_id = validated_loan_data["loan_id"]

        for loan in current_data:
            if loan.get("loan_id") == loan_id:
                raise exc.LoanError(
                    f"Loan with ID: {loan_id} exists in the database. ID number must be unique value."
                )

        current_data.append(validated_loan_data)
        self.json_service.write_json_data(current_data)
        return f"Added new loan to data base with ID: {loan_id}."

    def get_all_loans_list(self):
        """Retrieve all loan records from the database.
        Returns:
            all_loans (list): List of all loan records.
        """
        current_data = self.json_service.load_json_file()
        all_loans = []

        for loan in current_data:
            if isinstance(loan, dict) and "loan_id" in loan:
                all_loans.append(loan)

        if not all_loans:
            raise exc.LoanNotFoundError("No loan found in the database.")

        return all_loans

    def update_loan_data(self, loan_id, field, new_value):
        """Update a specific field in a loan record.
        Args:
            loan_id (int): ID of the loan to update.
            field (str): The field to update.
            new_value: The new value to set for the specified field.
        Returns:
            str: Message with confirmation of success.
        """
        current_data = self.json_service.load_json_file()
        loan_id_found = False

        if loan_id is None:
            raise exc.ValidationError("Loan ID is missing or it's an empty value.")

        if field is None:
            raise exc.ValidationError(
                "The field value is missing or it's an empty value."
            )

        if new_value is None:
            raise exc.ValidationError(
                "New value to update loan data is missing or it's an empty value."
            )

        for loan in current_data:
            if loan.get("loan_id") == loan_id:
                if field not in loan:
                    raise exc.ValidationError(
                        f"The field '{field}' is missing in this loan record entry."
                    )

                loan[field] = new_value

                try:
                    self.json_service.validate_against_schema(loan, schema.loan_schema)
                except exc.ValidationError as e:
                    raise exc.LoanValidationError(
                        f"Validation failed while updating loan data: {e}"
                    )

                loan_id_found = True
                break

        if not loan_id_found:
            raise exc.LoanNotFoundError(
                f"Loan with ID: {loan_id} not found in database."
            )

        self.json_service.write_json_data(current_data)
        return f"New data value has been saved for loan with ID: {loan_id}"

    def delete_loan_data_from_file(self, loan_id):
        """Delete a loan record by its ID.
        Args:
            loan_id (int): ID of the loan to delete.
        Returns:
            str: Message with confirmation of success.
        """
        current_data = self.json_service.load_json_file()
        loan_deleted = False

        if loan_id is None:
            raise exc.ValidationError("Loan ID is missing or it's an empty value.")

        for loan in current_data:
            if loan.get("loan_id") == loan_id:
                current_data.remove(loan)
                loan_deleted = True
                break

        self.json_service.write_json_data(current_data)

        if not loan_deleted:
            raise exc.LoanNotFoundError(
                f"Loan with ID: {loan_id} could not be removed from the database."
            )

        return f"Loan record with ID {loan_id} has been deleted from database."

    # RESERVATION METHODS:

    def add_reservation_data(self, reservation_data):

        current_data = self.json_service.load_json_file()

        if not reservation_data:
            raise exc.ValidationError("Reservation data to add is missing.")

        if not isinstance(reservation_data, dict):
            raise exc.DataTypeError(
                "Reservation data type is incorrect. Reservation data must be a dict type."
            )

        try:
            validated_reservation_data = self.json_service.validate_against_schema(
                reservation_data, schema.reservation_schema
            )
        except exc.ValidationError as e:
            raise exc.ReservationValidationError(
                f"Validation failed. Reservation data doesn't match database file schema: {e}"
            )

        if not isinstance(validated_reservation_data, dict):
            raise exc.ValidationError("Validated reservation data is not a dictionary")

        reservation_id = validated_reservation_data["reservation_id"]

        for reservation in current_data:
            if reservation.get("reservation_id") == reservation_id:
                raise exc.ReservationError(
                    f"Reservation with ID: {reservation_id} exists in the database. ID must be unique value."
                )

        current_data.append(validated_reservation_data)
        self.json_service.write_json_data(current_data)

        return f"New reservation with ID: {reservation_id} has been created."

    def get_reservation_data(self):
        pass

    def get_all_reservation_list(self):
        pass

    def delete_reservation_data(self):
        pass
