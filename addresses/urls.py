from django.conf.urls import url
from .views import checkout_address_create, checkout_address_reuse


urlpatterns = [
    url(r'^create/$', checkout_address_create, name='create'),
    url(r'^reuse/$', checkout_address_reuse, name='reuse'),
]
