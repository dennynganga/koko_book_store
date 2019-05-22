from django.urls import path

from . import views

urlpatterns = [
    path("customers/", views.CustomerList.as_view(), name="customer_list"),
    path("customers/<int:pk>/", views.CustomerDetail.as_view(), name="customer_detail"),
    path(
        "customers/<int:pk>/rentals/",
        views.CustomerRentalList.as_view(),
        name="customer_rental_list",
    ),
]
