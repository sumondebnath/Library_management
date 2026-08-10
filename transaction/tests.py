from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from transaction.models import Transaction


class DepositTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("reader", "reader@example.com", "StrongPass123!")

    def test_deposit_requires_login(self):
        response = self.client.get(reverse("deposite"))
        self.assertEqual(response.status_code, 302)

    def test_deposit_increases_balance_and_creates_transaction(self):
        self.client.login(username="reader", password="StrongPass123!")
        response = self.client.post(reverse("deposite"), {"amount": "250.50"})
        self.assertEqual(response.status_code, 302)
        self.user.account.refresh_from_db()
        self.assertEqual(self.user.account.balance, 250.50)
        txn = Transaction.objects.get(account=self.user.account)
        self.assertEqual(txn.amount, 250.50)
        self.assertEqual(txn.balance_after_borrowed, 250.50)

    def test_deposit_negative_amount_rejected(self):
        self.client.login(username="reader", password="StrongPass123!")
        response = self.client.post(reverse("deposite"), {"amount": "-5"})
        self.assertEqual(response.status_code, 200)
        self.user.account.refresh_from_db()
        self.assertEqual(self.user.account.balance, 0)
        self.assertFalse(Transaction.objects.filter(account=self.user.account).exists())
