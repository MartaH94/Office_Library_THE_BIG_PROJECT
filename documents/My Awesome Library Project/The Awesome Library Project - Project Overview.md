==Status: DRAFT


BELOW IS THE: Module documentation
Technical Architecture Purpose

Why Python was chosen? 
I decided to use Python programming language due to my goal to develop my skills in programming. I chose the Python because it's widely used by programmers to analyze data, task automatization, creating web applications and it is also popular across Artificial Intelligence and Machine Learning tasks. 
My goal is to develop my skills in topics related with software development and Artificial Intelligence. This approach will help to create modern and efficient software. 

I use modular and OOP approach in that project. The application consists of 8 modules, each one is responsible for different logic. I decided to separate core logic to smaller modules to avoid huge files with mixed purposes and make it easier to maintain the application files. Writing the code in smaller pieces is also easier and will help me to maintain the code clean and review. 


# Architecture of "The BIG Library Project"

`database`
`documents`
`gui`
`models`
`program_data`
`services`
`tests`
`utils`

---
## `database`

This module provides a core logic for working with JSON files. The project has a JSON-base structure. It is made up of 5 python scripts:
1. `json_files_major_services.py`
2. `database_schemes.py`
3. `book_json_file_service.py`
4. `loan_json_file_service.py`
5. `user_json_file_service.py`

`json_files_major_services.py` - This file is designed to manage basic files operations in consistent, safe and schema-compliant approach. 
	It provides interface to:
	- load and save data 
	- validate records against a defined schema
	- add, update or delete data
	- generate backup files

`database_schemes.py` - This script defines the database schema. It holds parameters for users, books, book loans and reservations. Using the schema all records in the file will have the same set of parameters. 

`book_json_file_service.py` - This module provides a service for managing book data in JSON file. It is used to maintain the library's book collection in a consistent and safe way. It supports adding, retrieving, updating, and deleting book entries.

`loan_json_file_service.py` - This module provides a service for managing loans data in JSON file. It supports adding new loans, retrieving individual records, listing loans, updating loan details, and deleting loan entries. It is used to maintain the loans operations in a consistent and safe way.

`user_json_file_service.py` - This module provides a service for managing users data in JSON file. It offers simple helpers to load, add, query, update, and delete users. 


---
## `documents`

This module contains project related files and project documentation. 

---
## `gui`

In this module I store the Python scripts with code of the Graphic User Interface. 

---
## `models`

This module is made up of models widely used in the project. It holds model of book, loans and for users. This module supports and implements Object-Oriented Programming which is a basic approach in this application. 

Each model defines a class to represent and define the model. Also, each class representing the model includes a method to_dict() for converting the model object into a dictionary representation.

---
## `program_data`

In this module I placed all JSON files necessary for storing the project data. All operations designed in database module are implemented to operate on those files. This module contains 4 core JSON files to separate data related to program users, loans, and book data.

---
## `services`

This module is built to manage all crucial services of the Library application. I designed 4 service scripts in this module.

### `authorisation_service.py` 
This module script handles users authorization including login, logout and permissions checks.

### `book_service.py` 

The main role of this module is to encapsulate business logic related to books. It exposes clear methods for:

- Retrieving books (all or by specific criteria)
- Adding new books
- Updating book data
- Deleting books
- Searching and filtering books
- Managing book availability and borrowing status

By centralizing these operations, the module keeps the rest of the system simple and independent from storage details.

#### How It Works

The module is built around the `BookService` class, which interacts with:

- **`BookJsonFileService`** – handles low-level data storage and retrieval from a JSON file
- **`Book` model** – represents a book as a structured object
- **Custom exceptions (`exceptions`)** – ensure clear error handling and validation
- **Utility functions** (e.g. `generate_book_id`) – support operations like ID generation

The service:
1. Retrieves raw data from the JSON service
2. Validates input parameters and business rules
3. Converts data into `Book` objects when needed
4. Executes operations (add, update, delete, search)
5. Raises meaningful exceptions when something goes wrong

#### Structure

The `BookService` class is organized into several logical groups of methods:

1. **Core operations**
    - `get_all_books`, `get_book_by_id`
    - `add_book`, `update_book_data`, `delete_book`
    
2. **Existence checks**
    - `book_exists_by_id`, `ensure_book_exists`
    
3. **Search and filtering**
    - `get_books_by_keyword`
    - `get_books_by_year`
    - `get_books_by_category`
    
4. **Availability and status**
    - `is_book_available`
    - `get_available_books`
    - `mark_book_as_borrowed`


#### Key Characteristics

- **Separation of concerns** – business logic is separated from data storage
- **Validation-first approach** – all inputs are validated before processing
- **Explicit error handling** – uses custom exceptions for clarity and control
- **Simple persistence model** – relies on a JSON-based storage service
- **Readable and maintainable design** – methods are small and focused

### `loan_service.py`

This module is prepared for managing loan operations like borrowing, returning, viewing loans, checking books availability etc.


### `user_service.py`

The module encapsulates business logic related to users and exposes methods for:

- Adding new users
- Retrieving users by different criteria (ID, username, email)
- Updating user data and attributes
- Validating user existence
- Managing user status, roles, and login information

By centralizing user-related operations, it simplifies interaction with the data layer and enforces consistent rules across the system.

#### How It Works

The module is built around the `UserService` class, which collaborates with:

- **`UsersJsonFileService`** – handles storage and retrieval of user data from a JSON file
- **`User` model** – represents user data as structured objects
- **Custom exceptions (`exceptions`)** – provide clear and explicit error handling
- **Helper utilities** (e.g. `validate_email`) – ensure correctness of input data
- **Predefined roles (`valid_roles`)** – enforce allowed user roles

The service performs the following steps:

1. Retrieves raw user data from the storage layer
2. Validates input parameters and business rules (e.g. email format, role validity)
3. Converts data into `User` objects when needed
4. Executes CRUD and update operations
5. Raises meaningful exceptions when invalid operations are detected


#### Structure

The `UserService` class is organized into logical groups of methods:

1. **Core operations**
    - `add_user`, `get_all_users`

2. **Search and retrieval**
    - `get_user_by_id`
    - `get_user_by_username`
    - `get_user_by_email`

3. **Existence checks**
    - `user_exists_by_username`
    - `user_exists_by_email`
    - `ensure_user_exists`

4. **User data updates**
    - `update_user_data`
    - `update_user_role`
    - `update_user_status`
    - `update_last_login_date`

5. **Utility operations**
    - `delete_user`

6. **Helper methods**
    - `get_user_role`
    - `is_user_active`
    - `get_user_profile`

#### Key Characteristics

- **Separation of concerns** – business logic is independent of storage implementation
- **Validation-focused design** – ensures correctness of input data before processing
- **Explicit error handling** – uses custom exceptions for predictable behavior
- **Simple data persistence** – relies on JSON-based storage
- **Clear and readable structure** – methods are logically grouped and easy to understand

---
## `tests`

This module is dedicated to tests designed to perform required tests during software manufacturing. Tests are important part of software development. I split tests to prepare test service scripts that are stored in services directory. 

On first stage I planned unit test for module database. I prepared unit tests for 4 modules which are responsible for core activities on json files.






---
## `utils`

This module is designed to be supportive module for the program. Inside utils module I prepare 3 scripts with configuration, helpers and validators widely used in the application. 



Data & Core Logic Purpose




---
---


Documentation draft
##### Overview:
*Give a quick, high-level understanding of the project.* 
Checklist: 
- [ ] Project name 
- [x] description (what it is) 
- [x] Short paragraph explaining the main idea 
- [x] Primary goal of the application 
- [ ] Who this project is for 
- [ ] Current project status (idea / prototype / MVP / in progress) 
- [ ] Link to key sections (Problem, Users, How it Works) 

Guiding questions: 
• Why does it exist? 
• Who should care about it?


---
##### Problem & Motivation Purpose: 
*Explain why the project exists.* 
Checklist: 
- [ ] Description of the real-world problem 
- [ ] Who is affected by this problem 
- [ ] How the problem is handled today 
- [ ] Why existing solutions are insufficient 
- [ ] What happens if the problem is not solved 

Guiding questions: 
• What pain point triggered this project? 
• What is inefficient, confusing, or missing today? 
• Why is this problem worth solving?


---
##### Scope & Capabilities Purpose: 
*Define clear boundaries of the project.* 
Checklist: 
- [ ] List of core features (what the app does) 
- [ ] Explicit list of non-goals (what the app does NOT do) 
- [ ] Assumptions made during design 
- [ ] Known constraints (technical or conceptual) 
- [ ] High-level future ideas (optional) 

Guiding questions: 
• What problems does this project solve? 
• What problems does it intentionally ignore? 
• What should users NOT expect?


---
##### Users & Use Cases Purpose: 
*Show how real people interact with the system.* 
Checklist: 
- [ ] Description of each user type 
- [ ] Main goals of each user type 
- [ ] 3–5 key use cases written as short stories 
- [ ] Expected outcome for each use case 
- [ ] Use case template: User wants to:\ Because:\ The application does:\ Result: 

Guiding questions: 
• Who uses the app? 
• What do they want to achieve? 
• What does “success” look like for them?


---
##### How It Works (High-Level) Purpose: 
*Explain the system without technical details.* 
Checklist:
- [ ] List of main system components 
- [ ] Description of how components interact 
- [ ] Data flow explained in simple terms 
- [ ] One simple diagram (optional but recommended) 

Guiding questions: 
• What are the main building blocks? 
• How does information move through the system? 
• How would I explain this to a non-technical person?

---
##### Technical Architecture Purpose: 
*Explain technical design decisions clearly.* 
Checklist: 
- [x] Why Python was chosen 
- [ ] High-level structure of the codebase 
- [ ] Key modules and their responsibilities 
- [ ] Important architectural decisions 
- [ ] Trade-offs and alternatives considered 

Guiding questions: 
• Why is the system built this way? 
• What problems does the architecture solve? 
• What did you deliberately avoid?

---
##### Data & Core Logic Purpose: 
*Describe what the system knows and how it thinks.* 
Checklist: 
- [ ] Types of data handled by the application 
- [ ] Source of the data 
- [ ] How data is stored or managed 
- [ ] Key business rules / logic 
- [ ] Error handling at a conceptual level 

Guiding questions: 
• What information is essential for the app? 
• How is data transformed or processed? 
• What rules control system behavior?

---
##### Limitations & Future Purpose: 
*Be transparent and professional.* 
Checklist: 
- [ ] Known limitations of the current version 
- [ ] Technical or conceptual risks 
- [ ] What the project cannot currently support 
- [ ] Ideas for future improvements 
- [ ] Open questions or uncertainties 

Guiding questions: 
• What are the weak points today? 
• What would you improve next? 
• What assumptions might change?


`database`
`documents`
`gui`
`models`
`program_data`
`services`
`tests`
`utils`