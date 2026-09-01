"""
Tests for Razorpay order generation, payment signature verification, webhooks, and Pro upgrades.
"""
import hmac
import hashlib
import json
from decimal import Decimal
from unittest.mock import MagicMock
import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from billing.models import SubscriptionPlan, Subscription
from billing.services import verify_razorpay_signature


@pytest.mark.django_db
class TestBillingAndPayments:
    """Test suite for Razorpay payments and Pro subscription lifecycles."""

    def test_list_subscription_plans(self, api_client, sample_plan):
        """Test listing public subscription plans."""
        url = reverse('billing-plans')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        assert response.data[0]['name'] == sample_plan.name

    def test_create_razorpay_order(self, auth_client, sample_user, sample_plan, monkeypatch):
        """Test creating Razorpay order for Pro upgrade."""
        mock_client = MagicMock()
        mock_client.order.create.return_value = {
            'id': 'order_rzp_mock_12345',
            'amount': 49900,
            'currency': 'INR',
            'receipt': 'rcpt_test'
        }
        monkeypatch.setattr("billing.services.get_razorpay_client", lambda: mock_client)

        url = reverse('billing-create-order')
        payload = {'plan_id': sample_plan.id}

        response = auth_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['order_id'] == 'order_rzp_mock_12345'
        assert response.data['amount'] == 49900

        # Verify created pending subscription
        assert Subscription.objects.filter(
            user=sample_user,
            razorpay_order_id='order_rzp_mock_12345',
            status='created'
        ).exists()

    def test_verify_payment_success_activates_pro(self, auth_client, sample_user, sample_plan, monkeypatch):
        """Test valid Razorpay signature verification activates user Pro subscription."""
        order_id = 'order_test_999'
        payment_id = 'pay_test_888'

        sub = Subscription.objects.create(
            user=sample_user,
            plan=sample_plan,
            razorpay_order_id=order_id,
            status='created'
        )

        # Mock signature verification as valid
        monkeypatch.setattr("billing.services.verify_razorpay_signature", lambda o, p, s: True)

        url = reverse('billing-verify-payment')
        payload = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': 'valid_mock_signature'
        }

        response = auth_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['subscription']['status'] == 'active'

        # Verify User and Subscription updated
        sample_user.refresh_from_db()
        assert sample_user.is_pro is True
        assert sample_user.pro_expires_at is not None

        sub.refresh_from_db()
        assert sub.status == 'active'
        assert sub.razorpay_payment_id == payment_id

    def test_verify_payment_invalid_signature_rejected(self, auth_client, sample_user, sample_plan, monkeypatch):
        """Test that fraudulent or tampered payment signatures are rejected."""
        order_id = 'order_test_fake'
        Subscription.objects.create(
            user=sample_user,
            plan=sample_plan,
            razorpay_order_id=order_id,
            status='created'
        )

        # Force verify_razorpay_signature to return False
        monkeypatch.setattr("billing.services.verify_razorpay_signature", lambda o, p, s: False)

        url = reverse('billing-verify-payment')
        payload = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': 'pay_fake',
            'razorpay_signature': 'tampered_signature'
        }

        response = auth_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        sample_user.refresh_from_db()
        assert sample_user.is_pro is False

    def test_razorpay_webhook_payment_captured(self, api_client, sample_user, sample_plan, monkeypatch):
        """Test Razorpay server-to-server webhook updates subscription."""
        order_id = 'order_webhook_123'
        sub = Subscription.objects.create(
            user=sample_user,
            plan=sample_plan,
            razorpay_order_id=order_id,
            status='created'
        )

        # Mock webhook signature verification
        monkeypatch.setattr("billing.views.handle_razorpay_webhook", lambda raw_payload, signature_header: {
            "status": "success", "event": "payment.captured"
        })

        url = reverse('billing-webhook')
        payload = {
            'event': 'payment.captured',
            'payload': {
                'payment': {
                    'entity': {
                        'id': 'pay_webhook_999',
                        'order_id': order_id,
                        'status': 'captured'
                    }
                }
            }
        }

        response = api_client.post(
            url,
            json.dumps(payload),
            content_type="application/json",
            HTTP_X_RAZORPAY_SIGNATURE="mock_webhook_sig"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'success'

    def test_get_current_subscription(self, auth_client, sample_user, sample_plan):
        """Test retrieving current user's subscription details."""
        Subscription.objects.create(
            user=sample_user,
            plan=sample_plan,
            status='active',
            started_at=timezone.now(),
            current_period_end=timezone.now() + timezone.timedelta(days=30)
        )

        url = reverse('billing-my-subscription')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['plan_name'] == sample_plan.name
        assert response.data['status'] == 'active'
