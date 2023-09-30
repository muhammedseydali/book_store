from django.urls import path

from .views import RetrieveUpdateDestroyBookAPIView, CreateBookAPIView, ListCreateAPIView, Show_books, BorrowAPIView, Borrowed_user, ReturnAPIView




urlpatterns = [
    path('create_book/', CreateBookAPIView.as_view()),
    path('list_books/', Show_books.as_view()),
    path("retreive_books/<int:pk>/",RetrieveUpdateDestroyBookAPIView.as_view()),
    path('borrow_book/', BorrowAPIView.as_view()),
    path('return_book/',ReturnAPIView.as_view()),
    path('borrowed_users/',Borrowed_user.as_view()),

]

