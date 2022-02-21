""" Classes for creating forms """
from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import authenticate
from user.models import User


class RegistrationForm(UserCreationForm):
    """ Modify default UserCreationForm to include email """

    email = forms.EmailField(max_length=255, help_text='Require valid email address.')

    class Meta:
        """ Define basic meta data for form - what model to use, what fields to use """
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        """ """
        email = self.cleaned_data['email'].lower()
        try:
            # [email] raises error while .get(email) does not
            user = User.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email} already exists.')

    def clean_username(self):
        """ """
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f'Username {username} already exists.')