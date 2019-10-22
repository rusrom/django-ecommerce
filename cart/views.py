from django.shortcuts import render, redirect

from products.models import Product
from .models import Cart
from orders.models import Order
from billing.models import BillingProfile
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.models import Address
from addresses.forms import AddressForm


def cart_home(request):
    cart_instance, new_cart = Cart.objects.new_or_get(request)
    context = {
        'cart': cart_instance,
    }

    return render(request, 'cart/home.html', context)


def cart_update(request):
    product_id = request.POST.get('product_id')

    try:
        product_obj = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        print('Show message to user, product is gone!')
        return redirect('cart:home')

    cart_obj, new_cart = Cart.objects.new_or_get(request)

    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
    else:
        cart_obj.products.add(product_obj)
    request.session['cart_items'] = cart_obj.products.count()

    return redirect('cart:home')


def checkout_home(request):
    cart, new_cart = Cart.objects.new_or_get(request)

    # Check is cart new or cart empty
    if new_cart or not cart.products.count():
        return redirect('cart:home')

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_form = AddressForm()

    billing_profile, billing_created = BillingProfile.objects.new_or_get(request)

    order = None
    address_qs = None
    # if billing_profile and request.user.is_authenticated():
    if billing_profile:
        order, order_created = Order.objects.new_or_get(billing_profile, cart)
        address_qs = Address.objects.filter(billing_profile=billing_profile)

        shipping_address_id = request.session.get('shipping_address_id')
        billing_address_id = request.session.get('billing_address_id')

        if shipping_address_id:
            order.shipping_address = Address.objects.get(pk=shipping_address_id)
            request.session.pop('shipping_address_id', None)
            order.save()

        if billing_address_id:
            order.billing_address = Address.objects.get(pk=billing_address_id)
            request.session.pop('billing_address_id', None)
            order.save()

    # Check order complete or waiting
    if request.method == 'POST' and order.mark_as_new():
        request.session.pop('cart_items', None)
        request.session.pop('cart_id', None)
        return redirect('cart:checkout_success')

    context = {
        'billing_profile': billing_profile,
        'order': order,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'billing_form': billing_form,
        'address_qs': address_qs,
    }
    return render(request, 'cart/checkout.html', context)


def checkout_success(request):
    return render(request, 'cart/checkout_success.html')
