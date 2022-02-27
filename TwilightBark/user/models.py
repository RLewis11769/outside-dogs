""" Define User models for basic user and admin user """
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    """ Define custom user manager """

    def create_user(self, email, username, password=None):
        """ Create new user """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        # Create user object with email, username, and password
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        # Can set password as here or in create_superuser - same thing
        # Note that password is optional for user creation
        user.set_password(password)
        # Save user object to database
        user.save(using=self.db)
        return user

    def create_superuser(self, email, username, password):
        """ If user is defined as superuser, create user """
        """ Only superuser/admin can use admin panel """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        # Superuser has all permissions
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """ Defines user model to override default django user model """
    """ Logging in with email rather than username """

    email = models.EmailField(verbose_name="email", max_length=60,
                              unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined',
                                       auto_now_add=True)
    profile_pic = models.ImageField(max_length=200,
                                    upload_to='profile_images', blank=True,
                                    default='default_pic.png')
    hide_email = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # Required fields to override AbstractBaseUser class
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # When logging into admin, override to use email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Link to custom user manager above
    objects = AccountManager()

    def get_profile_pic_filename(self):
        """ Return user-defined profile pic name that is default overridden """
        # Take everything from profile_pic field after profile_images/id
        return (str(self.profile_pic)[str(self.profile_pic)
                .index(f'profile_images/{self.id}/'):])

    # These are more default methods that need to be overridden
    def __str__(self):
        """ When type {user}, prints username rather than address """
        return self.username

    def has_perm(self, perm, obj=None):
        """ Checks if user has specific permission """
        return self.is_admin

    def has_module_perms(self, app_label):
        """ Checks if user has permission to view app at all """
        return True
