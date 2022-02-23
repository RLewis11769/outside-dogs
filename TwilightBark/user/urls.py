""" Match URLs to views for user app """
from django.urls import path
from .views import (register_user, login_user, logout_user,
                    user_account, edit_account)


# Define name which links to namespace in TwilightBark/urls.py
app_name = 'user'

# Name used in templates as {% url 'user:url_name' %}
# If didn't include namespace, would be {% url 'url_name' %}
urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('<user_id>/', user_account, name='account'),
    path('<user_id>/edit/', edit_account, name='edit'),
]
