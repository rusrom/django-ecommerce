from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404

from .models import Product
from cart.models import Cart


class ProductFeaturedListView(ListView):
    # Default template is: 'product/product_list.html'
    template_name = 'products/list.html'

    # (*) Using custom Model Manager
    def get_queryset(self, *args, **kwargs):
        # To get a request
        # request = self.request
        # print('Request info from custom Model Manager of ProductListView(ListView) class:', request)

        # return Product.objects.featured()

        # Using Custom QuerySet from models
        return Product.objects.all().featured()


class ProductFeaturedDetailView(DetailView):
    # Default template is: 'products/product_detail.html'
    template_name = 'products/featured-detail.html'

    # (*) Using custom Model Manager
    def get_queryset(self, *args, **kwargs):
        # return Product.objects.featured()

        # Using Custom QuerySet from models
        return Product.objects.all().featured()


class ProductListView(ListView):
    # (1)
    # model = Product

    # (2)
    # or make queryset instead using model = Product above)
    # queryset = Product.objects.all()

    # Default template is: 'product/product_list.html'
    template_name = 'products/list.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     context['tyty'] = 432342342
    #     print(context)
    #     return context

    # (3*) Using custom Model Manager
    def get_queryset(self, *args, **kwargs):
        # To get a request
        request = self.request
        print('Request info from custom Model Manager of ProductListView(ListView) class:', request)

        return Product.objects.all()


# Equvivalent to above class ProductListView
def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset,
    }
    return render(request, 'products/list.html', context)


class ProductDetailSlugView(DetailView):
    template_name = 'products/detail.html'
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cart'] = Cart.objects.new_or_get(self.request)
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404('Product with such slug not found')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        return instance

    # Such variant of get_object() above can catch MultipleObjectsRetuned Exeption
    # def get_object(self, *args, **kwargs):
    #     slug = self.kwargs.get('slug')
    #     instance = get_object_or_404(Product, slug=slug, active=True)
    #     return instance


class ProductDetailView(DetailView):
    # (1)
    # model = Product

    # (2)
    # or make queryset instead using model = Product above)
    # queryset = Product.objects.all()

    # Default template is: 'products/product_detail.html'
    template_name = 'products/detail.html'

    # Hack to view context inside terminal after request)
    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
    #     context['tyty'] = 432342342
    #     print(context)
    #     return context

    # (3.1*) Using custom Model Manager from .models
    def get_object(self, *args, **kwargs):
        # To get a request
        # request = self.request
        # print('Request info from custom Model Manager of ProductDetailView(DetailView) class:', request)

        pk = self.kwargs.get('pk')

        # Using custom Model Manager from .models - objects.get_by_id(id)
        instance = Product.objects.get_by_id(id=pk)
        if instance is None:
            raise Http404('Product does not exist or has several instances)')
        return instance

    # (3.2*) Using custom Model Manager from .models (USING get_queryset() method LIKE IN ProductListView(ListView) Class above)
    # def get_queryset(self, *args, **kwargs):
    #     # To get a request
    #     # request = self.request
    #     # print('Request info from custom Model Manager of ProductListView(ListView) class:', request)

    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(id=pk)


# Equvivalent to above class ProductListView
def product_detail_view(request, pk):
    # (1)
    # instance = Product.objects.get(pk=pk)

    # (2)
    # try:
    #     instance = Product.objects.get(pk=pk)
    # except Product.DoesNotExist:
    #     raise Http404('Product does not exist')
    # except:
    #     print('Huh?')

    # (3)
    # qs = Product.objects.filter(pk=pk)
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404('Product does not exist')

    # (4*) Using Custom Model Manager from .models
    instance = Product.objects.get_by_id(id=pk)
    # if not instance:
    if instance is None:
        raise Http404('Product does not exist or has several instances)')

    # (5)
    # instance = get_object_or_404(Product, pk=pk)

    context = {
        'object': instance,
    }
    return render(request, 'products/detail.html', context)
