# basic settings of the project like file paths, database parameters, etc.

import json
import os
from pathlib import Path

CONFIG_FILE_DIRECTORY = Path(__file__).parent.resolve()
JSON_FILES_DIRECTORY = CONFIG_FILE_DIRECTORY / "program_data"
JSON_FILES_DIRECTORY.mkdir(
    exist_ok=True
)  # If the catalog (program_data) exists, no action needed.

LOANS_LIST_FILE_PATH = JSON_FILES_DIRECTORY / "list_of_loans.json"
RESERVATIONS_LIST_FILE_PATH = JSON_FILES_DIRECTORY / "list_of_reservations.json"
PROGRAM_USERS_FILE_PATH = JSON_FILES_DIRECTORY / "program_users.json"
SINGLE_USER_LOANS_FILE_PATH = JSON_FILES_DIRECTORY / "single_user_history.json"
THE_LIBRARY_FILE_PATH = JSON_FILES_DIRECTORY / "the_awesome_library.json"

BACKUP_FILES_DIRECTORY = Path(__file__).resolve().parent.parent / "program_data_backups"

PROJECT_ALIAS = "library_copy"
