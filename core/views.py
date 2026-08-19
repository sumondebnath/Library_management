from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from book.models import Book
from category.models import Category


def home(request, category_slug=None):
    books = Book.objects.all()
    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        books = Book.objects.filter(categories=category)
    categories = Category.objects.all()
    return render(request, "core/index.html", {"books": books, "categories": categories})


def Health_Check(request):
    return JsonResponse({"status": "ok", "message": "Library Management System is running smoothly."})