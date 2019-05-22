from rest_framework import generics
from rest_framework import mixins

from books.models import Book, Rental
from books.serializers import BookSerializer, CloseRentalSerializer


class BookList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        """
        Used to retrieve a list of all books
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Creates a new book
        """
        return self.create(request, *args, **kwargs)


class BookDetail(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        """
        Gets info on a particular book
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Updates a book's info
        """
        return self.update(request, *args, **kwargs)


class RentalClose(mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    Closes a rental. Simply, a book is returned to the store.
    """

    queryset = Rental.objects.all()
    serializer_class = CloseRentalSerializer

    def put(self, request, *args, **kwargs):
        # update book as available
        book = self.get_object().book
        book.rental_status = Book.AVAILABLE
        book.save(update_fields=["rental_status"])

        return self.partial_update(request, *args, **kwargs)
