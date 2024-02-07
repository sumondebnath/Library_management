from django.shortcuts import render
from django.views.generic import TemplateView
from book.models import Book
from category.models import Category

# Create your views here.


# Create your views here.
def home(request):
    book = Book.objects.all()
    return render(request, "core/index.html", {"book":book})


def home(request, category_slug = None):
    book = Book.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        book = Book.objects.filter(categories=category)
    categorie = Category.objects.all()
    return render(request, "core/index.html", {"books":book, "categories":categorie})