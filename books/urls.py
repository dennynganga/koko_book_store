from django.urls import path

from . import views

urlpatterns = [
    path("books/", views.BookList.as_view(), name="book_list"),
    path("books/<int:pk>/", views.BookDetail.as_view(), name="book_detail"),
    path("books/<int:pk>/", views.BookDetail.as_view(), name="book_detail"),
    path("rentals/<int:pk>/close/", views.RentalClose.as_view(), name="close_rental"),
]
