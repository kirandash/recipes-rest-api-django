from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# always use gettext from translation utils for texts
# so in future texts can be translated
from django.utils.translation import gettext as _
from core import models


class UserAdmin(BaseUserAdmin):
    # order by id
    ordering = ['id']
    # show email and name in list view
    list_display = ['email', 'name']
    # Fieldsets for edit user page
    fieldsets = (
        # 4 sections
        # (title, {fields})
        (None, {'fields': ('email', 'password')}),
        # personal info section with name field
        (_('Personal Info'), {'fields': ('name',)}),
        # permissions section
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        # important dates section
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    # Fieldsets for Add user page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),  # always make sure to add a comma when there is one item in an obj
    )


# Register custom User model to UserAdmin
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
