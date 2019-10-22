from django.db import models
from django.db.models.signals import pre_save, post_save

from addresses.models import Address
from cart.models import Cart
from ecommerce.utils import unique_order_id_generator
from billing.models import BillingProfile

from decimal import Decimal


ORDER_STATUS_CHOICES = (
    ('waiting', 'Waiting'),
    ('new', 'New'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('closed', 'Closed'),
    ('refunded', 'Refunded'),
)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart):
        qs = self.get_queryset().filter(
            cart=cart,
            billing_profile=billing_profile,
            status='waiting',
            active=True,
        )

        if qs.exists():
            order = qs.first()
            created = False
        else:
            order = self.model.objects.create(
                cart=cart,
                billing_profile=billing_profile,
            )
            created = True
        return order, created


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True)
    order_id = models.CharField(max_length=120, blank=True)
    shipping_address = models.ForeignKey(
        Address,
        related_name='shipping_address',
        null=True,
        blank=True
    )
    billing_address = models.ForeignKey(
        Address,
        related_name='billing_address',
        null=True,
        blank=True
    )
    cart = models.ForeignKey(Cart)
    status = models.CharField(max_length=20, default='waiting', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)

    objects = OrderManager()

    def update_total(self):
        self.total = Decimal(self.cart.total) + Decimal(self.shipping_total)
        self.save()

    def check_done(self):
        if self.billing_profile and self.shipping_address and self.billing_address and self.total > 0:
            return True

    def mark_as_new(self):
        if self.check_done():
            self.status = 'new'
            self.save()
            return True
        # return self.status

    def __str__(self):
        return self.order_id


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

    prev_order = Order.objects.filter(
        cart=instance.cart,
        active=True
    ).exclude(
        billing_profile=instance.billing_profile
    )
    if prev_order.exists():
        prev_order.update(active=False)
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
