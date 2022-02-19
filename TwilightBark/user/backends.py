""" Customization of default user auth so user login is case-insensitive """
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CaseInsensitiveModelBackend(ModelBackend):
    """ Custom ModelBackend that allows case-insensitive user auth"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """ Override default method that returns user based on credentials """

        # Authenticate based on user model
        UserModel = get_user_model()
        if username is None:
            # Gets username based on email address
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            # If username is not None, try to get user object
            # Get user object based on username
            case_insensitive_username = f'{UserModel.USERNAME_FIELD}__iexact'
            user = (UserModel._default_manager
                    .get(**{case_insensitive_username: username}))
        except UserModel.DoesNotExist:
            # If can't find user, set password to password passed in
            UserModel().set_password(password)

        else:
            # If user found, check password and return specific user object
            if (user.check_password(password) and
               self.user_can_authenticate(user)):
                return user
