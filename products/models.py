from django.db.models import Q
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save

import os.path
import re

from ecommerce.utils import unique_slug_generator


def upload_image_path(instance, filename):
    '''Rename image as product title
    and save to static_cdn/media_root/products
    '''
    # print(instance)
    # print(type(instance))
    # print(filename)

    new_filename = re.sub(r'\s+', '-', instance.title.lower())
    extension = os.path.splitext(filename)[1]
    return 'products/' + new_filename + extension


# (*) Create custom QuerySet instead of default - objects.all()
class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True, active=True)

    def active(self):
        return self.filter(active=True)

    def search(self, search_query):
        lookups = (
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tag__title__icontains=search_query)
        )
        return self.filter(lookups).distinct()


# (*) Create custom Model Manager instead of default manager - objects
class ProductManager(models.Manager):
    # Overide get_queryset() using new custom QuerySet - ProductQuerySet
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    # Create new method for model manager in order to extend its functionality
    def featured(self):  # Product.objects.featured()
        # Using default QuerySet
        # return self.get_queryset().filter(featured=True)

        # Using Custom QuerySet featured
        return self.get_queryset().featured()

    # Create new method for model manager in order to extend its functionality
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)  # Product.onjects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, search_query):
        return self.get_queryset().active().search(search_query)


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, default=29.99)
    # document = models.FileField(upload_to='products/', null=True, blank=True)
    # document = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # (*) Use custom Model Manager
    # This is not overide the defaults, just extends
    objects = ProductManager()

    def get_absolute_url(self):
        # return f'/products/{self.slug}'
        # Improved version and more powerfull)
        return reverse('products:detail_slug', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


# Use Signal for slug sield before saving product
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver, sender=Product)
