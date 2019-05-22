from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book
from books.serializers import BookSerializer
from books.utils import create_test_book


class BookAPITest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(BookAPITest, cls).setUpClass()

        create_test_book(title="Black Leopard", author="Marlon", book_type=Book.FICTION)
        create_test_book(
            title="Intro to Python",
            author="Dennis",
            rental_status=Book.RENTED_OUT,
            book_type=Book.REGULAR,
        )
        create_test_book(
            title="City of Girls", author="Elizabeth", book_type=Book.NOVEL
        )

    def test_create_book(self):
        """
        Ensure a new book is created
        """
        create_book_url = reverse("book_list")

        book_info = {"title": "Gingerbread", "author": "Helen", "book_type": Book.NOVEL}

        response = self.client.post(create_book_url, data=book_info, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.get(pk=4).title, book_info["title"])
        self.assertEqual(Book.objects.get(pk=4).author, book_info["author"])

    def test_update_book_valid_payload(self):
        """
        Ensure a book is updated correctly
        """
        update_book_url = reverse("book_detail", kwargs={"pk": 1})

        payload = {"title": "Black Leopard, Red Wolf", "author": "Marlon"}

        response = self.client.put(update_book_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        book = Book.objects.get(pk=1)
        self.assertEqual(book.title, payload["title"])

    def test_update_book_invalid_payload(self):
        """
        Ensure a book is not updated if incorrect data is sent
        """
        update_book_url = reverse("book_detail", kwargs={"pk": 1})

        payload = {"author": "Arthur", "title": ""}

        response = self.client.put(update_book_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_books(self):
        """
        Ensure all books are returned
        """
        get_books_url = reverse("book_list")
        response = self.client.get(get_books_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get data from db
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.data, serializer.data)

        self.assertEqual(len(response.data), 3)

    def test_get_book(self):
        """
        Ensure correct book is returned
        """
        get_book_url = reverse("book_detail", kwargs={"pk": 2})
        response = self.client.get(get_book_url)

        book_expected_json = {
            "title": "Intro to Python",
            "author": "Dennis",
            "rental_status": "Rented Out",
            "book_type": "Regular",
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, book_expected_json)

    def test_get_non_existent_book_returns_404(self):
        """
        Ensures a 404 is returned when an invalid book ID is passed
        """
        get_book_url = reverse("book_detail", kwargs={'pk': 9000})
        response = self.client.get(get_book_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
