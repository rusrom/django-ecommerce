from django.conf.urls import url
from .views import cart_home, cart_update, checkout_home, checkout_success


urlpatterns = [
    url(r'^$', cart_home, name='home'),
    url(r'^update/$', cart_update, name='update'),
    url(r'^checkout/$', checkout_home, name='checkout'),
    url(r'^checkout/success/$', checkout_success, name='checkout_success'),
]
