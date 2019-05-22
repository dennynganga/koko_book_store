"""koko_book_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

from books import views as books_views
from customers import views as customer_views

schema_view = get_swagger_view(title="Koko Book Store API")

urlpatterns = [
    path("admin/", admin.site.urls),
    # books endpoints
    path("books/", books_views.BookList.as_view(), name="book_list"),
    path("books/<int:pk>/", books_views.BookDetail.as_view(), name="book_detail"),
    path("books/<int:pk>/", books_views.BookDetail.as_view(), name="book_detail"),
    path(
        "rentals/<int:pk>/close/",
        books_views.RentalClose.as_view(),
        name="close_rental",
    ),
    # customers endpoints
    path("customers/", customer_views.CustomerList.as_view(), name="customer_list"),
    path(
        "customers/<int:pk>/",
        customer_views.CustomerDetail.as_view(),
        name="customer_detail",
    ),
    path(
        "customers/<int:pk>/rentals/",
        customer_views.CustomerRentalList.as_view(),
        name="customer_rental_list",
    ),
    # api docs
    path("", schema_view),
]
