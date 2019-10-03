from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm


def home_page(request):
    # return HttpResponse('Hello world!')
    context = {
        'page_title': 'Home Page',
        'content': 'Welcome to the Home page',
    }
    if request.user.is_authenticated():
        context['premium_content'] = 'YEEEEH'
    return render(request, 'home_page.html', context)


def about_page(request):
    context = {
        'page_title': 'About Page',
        'content': 'Boom from the About page'
    }
    return render(request, 'about/about.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'page_title': 'Contact Page',
        'content': 'Our contact',
        'form': contact_form,
    }
    # if request.method == 'POST':
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))
    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    return render(request, 'contact/view.html', context)
