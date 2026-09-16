from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserAccount


@receiver(post_save, sender=User)
def create_user_account(sender, instance, raw=False, **kwargs):
    if raw:
        return  # skip during loaddata/fixture loading
    UserAccount.objects.get_or_create(user=instance)