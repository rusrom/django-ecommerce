from django.db import models

from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed

from products.models import Product


User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        user = request.user if request.user.is_authenticated() else None
        cart_id = request.session.get('cart_id')
        if cart_id:
            qs = self.get_queryset().filter(id=cart_id)
            # CartID exists in Django
            if qs.exists():
                cart_instance = qs.first()
                # Update user but keep CartID after login
                if request.user.is_authenticated() and cart_instance.user is None:
                    cart_instance.user = request.user
                    cart_instance.save()
                return cart_instance, False

        # Create cart
        cart_instance = self.new_cart(user)
        request.session['cart_id'] = cart_instance.id
        return cart_instance, True

    def new_cart(self, user=None):
        print(user, '|', type(user))
        return self.model.objects.create(user=user)


class Cart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cart_created = models.DateTimeField(auto_now_add=True)
    cart_changed = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_reciever(sender, instance, action, *args, **kwargs):
    # print(action)
    if action in ['post_add', 'post_remove', 'post_clear']:
        products = instance.products.all()
        instance.subtotal = sum([product.price for product in products])
        instance.save()

m2m_changed.connect(receiver=m2m_changed_cart_reciever, sender=Cart.products.through)


def pre_save_cart_reciever(sender, instance, *args, **kwargs):
    instance.total = float(instance.subtotal) * 1.02

pre_save.connect(receiver=pre_save_cart_reciever, sender=Cart)
