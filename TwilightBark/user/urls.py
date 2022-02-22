""" Match URLs to views for user app """
from django.urls import path
from .views import register_user, login_user, logout_user


# Anything after user/ redirects here
# When using {% url 'name' %} in templates, matches name here
urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
]
