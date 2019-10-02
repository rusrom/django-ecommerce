from django.conf.urls import url

from .views import (
    ProductListView,
    ProductDetailView,
    ProductDetailSlugView,
    # product_list_view,
    # product_detail_view,
    # ProductFeaturedListView,
    # ProductFeaturedDetailView,
)

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    # url(r'^products-fbv/$', product_list_view, name='products_fbv'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail_slug'),
    # url(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view, name='detail_fbv'),
    # url(r'^featured/$', ProductFeaturedListView.as_view(), name='featured'),
    # url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view(), name='featured_detail'),
]
