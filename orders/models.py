from django.db import models
from django.db.models.signals import pre_save, post_save

from cart.models import Cart
from ecommerce.utils import unique_order_id_generator
from billing.models import BillingProfile

from decimal import Decimal


ORDER_STATUS_CHOICES = (
    ('new', 'New'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('shipped', 'Shipped'),
    ('closed', 'Closed'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True)
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart)
    status = models.CharField(max_length=20, default='new', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)

    def update_total(self):
        print('>>> self.cart.total >>>', type(self.cart.total))
        print('>>> self.shipping_total >>>', type(self.shipping_total))
        self.total = Decimal(self.cart.total) + Decimal(self.shipping_total)
        self.save()

    def __str__(self):
        return self.order_id


# Generate the order ID
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)


# Generate the order TOTAL
def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart = instance
        qs = Order.objects.filter(cart__id=cart.id)
        if qs.count() == 1:
            order = qs.first()
            order.update_total()
post_save.connect(post_save_cart_total, Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    print('running post_save_order')
    if created:
        print('Updating first ...')
        instance.update_total()
post_save.connect(post_save_order, sender=Order)
