'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''
import random
import string
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """

    slug = new_slug if new_slug else slugify(instance.title)

    qs = instance.__class__.objects.filter(slug=slug)
    if qs.exists():
        randstr = random_string_generator(size=4)
        new_slug = f'{slug}-{randstr}'
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_order_id_generator(instance):
    order_id = random_string_generator()

    qs = instance.__class__.objects.filter(order_id=order_id)
    if qs.exists():
        return unique_order_id_generator(instance)
    return order_id
