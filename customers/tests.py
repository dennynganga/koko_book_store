from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book
from books.utils import create_test_book, create_test_rental
from customers.models import Customer
from customers.serializers import CustomerSerializer
from customers.utils import create_test_user
from koko_book_store.constants import CURRENCY


class CustomerAPITest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(CustomerAPITest, cls).setUpClass()

        # create test customers
        cls.user1 = create_test_user(first_name="Dennis", last_name="Wainaina")
        cls.user2 = create_test_user(first_name="Veronica", last_name="Ajiambo")
        cls.user3 = create_test_user(first_name="Liam", last_name="Wainaina")
        cls.user4 = create_test_user(first_name="Olivia", last_name="Wanjiku")

        # create test books
        cls.book1 = create_test_book(title="Black Leopard", author="Marlon", book_type=Book.NOVEL)
        cls.book2 = create_test_book(title="City of Girls", author="Elizabeth", book_type=Book.FICTION)
        cls.book3 = create_test_book(title="Intro to Python", author="Dennis", book_type=Book.REGULAR)

        # create some test rentals too
        cls.rental = create_test_rental(
            book=cls.book3,
            customer=cls.user1,
            date_borrowed="2019-05-15 00:00:00.400952+00:00",
        )

    def test_create_customer(self):
        """
        Ensure a new customer is created
        """
        create_customer_url = reverse("customer_list")

        customer_info = {"first_name": "Denny", "last_name": "Wayne"}

        response = self.client.post(
            create_customer_url, data=customer_info, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 5)
        self.assertEqual(Customer.objects.get(pk=5).first_name, "Denny")
        self.assertEqual(Customer.objects.get(pk=5).last_name, "Wayne")

    def test_update_customer_valid_payload(self):
        """
        Ensure a customer is updated correctly
        """
        update_customer_url = reverse("customer_detail", kwargs={"pk": 1})

        payload = {"first_name": "Dennis", "last_name": "Ng'ang'a", "is_active": True}

        response = self.client.put(update_customer_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        customer = Customer.objects.get(pk=1)
        self.assertEqual(customer.last_name, "Ng'ang'a")

    def test_update_customer_invalid_payload(self):
        """
        Ensure a customer is not updated if incorrect data is sent
        """
        update_customer_url = reverse("customer_detail", kwargs={"pk": 1})

        payload = {"first_name": "Dennis", "last_name": "", "is_active": True}

        response = self.client.put(update_customer_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_customers(self):
        """
        Ensure all customers are returned
        """
        get_customers_url = reverse("customer_list")
        response = self.client.get(get_customers_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get data from db
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        self.assertEqual(response.data, serializer.data)

        self.assertEqual(len(response.data), 4)

    def test_get_customer(self):
        """
        Ensure correct customer is returned
        """
        get_customer_url = reverse("customer_detail", kwargs={"pk": 2})
        response = self.client.get(get_customer_url)

        customer_expected_json = {
            "first_name": "Veronica",
            "last_name": "Ajiambo",
            "is_active": True,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, customer_expected_json)

    def test_create_customer_rental(self):
        """
        Ensure a rental for a book is created for a customer
        """
        create_rental_url = reverse(
            "customer_rental_list", kwargs={"pk": self.user1.pk}
        )

        data = {"book": self.book1.pk}
        response = self.client.post(create_rental_url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_rental_with_unavailable_book(self):
        """
        Ensure that a book can't be rented out if not available
        """
        create_rental_url = reverse(
            "customer_rental_list", kwargs={"pk": self.user1.pk}
        )

        data = {"book": self.book3.pk}
        response = self.client.post(create_rental_url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_charge_correct_for_novel_after_close(self):
        """
        Ensure charges for novel rentals are accurate
        """
        rental = create_test_rental(
            book=self.book1,
            customer=self.user1,
            date_borrowed="2019-05-15 00:00:00.400952+00:00",
        )
        close_rental_url = reverse("close_rental", kwargs={"pk": rental.pk})

        data = {"date_returned": "2019-05-25 13:46:57.249145+03:00"}
        response = self.client.put(close_rental_url, data=data, format="json")

        self.assertEqual(response.data["amount_charged"], "15.00")
        self.assertEqual(response.data["rental_status"], "Closed")
        self.assertEqual(response.data["currency"], CURRENCY)

    def test_charge_correct_for_regular_after_close(self):
        """
        Ensure charges for regular rentals are accurate
        """
        rental = create_test_rental(
            book=self.book1,
            customer=self.user1,
            date_borrowed="2019-05-25 00:00:00.400952+00:00",
        )
        close_rental_url = reverse("close_rental", kwargs={"pk": rental.pk})

        data = {"date_returned": "2019-05-25 13:46:57.249145+03:00"}
        response = self.client.put(close_rental_url, data=data, format="json")

        self.assertEqual(response.data["amount_charged"], "1.50")
        self.assertEqual(response.data["rental_status"], "Closed")
        self.assertEqual(response.data["currency"], CURRENCY)

    def test_charge_correct_for_fiction_after_close(self):
        """
        Ensure charges for fiction rentals are accurate
        """
        rental = create_test_rental(
            book=self.book1,
            customer=self.user1,
            date_borrowed="2019-05-22 00:00:00.400952+00:00",
        )
        close_rental_url = reverse("close_rental", kwargs={"pk": rental.pk})

        data = {"date_returned": "2019-05-25 13:46:57.249145+03:00"}
        response = self.client.put(close_rental_url, data=data, format="json")

        self.assertEqual(response.data["amount_charged"], "4.50")
        self.assertEqual(response.data["rental_status"], "Closed")
        self.assertEqual(response.data["currency"], CURRENCY)
