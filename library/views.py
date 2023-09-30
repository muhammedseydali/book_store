from django.utils import timezone
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView


from .filters import BookFilter
from .pagination import CustomPagination
from .models import Book, Track_book_status
from .serializers import BookSerializer, TrackBookStatusSerializer

class CreateBookAPIView(ListCreateAPIView):
    """
    API view for creating and listing books.

    This view allows authenticated users to create new book entries and
    list existing books. It supports filtering and pagination for
    efficient book retrieval.

    Permissions:
        - Requires authentication (users must be logged in).

    HTTP Methods:
        - GET: Retrieve a list of books with filtering and pagination.
        - POST: Create a new book entry """
    
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyBookAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting individual books.

    This view allows authenticated users to retrieve, update, and delete
    individual book entries based on their unique identifier (primary key).
     """

    filterset_class = BookFilter 
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class Show_books(generics.ListAPIView):
    """
    A view for listing books.

    This view returns a paginated list of books and supports filtering based on various criteria."""

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    # permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filterset_class = BookFilter 



class BorrowAPIView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filterset_class = BookFilter 
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Update the status of a borrowed book to mark it as returned and send an email confirmation.

        This view handles the PUT request to update the status of a borrowed book record.
        It checks if the book has already been returned and, if not, marks it as returned and
        sends an email confirmation to the user.
        """
        serializer = TrackBookStatusSerializer(data=request.data)

        if serializer.is_valid():
            book_name = serializer.validated_data.get('book_name')
            print(book_name, 'book name is here')

            try:
                book = Book.objects.get(title=book_name)
                
            except ObjectDoesNotExist:
                return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

            existing_borrow = Track_book_status.objects.filter(
                user=request.user,
                book=book,
                returned_date__isnull=True 
            ).first()

            if existing_borrow:
                return Response({'message': 'You have already borrowed this book.'}, status=status.HTTP_400_BAD_REQUEST)

            if book.total_available > 0:

                track_status = serializer.save(user=request.user , book=book.id)

                book.total_available -= 1

                book.save()

                subject = 'Book purchase Confirmation'
                message = f'The book "{track_status.book.title}" has been successfully purchased on {track_status.returned_date}.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email]

                # send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                response_data = {
                    'message': 'Book borrowed successfully.',
                    'borrowed_book': {
                        'title': track_status.book.title,
                        'author': track_status.book.author,
                        'borrowed_date': track_status.borrowed_date,
                        'return_date': track_status.returned_date,
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'The book is out of stock.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReturnAPIView(APIView):

    """
    Update the status of a borrowed book to mark it as returned and send an email confirmation.

    This view handles the PUT request to update the status of a borrowed book record.
    It checks if the book has already been returned and, if not, marks it as returned and
    sends an email confirmation to the user.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TrackBookStatusSerializer(data=request.data)

        if serializer.is_valid():
            book_name = serializer.validated_data.get('book_name')

            try:
                book = Book.objects.get(title=book_name)
            except ObjectDoesNotExist:
                return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

            borrow_record = Track_book_status.objects.filter(
                user=request.user,
                book=book,
                is_returned=False
            ).first()

            if not borrow_record:
                return Response({'error': 'You have not borrowed this book.'}, status=status.HTTP_400_BAD_REQUEST)

            borrow_record.is_returned = True
            borrow_record.returned_date = timezone.now()
            borrow_record.save()

            book.total_available += 1
            book.save()

            # Send an email confirmation to the user
            subject = 'Book Return Confirmation'
            message = f'The book "{book.title}" has been successfully returned on {borrow_record.returned_date}.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]

            # send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            response_data = {
                'message': 'Book returned successfully.',
                'returned_book': {
                    'title': book.title,
                    'author': book.author,
                    'returned_date': borrow_record.returned_date,
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class Borrowed_user(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filterset_class = BookFilter 
    permission_classes = [IsAuthenticated]

    def get(self, request):

        track_book_status = Track_book_status.objects.filter(user=request.user)

        serializer = TrackBookStatusSerializer(track_book_status, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)