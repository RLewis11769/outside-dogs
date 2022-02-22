""" Defines what each page looks like - matches url to html file """
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, UserAuthenticationForm
from .models import User
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


def user_account(request, *args, **kwargs):
    """ Displays user account page - different for own page and other users """
    context = {}
    # Get id of user whose account is being viewed (own account or other user)
    user_id = kwargs.get('user_id')
    try:
        # Try to get user based on id
        account = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse(f'Account does not exist for user {user_id}')
    if account:
        # If successfully get user, get context to pass to template
        context['id'] = account.id
        context['email'] = account.email
        context['username'] = account.username
        context['profile_pic'] = account.profile_pic.url
        context['hide_email'] = account.hide_email

        # Define state (is it my account or someone else's, etc)
        # Default is true (my account)
        is_self = True
        # Get user who is viewing account/making request
        user = request.user
        # If user and account are different, viewing someone else's account
        if user.is_authenticated and user != account:
            is_self = False
        # If user is not logged in, obvs viewing someone else's account
        elif not user.is_authenticated:
            is_self = False
        # Set is_self in context
        context['is_self'] = is_self

        return render(request, 'user/account.html', context)
