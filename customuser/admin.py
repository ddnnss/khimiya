from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User,Guest


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password', 'used_promo')}),
        (_('Personal info'), {'fields': ('name', 'family', 'otchestvo', 'country',
                                         'city', 'post_code', 'phone', 'passport',
                                         'address', 'comment', 'is_allow_email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone'),
        }),
    )
    list_display = ('email', 'name', 'family', 'otchestvo', 'phone')

    ordering = ('email',)
    search_fields = ('email', 'name', 'family','phone')

admin.site.register(Guest)