from django.contrib import admin
from book.models import Book, BookReview, BorrowBooK
# Register your models here.
admin.site.register(Book)
admin.site.register(BookReview)
admin.site.register(BorrowBooK)