"""
URL routing for billing, subscriptions, and Razorpay endpoints.
"""
from django.urls import path
from billing.views import (
    SubscriptionPlansView,
    CurrentSubscriptionView,
    CreateOrderView,
    VerifyPaymentView,
    RazorpayWebhookView,
)

urlpatterns = [
    path('plans/', SubscriptionPlansView.as_view(), name='billing-plans'),
    path('my-subscription/', CurrentSubscriptionView.as_view(), name='billing-my-subscription'),
    path('create-order/', CreateOrderView.as_view(), name='billing-create-order'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='billing-verify-payment'),
    path('webhook/', RazorpayWebhookView.as_view(), name='billing-webhook'),
]
