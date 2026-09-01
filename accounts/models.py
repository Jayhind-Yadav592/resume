"""
Custom User model and Developer API Key models for resumeforge.
"""
import secrets
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model supporting phone number and Pro subscription status.
    """
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Contact phone number with optional country code."
    )
    is_pro = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Flag indicating whether user has active Pro subscription."
    )
    pro_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Expiry timestamp for Pro subscription."
    )

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        return f"{self.username} ({self.email})" if self.email else self.username

    @property
    def has_active_pro(self) -> bool:
        """Returns True if the user is currently marked as pro and pro_expires_at has not passed."""
        if not self.is_pro:
            return False
        if self.pro_expires_at and self.pro_expires_at < timezone.now():
            return False
        return True


class DeveloperApiKey(models.Model):
    """
    Public Developer API Keys for automated ATS scoring and platform integration.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='api_keys',
        db_index=True
    )
    name = models.CharField(
        max_length=100,
        default="Default Production Key",
        help_text="Descriptive label for this API key."
    )
    key = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text="Secret API key token (rf_live_...)."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this API key is currently active."
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Developer API Key'
        verbose_name_plural = 'Developer API Keys'

    def __str__(self) -> str:
        return f"{self.name} ({self.key[:12]}...) - {self.user.username}"

    @classmethod
    def generate_for_user(cls, user, name="Default Production Key"):
        """Generates a secure random 32-byte hex key prefixed with rf_live_."""
        raw_key = f"rf_live_{secrets.token_hex(24)}"
        return cls.objects.create(user=user, name=name, key=raw_key)
