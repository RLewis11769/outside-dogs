""" Defines fields, methods, etc for form classess """
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):
    """ Modify default UserCreationForm to include email """

    # Adding this field to default fields
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
        except User.DoesNotExist:
            # If no user with that email found, return email
            return email
        raise forms.ValidationError(f'Email {email} already exists.')

    def clean_username(self):
        """ Override form's clean method to validate username input """
        username = self.cleaned_data['username']
        try:
            # Try to get user with that username - if can, raise error
            user = User.objects.get(username=username)
        except User.DoesNotExist:
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


class AccountUpdateForm(forms.ModelForm):
    """ Define form for updating user account """

    class Meta:
        model = User
        # These are fields that can be updated
        fields = ('username', 'email', 'profile_pic', 'hide_email')

    def clean_email(self):
        """ Override form's clean method to validate email input """
        email = self.cleaned_data['email'].lower()
        try:
            # Try to get user with that email - if can, raise error
            # exclude current user so won't get error if stays the same
            user = User.objects.exclude(id=self.instance.id).get(email=email)
        except User.DoesNotExist:
            # If no user with that email found, return email
            return email
        raise forms.ValidationError(f'Email {email} already exists.')

    def clean_username(self):
        """ Override form's clean method to validate username input """
        username = self.cleaned_data['username']
        try:
            # Try to get user with that username - if can, raise error
            # exclude current user so won't get error if doesn't change
            user = (User.objects.exclude(id=self.instance.id)
                    .get(username=username))
        except User.DoesNotExist:
            # If no user with that username found, return username
            return username
        raise forms.ValidationError(f'Username {username} already exists.')

    def save(self, commit=True):
        """ Override default save method to update user's profile settings """
        # Get existing data from db but don't save yet
        user = super(AccountUpdateForm, self).save(commit=False)
        # Update with new cleaned data
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email'].lower()
        # profile_pic is working in admin but not account_update frontend
        user.profile_pic = self.cleaned_data['profile_pic']
        user.hide_email = self.cleaned_data['hide_email']
        # commit=True is default, so will be committing to db
        if commit:
            # Now that changes are committed, save to db
            user.save()
        return user
