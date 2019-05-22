from books.models import Book, Rental


def create_test_book(title, author, book_type, rental_status=Book.AVAILABLE):
    return Book.objects.create(
        title=title, author=author, rental_status=rental_status, book_type=book_type
    )


def create_test_rental(book, customer, date_borrowed):
    return Rental.objects.create(
        customer=customer, book=book, date_borrowed=date_borrowed
    )
