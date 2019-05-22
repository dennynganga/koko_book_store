from books.models import Book, Rental


def create_test_book(title, author, rental_status=Book.AVAILABLE):
    return Book.objects.create(title=title, author=author, rental_status=rental_status)


def create_test_rental(book, customer, date_borrowed):
    return Rental.objects.create(
        customer=customer, book=book, date_borrowed=date_borrowed
    )
