""" Match URLs to views for user app """
from django.urls import path
from . import views as v


urlpatterns = [
    path('register/', v.register, name='register'),
]
