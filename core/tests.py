from django.test import TestCase
from django.urls import reverse

from book.models import Book
from category.models import Category


class HomeTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Python", slug="python-programming")
        self.book = Book.objects.create(title="The Book", description="desc", borrowed_price="100.00")
        self.book.categories.add(self.category)

    def test_home_lists_books(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Book")

    def test_category_filter(self):
        response = self.client.get(reverse("book", args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Book")

    def test_invalid_category_returns_404(self):
        response = self.client.get(reverse("book", args=["does-not-exist"]))
        self.assertEqual(response.status_code, 404)
