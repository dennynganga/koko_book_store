from rest_framework import generics
from rest_framework import mixins

from books.models import Rental
from customers.models import Customer
from customers.serializers import CustomerSerializer, CustomerRentalSerializer


class CustomerList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    Used to retrieve a list of all customers
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustomerDetail(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    """
    Gets info on a particular customer, updates a customer
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CustomerRentalList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    Used to retrieve a list of a customer's rentals, or create a new one
    """

    serializer_class = CustomerRentalSerializer

    def get_queryset(self):
        customer_id = self.kwargs["pk"]
        return Rental.objects.filter(customer_id=customer_id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(customer_id=self.kwargs["pk"])
