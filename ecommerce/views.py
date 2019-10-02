from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm, LoginForm, RegisterForm


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


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'page_title': 'Login Page',
        'form': form,
    }
    # print('User loged in:', request.user.is_authenticated())
    if form.is_valid():
        # print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # How to login user:
        # https://docs.djangoproject.com/en/2.2/topics/auth/default/#how-to-log-a-user-in
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to success page
            return redirect('/')
            # # Clear form after submiting
            # context['form'] = LoginForm()
        else:
            # Return an invalid login error message
            print('Fail')
    return render(request, 'auth/login.html', context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'page_title': 'Register Form',
        'form': form,
    }

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        User = get_user_model()
        new_user = User.objects.create_user(username, email, password)

    return render(request, 'auth/register.html', context)
