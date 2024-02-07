from django.db import models
from django.contrib.auth.models import User
from accounts.constants import GENDER_TYPE, USER_TYPE

# Create your models here.
class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE)
    initial_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to="accounts/media/profile/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"