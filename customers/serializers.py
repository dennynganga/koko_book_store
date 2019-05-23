from rest_framework import serializers

from books.models import Rental
from customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("first_name", "last_name", "is_active")


class CustomerRentalSerializer(serializers.ModelSerializer):
    rental_status = serializers.CharField(
        source="get_rental_status_display", read_only=True
    )
    book_title = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = Rental
        fields = ("book", "customer_id", "rental_status", "book_title")

    def validate_book(self, book):
        if book.is_available:
            return book
        else:
            raise serializers.ValidationError("Book is unavailable")
