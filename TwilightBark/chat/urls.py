""" Define url patterns for chat """
from django.urls import path
from .views import room


# Set app_name connected to root directory's namespace
app_name = 'chat'

urlpatterns = [
    path('<room_name>/', room, name='room'),
]
