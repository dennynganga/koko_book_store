from rest_framework import serializers

from books.models import Book, Rental
from koko_book_store.constants import CURRENCY


class BookSerializer(serializers.ModelSerializer):
    rental_status = serializers.CharField(
        source="get_rental_status_display", read_only=True
    )

    class Meta:
        model = Book
        fields = ("title", "author", "rental_status")


class CloseRentalSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField()
    rental_status = serializers.CharField(source="get_rental_status_display")

    class Meta:
        model = Rental
        fields = ("amount_charged", "currency", "rental_status", "date_returned")
        read_only_fields = ("amount_charged", "currency", "rental_status")

    def get_currency(self, obj):
        return CURRENCY
