from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import Account

@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
        