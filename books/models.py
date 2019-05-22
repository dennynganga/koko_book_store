from django.db import models
from django.utils import timezone

from customers.models import Customer
from koko_book_store.constants import PRICE_PER_DAY_RENTAL


class Book(models.Model):
    AVAILABLE = 0
    RENTED_OUT = 1

    AVAILABILITY_STATUS = ((AVAILABLE, "Available"), (RENTED_OUT, "Rented Out"))

    REGULAR = "R"
    FICTION = "F"
    NOVEL = "N"

    BOOK_TYPES = ((REGULAR, "Regular"), (FICTION, "Fiction"), (NOVEL, "Novel"))

    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)

    book_type = models.CharField(max_length=2, choices=BOOK_TYPES, default=REGULAR)

    rental_status = models.IntegerField(choices=AVAILABILITY_STATUS, default=AVAILABLE)

    # timestamps
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "books"

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        return self.rental_status == self.AVAILABLE


class Rental(models.Model):

    ACTIVE = 0
    CLOSED = 1

    RENTAL_STATUS = ((ACTIVE, "Active"), (CLOSED, "Closed"))

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rental_status = models.IntegerField(choices=RENTAL_STATUS, default=ACTIVE)

    # timestamps
    date_borrowed = models.DateTimeField(default=timezone.now)
    date_returned = models.DateTimeField(null=True)

    amount_charged = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "rentals"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.book.rental_status = Book.RENTED_OUT
            self.book.save(update_fields=["rental_status"])

        # also check if date_returned is available
        # if available, calculate charge
        if self.date_returned and not self.amount_charged:
            delta = self.date_returned - self.date_borrowed
            # assuming it was borrowed in the morning and returned by evening :)
            rental_days = delta.days or 1

            # logic for charges, depending on book type
            # might need some more love later - maybe store charges to make system more
            # robust so that users can configure prices on their own

            self.amount_charged = (
                PRICE_PER_DAY_RENTAL[self.book.book_type] * rental_days
            )

            self.rental_status = self.CLOSED

        super(Rental, self).save()
