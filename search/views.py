from django.shortcuts import render
from django.views.generic.list import ListView

from products.models import Product


class SearchListView(ListView):

    # (1)
    # model = Product

    # (2)
    # or make queryset instead using model = Product above)
    # queryset = Product.objects.all()

    # Default template is: 'product/product_list.html'
    template_name = 'search/list.html'

    # (3*) Using custom Model Manager
    def get_queryset(self, *args, **kwargs):
        search_query = self.request.GET.get('q')
        if search_query:
            # return Product.objects.filter(title__icontains=search_query)
            # or using Custom Model Manager
            return Product.objects.search(search_query)
        return Product.objects.none()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['test'] = 'Sherihot!'
        return context
