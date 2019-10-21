from django.conf.urls import url
from .views import checkout_address_create


urlpatterns = [
    url(r'^create/$', checkout_address_create, name='create'),
]
