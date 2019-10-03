from django.shortcuts import render, redirect

from products.models import Product
from .models import Cart
from orders.models import Order
from billing.models import BillingProfile
from accounts.forms import LoginForm


# def cart_create(request, user=None):
#     print('New cart instance created')
#     cart_instance = Cart.objects.create(user=user)
#     request.session['cart_id'] = cart_instance.id
#     return cart_instance


def cart_home(request):
    cart_instance, new_cart = Cart.objects.new_or_get(request)
    context = {
        'cart': cart_instance,
    }

    # products = cart_instance.products.all()
    # total = sum([product.price for product in products])


    # user = request.user if request.user.is_authenticated() else None
    # cart_id = request.session.get('cart_id')

    # if cart_id:
    #     # CartID exists
    #     qs = Cart.objects.filter(id=cart_id)
    #     if qs.exists():
    #         cart_instance = qs.first()
    #         # Update user but keep CartID after login
    #         if request.user.is_authenticated() and cart_instance.user is None:
    #             cart_instance.user = request.user
    #             cart_instance.save()
    #     print('CartID:', cart_instance.id)
    # else:
    #     # No cart exists
    #     # cart_instance = cart_create(request)
    #     cart_instance = Cart.objects.new_cart(user)
    #     request.session['cart_id'] = cart_instance.id

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
    if new_cart or not cart.products.count():
        return redirect('cart:home')

    user = request.user
    billing_profile = None
    if user.is_authenticated():
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
            user=user,
            email=user.email
        )


    order, new_order = Order.objects.get_or_create(cart=cart)
    login_form = LoginForm()

    context = {
        'billing_profile': billing_profile,
        'order': order,
        'login_form': login_form,
    }
    return render(request, 'cart/checkout.html', context)
