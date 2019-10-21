from django.db import models

from django.db.models.signals import post_save
from django.conf import settings

from accounts.models import GuestEmail


User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')

        # Init billing_profile - Anonymous User
        billing_profile = None
        created = False

        # Authenticated user
        if user.is_authenticated():
            # billing_profile, created = BillingProfile.objects.get_or_create(
            # billing_profile, created = self.get_queryset().get_or_create(
            billing_profile, created = self.model.objects.get_or_create(
                user=user,
                email=user.email
            )

        # Guest user
        if guest_email_id:
            guest = GuestEmail.objects.get(id=guest_email_id)
            # billing_profile, created = BillingProfile.objects.get_or_create(
            # billing_profile, created = self.get_queryset().get_or_create(
            billing_profile, created = self.model.objects.get_or_create(
                email=guest.email
            )

        return billing_profile, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = BillingProfileManager()

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
