""" Define admin interface for user app """
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User


class AccountAdmin(UserAdmin):
    """ Define which User fields shown and how displayed in /admin panel """
    list_display = ('email', 'username', 'date_joined', 'is_admin')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined')

    # Required fields to override
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register User model in admin panel with AccountAdmin structure
admin.site.register(User, AccountAdmin)
