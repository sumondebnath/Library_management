from django.db import models
from django.contrib.auth.models import User
from category.models import Category
from book.constants import RATING
from accounts.models import UserAccount

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    book_image= models.ImageField(upload_to="book/media/images/", null=True, blank=True)
    description = models.TextField()
    borrowed_price = models.DecimalField(max_digits=6, decimal_places=2)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)

    class Meta:
        ordering = ["borrowed_date"]

    def __str__(self):
        return self.title
    

class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=50)
    review = models.TextField()
    created = models.DateTimeField(auto_now_add=True)



class BorrowBooK(models.Model):
    borrowUser = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    borrowBook = models.ForeignKey(Book, on_delete= models.CASCADE)
    borrowDate = models.DateTimeField(auto_now_add=True)