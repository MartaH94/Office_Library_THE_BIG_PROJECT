# managing loan operations like: borrow, return, view loans, check book availability

"""
Wypożyczenia:
- wypożycz książkę
- zwróć książkę
- przedłuż wypożyczenie (opcjonalnie)


Rezerwacje:
- zarezerwuj książkę
- anuluj rezerwację
- zatwierdź rezerwację (librarian/admin)
- pobierz listę rezerwacji


Status książki:
- sprawdzenie czy książka jest dostępna
- sprawdzenie kto wypożyczył książkę
- sprawdzenie czy użytkownik ma aktywne wypożyczenie


Powiązanie z userem:
- przypisywanie książek do usera
- historia wypożyczeń usera


Integracja z auth
sprawdzanie permission:
- borrow_book
- return_book
- reserve_book
- cancel_reservation
- approve_reservations



"""

from models.book import Book
from services.book_service import BookService
from models.user import User
from services.authorisation_service import UserAuthorisation
import exceptions as exc


class LoanService:
    def __init__(
        self,
        user_id,
        book_id,
        borrow_date,
        return_date,
        borrowed_by,
        authorisation: UserAuthorisation,
    ):
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.borrowed_by = borrowed_by
        self.authorisation = authorisation

    def loan_book(self):
        pass
        # this method is not done yet. I need manage JSON files first.
        # self.logged_user = User(user_id=self.user_id)
        # self.authorisation.login()

        # # if self.logged_user not in users:

        # if not self.logged_user:
        #     raise exc.UserError("User is not logged into system.")

        # self.book_to_loan = Book()
        # self.authorisation.check_permission("borrow_book")

        # user_permission = False

        # if self.logged_user: # if logged user permission is true
        #     BookService.is_book_available(book=self.book_to_loan)

    def return_book(self):
        self.authorisation.check_permission("return_book")
        pass

    def reserve_book(self):
        self.authorisation.check_permission("book_the_book")
        pass
