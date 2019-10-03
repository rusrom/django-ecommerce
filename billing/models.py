from django.db import models

from django.db.models.signals import post_save
from django.conf import settings


User = settings.AUTH_USER_MODEL


class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


# def billing_profile_created_reciever(sender, instance, created, *args, **kwargs):
#     if created:
#         print('ACTUAL API REQUEST: Send to Stripe/Braintree')
#         instance.customer_id = newID
#         instance.save()


def user_created_reciever(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)
post_save.connect(user_created_reciever, sender=User)
