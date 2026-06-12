# book class with atrbutes and methods


class Book:
    def __init__(
        self,
        author: str,
        title: str,
        publication_year: int,
        isbn: int,
        category: list,
        language: str,
    ):
        self.book_id = None
        self.author = author
        self.title = title
        self.publication_year = publication_year

        self.isbn = isbn
        self.category = category
        self.language = language

        self.book_status = "available"
        self.borrower_id = None
        self.due_date = None
        self.last_loan_date = None

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "author": self.author,
            "title": self.title,
            "publication_year": self.publication_year,
            "isbn": self.isbn,
            "category": self.category,
            "language": self.language,
            "book_status": self.book_status,
            "borrower_id": self.borrower_id,
            "due_date": self.due_date,
            "last_loan_date": self.last_loan_date,
        }


class BookCategory:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)
