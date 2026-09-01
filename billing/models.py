"""
Models for Subscription Plans and User Subscriptions.
"""
from django.conf import settings
from django.db import models


class SubscriptionPlan(models.Model):
    """
    Tiered subscription plan definitions (e.g. Free Tier, Pro Monthly, Pro Annual).
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Plan name (e.g. Pro Monthly, Free Starter)."
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price in standard currency units (e.g. 499.00 INR)."
    )
    currency = models.CharField(
        max_length=10,
        default='INR'
    )
    scan_limit_per_month = models.IntegerField(
        default=3,
        help_text="Number of scans allowed per month (-1 indicates unlimited)."
    )
    features = models.JSONField(
        default=list,
        blank=True,
        help_text="List of feature bullet points for this plan."
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['price']
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'

    def __str__(self) -> str:
        return f"{self.name} - {self.currency} {self.price}"


class Subscription(models.Model):
    """
    User subscription record tracking Razorpay order, payment, and validity period.
    """
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        db_index=True
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )
    razorpay_subscription_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    razorpay_order_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True
    )
    razorpay_payment_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='created',
        db_index=True
    )
    started_at = models.DateTimeField(
        null=True,
        blank=True
    )
    current_period_end = models.DateTimeField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self) -> str:
        return f"Subscription #{self.id} - {self.user.username} ({self.plan.name}) [{self.status}]"
