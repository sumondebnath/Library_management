from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from book.models import Book, BorrowBooK


class BorrowBookTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("reader", "reader@example.com", "StrongPass123!")
        self.book = Book.objects.create(title="The Book", description="desc", borrowed_price="100.00")

    def test_borrow_requires_login(self):
        response = self.client.get(reverse("borrow_book", args=[self.book.id]))
        self.assertEqual(response.status_code, 302)

    def test_borrow_allows_exact_balance(self):
        self.user.account.balance = 100
        self.user.account.save()
        self.client.login(username="reader", password="StrongPass123!")
        response = self.client.get(reverse("borrow_book", args=[self.book.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BorrowBooK.objects.filter(borrowUser=self.user, borrowBook=self.book).exists())
        self.user.account.refresh_from_db()
        self.assertEqual(self.user.account.balance, 0)

    def test_borrow_rejected_when_balance_too_low(self):
        self.user.account.balance = 50
        self.user.account.save()
        self.client.login(username="reader", password="StrongPass123!")
        response = self.client.get(reverse("borrow_book", args=[self.book.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BorrowBooK.objects.filter(borrowUser=self.user, borrowBook=self.book).exists())
        self.user.account.refresh_from_db()
        self.assertEqual(self.user.account.balance, 50)

    def test_cannot_borrow_same_book_twice(self):
        self.user.account.balance = 300
        self.user.account.save()
        BorrowBooK.objects.create(borrowUser=self.user, borrowBook=self.book)
        self.client.login(username="reader", password="StrongPass123!")
        self.client.get(reverse("borrow_book", args=[self.book.id]))
        self.assertEqual(BorrowBooK.objects.filter(borrowUser=self.user, borrowBook=self.book).count(), 1)
        self.user.account.refresh_from_db()
        self.assertEqual(self.user.account.balance, 300)


class ReviewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("reader", "reader@example.com", "StrongPass123!")
        self.book = Book.objects.create(title="The Book", description="desc", borrowed_price="100.00")

    def test_authenticated_user_can_review(self):
        self.client.login(username="reader", password="StrongPass123!")
        response = self.client.post(
            reverse("details", args=[self.book.id]),
            {"name": "Reader", "review": "Great book!"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.book.reviews.count(), 1)

    def test_invalid_review_shows_errors(self):
        self.client.login(username="reader", password="StrongPass123!")
        response = self.client.post(
            reverse("details", args=[self.book.id]),
            {"name": "", "review": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.book.reviews.count(), 0)
        self.assertContains(response, "This field is required")
