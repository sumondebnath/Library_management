from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import UserAccount
from book.models import Book, BorrowBooK
from category.models import Category


class RegistrationTests(TestCase):
    def test_registration_creates_user_and_account(self):
        response = self.client.post(reverse("register"), {
            "username": "reader",
            "first_name": "Test",
            "last_name": "User",
            "email": "reader@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "birth_date": "2000-01-01",
            "gender": "Male",
            "user_type": "Student",
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="reader")
        self.assertEqual(user.account.balance, 0)
        self.assertEqual(user.account.gender, "Male")

    def test_registration_requires_email(self):
        response = self.client.post(reverse("register"), {
            "username": "noemail",
            "first_name": "Test",
            "last_name": "User",
            "email": "",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "birth_date": "2000-01-01",
            "gender": "Male",
            "user_type": "Student",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="noemail").exists())


class UserAccountSignalTests(TestCase):
    def test_user_created_outside_registration_gets_account(self):
        user = User.objects.create_user("staffuser", "staff@example.com", "StrongPass123!")
        self.assertTrue(UserAccount.objects.filter(user=user).exists())
        self.assertIsNotNone(user.account)


class ProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("reader", "reader@example.com", "StrongPass123!")

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)

    def test_profile_page_renders(self):
        self.client.login(username="reader", password="StrongPass123!")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Borrowed Books")


class ReturnBookTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner", "owner@example.com", "StrongPass123!")
        self.other = User.objects.create_user("other", "other@example.com", "StrongPass123!")
        Category.objects.create(name="Test", slug="test")
        self.book = Book.objects.create(title="The Book", description="desc", borrowed_price="100.00")

    def test_user_cannot_return_another_users_book(self):
        borrow = BorrowBooK.objects.create(borrowUser=self.owner, borrowBook=self.book)
        owner_balance = self.owner.account.balance
        self.client.login(username="other", password="StrongPass123!")
        response = self.client.get(reverse("return", args=[borrow.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(BorrowBooK.objects.filter(id=borrow.id).exists())
        self.owner.account.refresh_from_db()
        self.assertEqual(self.owner.account.balance, owner_balance)

    def test_return_credits_balance_and_deletes_borrow(self):
        self.owner.account.balance = 200
        self.owner.account.save()
        borrow = BorrowBooK.objects.create(borrowUser=self.owner, borrowBook=self.book)
        self.client.login(username="owner", password="StrongPass123!")
        response = self.client.get(reverse("return", args=[borrow.id]))
        self.assertEqual(response.status_code, 302)
        self.owner.account.refresh_from_db()
        self.assertEqual(self.owner.account.balance, 300)
        self.assertFalse(BorrowBooK.objects.filter(id=borrow.id).exists())
