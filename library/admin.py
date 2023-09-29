from django.contrib import admin
from .models import Book,Track_book_status

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'year_of_publication', 'total_available', 'created_at', 'updated_at', 'creator')
    list_display_links = ('id','title','author')
    search_fields = ('id', 'title', 'author', 'category', 'year_of_publication')

class TrackBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'borrowed_date', 'due_date', 'returned_date', 'is_returned')
    list_display_links = ('id','book','borrowed_date')
    search_fields = ('id', 'book')


admin.site.register(Book, BookAdmin)
admin.site.register(Track_book_status, TrackBookAdmin)
