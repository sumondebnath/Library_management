from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserAccount

# Create your models here.

class Transaction(models.Model):
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    amount= models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    balance_after_borrowed = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    on_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["on_date"]