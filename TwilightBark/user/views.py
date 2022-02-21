""" """
# from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from user.forms import RegistrationForm
# from django.contrib.auth.forms import UserCreationForm


# Note: csrf is only excluded if not rendering anything (HttpResponse)
# @csrf_exempt
def register(request, *args, **kwargs):
    """ """
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
            email = form.cleaned_data.get('email').lower()
            pw = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=pw)
            login(request, user)
            destination = kwargs.get('next')
            if destination:
                return redirect(destination)
            return redirect('index')
        else:
            # If form not valid, return and display form with errors
            context['registration_form'] = form

    return render(request, 'register.html', context)
