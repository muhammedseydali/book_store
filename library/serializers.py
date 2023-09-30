
from rest_framework import serializers

from .models import Book, Track_book_status
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class BookSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'
        exlude = ['creator']

    def get_creator_name(self, obj):
        return f"{obj.creator.username}"



class TrackBookStatusSerializer(serializers.ModelSerializer):

    book_name = serializers.CharField(write_only=True) 
    user = UserSerializer(read_only=True)

    class Meta:
        model = Track_book_status
        fields = ['user', 'book_name', 'borrowed_date', 'due_date', 'returned_date']
        
    def validate_book_name(self, value):
        print('inside validate book name')
        try:
            book = Book.objects.get(title=value)
            print(book, 'book name in serializer')
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found.")
        return book

    def create(self, validated_data):
        # Use the validated book instance
        book = validated_data['book_name']
        book = Book.objects.get(title=book)
        track_status = Track_book_status.objects.create(
            user=validated_data['user'],
            book=book,
            borrowed_date=validated_data.get('borrowed_date'),
            due_date=validated_data.get('due_date')
        )
        return track_status






