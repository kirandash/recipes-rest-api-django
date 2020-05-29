from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models


class UserAdmin(BaseUserAdmin):
    # order by id
    ordering = ['id']
    # show email and name in list view
    list_display = ['email', 'name']


# Register custom User model to UserAdmin
admin.site.register(models.User, UserAdmin)
