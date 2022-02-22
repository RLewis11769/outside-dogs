""" Defines classes for forms """
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from user.models import User


class RegistrationForm(UserCreationForm):
    """ Modify default UserCreationForm to include email """

    email = forms.EmailField(max_length=255,
                             help_text='Require valid email address.')

    class Meta:
        """ Define basic metadata for form - what model and fields to use """
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        """ Override form's clean method to validate email input """
        email = self.cleaned_data['email'].lower()
        try:
            # Try to get user with that email - if can, raise error
            user = User.objects.get(email=email)
        except Exception as e:
            # If no user with that email found, return email
            return email
        raise forms.ValidationError(f'Email {email} already exists.')

    def clean_username(self):
        """ Override form's clean method to validate username input """
        username = self.cleaned_data['username']
        try:
            # Try to get user with that username - if can, raise error
            user = User.objects.get(username=username)
        except Exception as e:
            # If no user with that username found, return username
            return username
        raise forms.ValidationError(f'Username {username} already exists.')


class UserAuthenticationForm(forms.ModelForm):
    """ Define form for user authentication """
    # widget handles rendering - password widget obscures input
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        """ Defines what model and what fields form uses """
        model = User
        fields = ('email', 'password')

    def clean(self):
        """ Validate email and password (defined in settings.py) """
        if self.is_valid():
            # Get cleaned data from form
            email = self.cleaned_data['email']
            pw = self.cleaned_data['password']
            # No need to return - just raise error if can't authenticate
            if not authenticate(email=email, password=pw):
                raise forms.ValidationError('Invalid email or password')
