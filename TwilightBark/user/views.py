""" Defines what each page looks like - matches url to html file """
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, UserAuthenticationForm
from .utils import get_redirect_destination


def register_user(request, *args, **kwargs):
    """ Registers new user into db with new account """
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'You are already logged in as {user.email}')

    context = {}
    if request.POST:
        # Create new form instance and populate with data from request
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # is_valid() does type checking, etc on fields in form
            form.save()
            # Gets email and password from form
            email = form.cleaned_data.get('email').lower()
            pw = form.cleaned_data.get('password1')
            # Gets user based on email and password
            user = authenticate(email=email, password=pw)
            # Logs user in
            login(request, user)
            # Redirects to correct page (whether 'next' or index)
            destination = get_redirect_destination(request)
            if destination:
                return redirect(destination)
            return redirect('index')
        else:
            # If form is not valid, return and display form with errors
            context['registration_form'] = form
    # Render form (either blank or with errors)
    return render(request, 'user/register.html', context)


def logout_user(request):
    """ Logs out user """
    logout(request)
    return redirect('index')


def login_user(request, *args, **kwargs):
    """ Logs in user """
    user = request.user
    # If user is already logged in, no need to login so just redirect
    if user.is_authenticated:
        return redirect('index')

    context = {}
    if request.POST:
        # Create new form instance and populate with data from request
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            # is_valid() 'cleans' aka type checks and validates input
            email = request.POST['email'].lower()
            pw = request.POST['password']
            # Gets user based on email and password
            user = authenticate(email=email, password=pw)
            if user:
                # Logs user in and redirects to correct page
                login(request, user)
                destination = get_redirect_destination(request)
                if destination:
                    return redirect(destination)
                return redirect('index')
        else:
            # If form is not valid, return and display form with errors
            context['login_form'] = form
    # Render form (either blank with {} context or with errors)
    return render(request, 'user/login.html', context)
