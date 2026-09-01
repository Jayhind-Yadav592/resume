"""
Service layer for user registration, authentication, and token generation.
"""
from typing import Dict, Any, Tuple
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed, ValidationError

User = get_user_model()


def get_tokens_for_user(user: User) -> Dict[str, str]:
    """
    Generates JWT access and refresh token pair for a given user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def register_user(validated_data: Dict[str, Any]) -> Tuple[User, Dict[str, str]]:
    """
    Creates a new user with hashed password and generates JWT tokens.
    """
    password = validated_data.pop('password')
    user = User(
        username=validated_data.get('username'),
        email=validated_data.get('email', ''),
        first_name=validated_data.get('first_name', ''),
        last_name=validated_data.get('last_name', ''),
        phone_number=validated_data.get('phone_number', '')
    )
    user.set_password(password)
    user.save()

    tokens = get_tokens_for_user(user)
    return user, tokens


def authenticate_user(username: str, password: str) -> Tuple[User, Dict[str, str]]:
    """
    Authenticates user credentials and returns user and JWT tokens.
    """
    user = authenticate(username=username, password=password)
    if not user:
        # Check if login with email was attempted
        try:
            user_obj = User.objects.get(email=username)
            if user_obj.check_password(password):
                user = user_obj
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            pass

    if not user:
        raise AuthenticationFailed('Invalid username/email or password.')

    if not user.is_active:
        raise AuthenticationFailed('User account is disabled.')

    tokens = get_tokens_for_user(user)
    return user, tokens
