"""
Authentication views (REST API and MVT Template login).
"""
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema

from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    AuthTokenResponseSerializer,
)
from accounts.services import register_user, authenticate_user


class RegisterView(APIView):
    """
    API endpoint for new user registration.
    """
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserRegistrationSerializer

    @extend_schema(
        summary="Register New User",
        description="Creates a new user account with hashed password and returns access/refresh JWT tokens.",
        request=UserRegistrationSerializer,
        responses={201: AuthTokenResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, tokens = register_user(serializer.validated_data)
        user_data = UserProfileSerializer(user).data
        return Response(
            {
                'message': 'Registration successful',
                'user': user_data,
                'access': tokens['access'],
                'refresh': tokens['refresh'],
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    """
    API endpoint for user authentication and token retrieval.
    """
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserLoginSerializer

    @extend_schema(
        summary="User Login",
        description="Authenticates username/email and password, returning JWT access and refresh tokens.",
        request=UserLoginSerializer,
        responses={200: AuthTokenResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, tokens = authenticate_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        user_data = UserProfileSerializer(user).data
        return Response(
            {
                'message': 'Login successful',
                'user': user_data,
                'access': tokens['access'],
                'refresh': tokens['refresh'],
            },
            status=status.HTTP_200_OK
        )


class CurrentUserProfileView(APIView):
    """
    API endpoint to retrieve or update the authenticated user's profile.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    @extend_schema(
        summary="Get Current User Profile",
        description="Returns detailed profile information for the authenticated user.",
        responses={200: UserProfileSerializer}
    )
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginTemplateView(TemplateView):
    """
    Classic Django MVT Template View for the web login page.
    """
    template_name = 'accounts/login.html'


class RegisterTemplateView(TemplateView):
    """
    Classic Django MVT Template View for the registration page.
    """
    template_name = 'accounts/register.html'
