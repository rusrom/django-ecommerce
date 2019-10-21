from django.db import models

from billing.models import BillingProfile


ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=120, default='Dominican Rupublic')
    region = models.CharField(max_length=120)
    city = models.CharField(max_length=120, default='Santa Domingo')
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    gate = models.CharField(max_length=10, null=True, blank=True)
    floor = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.billing_profile)
