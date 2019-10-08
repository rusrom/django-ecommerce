from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from django.contrib.auth import authenticate, login, get_user_model

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail


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
        if user:
            login(request, user)

            # Clear guest_email_id if user logedin
            request.session.pop('guest_email_id', False)

            # if request.session.get('guest_email_id'):
            # if 'guest_email_id' in request.session:
            #     del request.session['guest_email_id']

            # Redirect to success page
            redirect_url = request.GET.get('next') or request.POST.get('next')
            if is_safe_url(redirect_url, request.get_host()):
                return redirect(redirect_url)
            return redirect('/')
            # Clear form after submiting
            # context['form'] = LoginForm()
        else:
            # Return an invalid login error message
            print('Fail')
    return render(request, 'accounts/login.html', context)


def guest_register(request):
    form = GuestForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data.get('email')
        guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = guest_email.id

        redirect_url = request.GET.get('next') or request.POST.get('next')

        if is_safe_url(redirect_url, request.get_host()):
            return redirect(redirect_url)

    # Return an invalid guest login error message
    print('Fail checkout as Guest redirect to Register Form')
    return redirect('register')


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

    return render(request, 'accounts/register.html', context)
