""" TwilightBark URL Configuration

The 'urlpatterns' list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import index


# Anything after domain name is sent here
# Anything after urlpattern is sent to urls.py page referenced
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    # namespace is used to define/indiviudalize urls
    # Referenced in templates as {% url 'namespace:url_name' %}
    path('chat/', include('chat.urls', namespace='chat')),
    path('user/', include('user.urls', namespace='user')),

    # Password reset/confirm views (auto-generated by Django)
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='user/password/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='user/password/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='user/password/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='user/password/password_reset_confirm.html'),
         name='password_reset_confirm'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Add media files to search path (as seen in settings.py)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
