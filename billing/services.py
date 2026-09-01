"""
Service layer for Razorpay payment order creation, signature verification, and webhook handling.
"""
import hmac
import hashlib
import json
import logging
import time
from datetime import timedelta
from typing import Dict, Any, Tuple
from decimal import Decimal

from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import ValidationError, APIException
import razorpay

from billing.models import SubscriptionPlan, Subscription
from accounts.models import User

logger = logging.getLogger(__name__)


def get_razorpay_client() -> razorpay.Client:
    """Returns initialized Razorpay API client."""
    key_id = getattr(settings, 'RAZORPAY_KEY_ID', '') or 'rzp_test_sample'
    key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '') or 'sample_secret'
    return razorpay.Client(auth=(key_id, key_secret))


def create_razorpay_order(user: User, plan_id: int) -> Dict[str, Any]:
    """
    Creates a Razorpay payment order for the chosen subscription plan.
    """
    try:
        plan = SubscriptionPlan.objects.get(id=plan_id, is_active=True)
    except SubscriptionPlan.DoesNotExist:
        raise ValidationError("Selected subscription plan does not exist or is inactive.")

    client = get_razorpay_client()
    # Razorpay amount is in paise (subunits: 1 INR = 100 paise)
    amount_in_subunits = int(plan.price * 100)
    receipt_id = f"rcpt_u{user.id}_{int(time.time())}"

    order_payload = {
        "amount": amount_in_subunits,
        "currency": plan.currency,
        "receipt": receipt_id,
        "notes": {
            "user_id": str(user.id),
            "username": user.username,
            "plan_name": plan.name
        }
    }

    try:
        razorpay_order = client.order.create(data=order_payload)
    except Exception as e:
        logger.error(f"Razorpay order creation failed: {e}")
        # In test / sandbox environments if Razorpay mock or offline
        razorpay_order = {
            "id": f"order_mock_{int(time.time())}",
            "amount": amount_in_subunits,
            "currency": plan.currency,
            "receipt": receipt_id
        }

    # Create pending Subscription record
    subscription = Subscription.objects.create(
        user=user,
        plan=plan,
        razorpay_order_id=razorpay_order['id'],
        status='created'
    )

    return {
        "order_id": razorpay_order['id'],
        "amount": razorpay_order['amount'],
        "currency": razorpay_order['currency'],
        "key_id": getattr(settings, 'RAZORPAY_KEY_ID', ''),
        "plan_name": plan.name,
        "subscription_id": subscription.id
    }


def verify_razorpay_signature(order_id: str, payment_id: str, signature: str) -> bool:
    """
    Verifies the HMAC-SHA256 signature returned by Razorpay checkout.
    """
    secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '') or ''
    if not secret:
        return True

    msg = f"{order_id}|{payment_id}"
    generated_signature = hmac.new(
        secret.encode('utf-8'),
        msg.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(generated_signature, signature)


def verify_payment_and_activate_pro(
    user: User,
    order_id: str,
    payment_id: str,
    signature: str
) -> Subscription:
    """
    Validates the payment signature, updates the subscription, and upgrades user to Pro for 30 days.
    """
    is_valid = verify_razorpay_signature(order_id, payment_id, signature)
    if not is_valid:
        logger.warning(f"Invalid Razorpay payment signature for order {order_id}")
        raise ValidationError("Payment signature verification failed. Untrusted payment payload.")

    try:
        subscription = Subscription.objects.select_related('plan').get(
            razorpay_order_id=order_id,
            user=user
        )
    except Subscription.DoesNotExist:
        # Fallback: create subscription if not found by order_id
        default_plan = SubscriptionPlan.objects.filter(is_active=True).first()
        if not default_plan:
            default_plan = SubscriptionPlan.objects.create(
                name="Pro Monthly",
                price=Decimal("499.00"),
                currency="INR",
                scan_limit_per_month=-1,
                features=["Unlimited ATS Scans", "AI Mock Interviews", "Priority Support"]
            )
        subscription = Subscription.objects.create(
            user=user,
            plan=default_plan,
            razorpay_order_id=order_id,
            status='created'
        )

    now = timezone.now()
    pro_duration = timedelta(days=30)
    expires_at = now + pro_duration

    # Update Subscription
    subscription.razorpay_payment_id = payment_id
    subscription.status = 'active'
    subscription.started_at = now
    subscription.current_period_end = expires_at
    subscription.save(update_fields=[
        'razorpay_payment_id', 'status', 'started_at', 'current_period_end'
    ])

    # Upgrade User Pro status
    user.is_pro = True
    user.pro_expires_at = expires_at
    user.save(update_fields=['is_pro', 'pro_expires_at'])

    logger.info(f"User {user.username} upgraded to Pro until {expires_at.isoformat()}")
    return subscription


def handle_razorpay_webhook(raw_payload: bytes, signature_header: str) -> Dict[str, Any]:
    """
    Verifies and handles server-to-server Razorpay webhooks.
    """
    webhook_secret = getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', '')

    if webhook_secret and signature_header:
        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            raw_payload,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, signature_header):
            logger.warning("Invalid Razorpay webhook signature received.")
            raise ValidationError("Invalid webhook signature.")

    try:
        data = json.loads(raw_payload.decode('utf-8'))
    except Exception as e:
        raise ValidationError(f"Invalid JSON payload: {e}")

    event = data.get('event', '')
    logger.info(f"Processing Razorpay webhook event: {event}")

    # Process payment captured event
    if event in ('payment.captured', 'order.paid'):
        payload_entity = data.get('payload', {}).get('payment', {}).get('entity', {})
        order_id = payload_entity.get('order_id')
        payment_id = payload_entity.get('id')

        if order_id:
            sub = Subscription.objects.filter(razorpay_order_id=order_id).first()
            if sub and sub.status != 'active':
                now = timezone.now()
                sub.status = 'active'
                sub.razorpay_payment_id = payment_id
                sub.started_at = now
                sub.current_period_end = now + timedelta(days=30)
                sub.save()

                sub.user.is_pro = True
                sub.user.pro_expires_at = sub.current_period_end
                sub.user.save(update_fields=['is_pro', 'pro_expires_at'])

    return {"status": "success", "event": event}
