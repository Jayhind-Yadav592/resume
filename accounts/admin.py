"""
Admin customization for User model.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model."""
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'is_pro',
        'pro_expires_at',
        'is_staff',
        'date_joined',
    )
    list_filter = ('is_pro', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-date_joined',)

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            _('Pro Subscription & Profile'),
            {
                'fields': (
                    'phone_number',
                    'is_pro',
                    'pro_expires_at',
                )
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            _('Additional Info'),
            {
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'phone_number',
                    'is_pro',
                    'pro_expires_at',
                )
            },
        ),
    )
