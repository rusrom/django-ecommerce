from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import AddressForm
from .models import Address
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


def checkout_address_reuse(request):
    # if not request.user.is_authenticated():
    #     return redirect('login')

    if request.method == 'POST':
        address_type = request.POST.get('address_type')
        address_id = request.POST.get('address_id')

        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

        if address_id:
            qs = Address.objects.filter(billing_profile=billing_profile, id=address_id)
            if qs.exists():
                request.session[address_type + '_address_id'] = address_id

                redirect_url = request.GET.get('next_url') or request.POST.get('next_url')

                if is_safe_url(redirect_url, request.get_host()):
                    return redirect(redirect_url)

    return redirect('cart:checkout')
