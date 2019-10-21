from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import AddressForm
from billing.models import BillingProfile


def checkout_address_create(request):
    form = AddressForm(request.POST or None)

    if form.is_valid():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

        if billing_profile:
            instance = form.save(commit=False)
            instance.billing_profile = billing_profile
            instance.address_type = request.POST.get('address_type', 'shipping')
            instance.save()

            request.session[instance.address_type + '_address_id'] = instance.id

            redirect_url = request.GET.get('next') or request.POST.get('next')

            if is_safe_url(redirect_url, request.get_host()):
                return redirect(redirect_url)

    return redirect('cart:checkout')
