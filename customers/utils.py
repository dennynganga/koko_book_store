from customers.models import Customer


def create_test_user(first_name, last_name):
    return Customer.objects.create(first_name=first_name, last_name=last_name)
