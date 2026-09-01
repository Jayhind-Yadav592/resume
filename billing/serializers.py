"""
Serializers for subscription plans, order creation, and payment verification.
"""
from rest_framework import serializers
from billing.models import SubscriptionPlan, Subscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = (
            'id',
            'name',
            'price',
            'currency',
            'scan_limit_per_month',
            'features',
            'is_active',
        )
        read_only_fields = fields


class SubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.ReadOnlyField(source='plan.name')

    class Meta:
        model = Subscription
        fields = (
            'id',
            'plan',
            'plan_name',
            'razorpay_order_id',
            'razorpay_payment_id',
            'status',
            'started_at',
            'current_period_end',
            'created_at',
        )
        read_only_fields = fields


class CreateOrderSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField(required=True)


class CreateOrderResponseSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    amount = serializers.IntegerField()
    currency = serializers.CharField()
    key_id = serializers.CharField()
    plan_name = serializers.CharField()
    subscription_id = serializers.IntegerField()


class VerifyPaymentSerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField(required=True)
    razorpay_payment_id = serializers.CharField(required=True)
    razorpay_signature = serializers.CharField(required=True)


class VerifyPaymentResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    subscription = SubscriptionSerializer()
