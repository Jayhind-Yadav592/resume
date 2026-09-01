"""
Admin configuration for billing and subscription models.
"""
from django.contrib import admin
from billing.models import SubscriptionPlan, Subscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'currency', 'scan_limit_per_month', 'is_active')
    list_filter = ('is_active', 'currency')
    search_fields = ('name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'plan',
        'status',
        'razorpay_order_id',
        'razorpay_payment_id',
        'started_at',
        'current_period_end',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'user__username',
        'user__email',
        'razorpay_order_id',
        'razorpay_payment_id',
    )
    readonly_fields = ('created_at',)
