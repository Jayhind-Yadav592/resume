"""
Views for Razorpay order generation, payment verification, and webhooks.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiTypes

from billing.models import SubscriptionPlan, Subscription
from billing.serializers import (
    SubscriptionPlanSerializer,
    SubscriptionSerializer,
    CreateOrderSerializer,
    CreateOrderResponseSerializer,
    VerifyPaymentSerializer,
    VerifyPaymentResponseSerializer,
)
from billing.services import (
    create_razorpay_order,
    verify_payment_and_activate_pro,
    handle_razorpay_webhook,
)


class SubscriptionPlansView(APIView):
    """
    Lists available subscription plans.
    """
    permission_classes = [AllowAny]
    serializer_class = SubscriptionPlanSerializer

    @extend_schema(
        summary="List Subscription Plans",
        description="Returns list of active subscription tiers (Free, Pro Monthly, etc.).",
        responses={200: SubscriptionPlanSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')
        serializer = self.serializer_class(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentSubscriptionView(APIView):
    """
    Retrieves the authenticated user's current subscription.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    @extend_schema(
        summary="Get Current User Subscription",
        description="Returns active or latest subscription details for authenticated user.",
        responses={200: SubscriptionSerializer}
    )
    def get(self, request, *args, **kwargs):
        subscription = Subscription.objects.filter(
            user=request.user
        ).order_by('-created_at').first()

        if not subscription:
            return Response({'detail': 'No active subscription found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateOrderView(APIView):
    """
    Creates a Razorpay order for upgrading to Pro.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderSerializer

    @extend_schema(
        summary="Create Razorpay Order",
        description="Initializes Razorpay order for subscription purchase, returning order_id to client.",
        request=CreateOrderSerializer,
        responses={201: CreateOrderResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_data = create_razorpay_order(
            user=request.user,
            plan_id=serializer.validated_data['plan_id']
        )
        return Response(order_data, status=status.HTTP_201_CREATED)


class VerifyPaymentView(APIView):
    """
    Verifies Razorpay payment signature and upgrades user to Pro.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyPaymentSerializer

    @extend_schema(
        summary="Verify Razorpay Payment",
        description="Validates Razorpay payment signature, marks subscription active, and activates Pro for 30 days.",
        request=VerifyPaymentSerializer,
        responses={200: VerifyPaymentResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        subscription = verify_payment_and_activate_pro(
            user=request.user,
            order_id=serializer.validated_data['razorpay_order_id'],
            payment_id=serializer.validated_data['razorpay_payment_id'],
            signature=serializer.validated_data['razorpay_signature']
        )

        return Response(
            {
                "message": "Payment verified successfully. Pro subscription activated!",
                "subscription": SubscriptionSerializer(subscription).data
            },
            status=status.HTTP_200_OK
        )


class RazorpayWebhookView(APIView):
    """
    Webhook handler for asynchronous Razorpay events.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Razorpay Webhook Handler",
        description="Receives and validates server-to-server webhook events from Razorpay.",
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request, *args, **kwargs):
        signature = request.headers.get('X-Razorpay-Signature', '')
        result = handle_razorpay_webhook(
            raw_payload=request.body,
            signature_header=signature
        )
        return Response(result, status=status.HTTP_200_OK)
