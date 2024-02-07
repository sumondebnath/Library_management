from django.urls import path
from book.views import Detail_view, BorrowBookView

urlpatterns = [
    path("details/<int:id>/", Detail_view.as_view(), name="details"),
    path("borrow-book/<int:id>/", BorrowBookView, name="borrow_book"),
]