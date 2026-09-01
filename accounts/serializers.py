"""
Serializers for user authentication, registration, and profile management.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user details."""
    has_active_pro = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'is_pro',
            'pro_expires_at',
            'has_active_pro',
            'date_joined',
        )
        read_only_fields = ('id', 'is_pro', 'pro_expires_at', 'has_active_pro', 'date_joined')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration with robust password validation."""
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="User password meeting complexity requirements."
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'phone_number'
        )
        read_only_fields = ('id',)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return value.lower()

    def validate_password(self, value):
        validate_password(value)
        return value


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login request."""
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )


class AuthTokenResponseSerializer(serializers.Serializer):
    """Serializer for authentication token response."""
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserProfileSerializer()
