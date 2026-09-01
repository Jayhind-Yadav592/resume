"""
Tests for user accounts, registration, JWT authentication, and permissions.
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from accounts.permissions import IsProUser
from django.utils import timezone
from datetime import timedelta
from unittest.mock import MagicMock

User = get_user_model()


@pytest.mark.django_db
class TestUserAuthentication:
    """Test suite for authentication endpoints."""

    def test_user_registration_success(self, api_client):
        """Test successful registration with valid payload."""
        url = reverse('auth-register')
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePassword987!',
            'first_name': 'New',
            'last_name': 'User',
            'phone_number': '+1987654321'
        }
        response = api_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['username'] == 'newuser'
        assert response.data['user']['email'] == 'newuser@example.com'
        assert User.objects.filter(username='newuser').exists()

    def test_user_registration_duplicate_email(self, api_client, sample_user):
        """Test registration fails when email is already in use."""
        url = reverse('auth-register')
        payload = {
            'username': 'differentuser',
            'email': sample_user.email,
            'password': 'SecurePassword987!'
        }
        response = api_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_user_registration_weak_password(self, api_client):
        """Test registration fails when password does not meet min length."""
        url = reverse('auth-register')
        payload = {
            'username': 'weakuser',
            'email': 'weak@example.com',
            'password': '123'
        }
        response = api_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    def test_user_login_success(self, api_client, sample_user):
        """Test successful login returns JWT tokens."""
        url = reverse('auth-login')
        payload = {
            'username': sample_user.username,
            'password': 'StrongPassword123!'
        }
        response = api_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['username'] == sample_user.username

    def test_user_login_invalid_credentials(self, api_client, sample_user):
        """Test login fails with incorrect password."""
        url = reverse('auth-login')
        payload = {
            'username': sample_user.username,
            'password': 'WrongPassword123!'
        }
        response = api_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_refresh(self, api_client, sample_user):
        """Test obtaining a new access token via refresh token."""
        login_url = reverse('auth-login')
        login_res = api_client.post(login_url, {
            'username': sample_user.username,
            'password': 'StrongPassword123!'
        }, format='json')
        refresh_token = login_res.data['refresh']

        refresh_url = reverse('auth-refresh')
        res = api_client.post(refresh_url, {'refresh': refresh_token}, format='json')
        assert res.status_code == status.HTTP_200_OK
        assert 'access' in res.data

    def test_get_current_user_profile_authenticated(self, auth_client, sample_user):
        """Test retrieving current user profile with valid JWT auth."""
        url = reverse('auth-me')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == sample_user.username
        assert response.data['email'] == sample_user.email
        assert response.data['is_pro'] is False

    def test_get_current_user_profile_unauthenticated(self, api_client):
        """Test unauthenticated request to /auth/me/ returns 401."""
        url = reverse('auth-me')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserModelAndPermissions:
    """Test custom user model properties and IsProUser permission."""

    def test_user_string_representation(self, sample_user):
        assert sample_user.username in str(sample_user)

    def test_has_active_pro_property(self, sample_user, pro_user):
        assert sample_user.has_active_pro is False
        assert pro_user.has_active_pro is True

        # Expired pro
        pro_user.pro_expires_at = timezone.now() - timedelta(days=1)
        pro_user.save()
        assert pro_user.has_active_pro is False

    def test_is_pro_user_permission(self, sample_user, pro_user):
        permission = IsProUser()
        view = MagicMock()

        # Anonymous request
        anon_request = MagicMock()
        anon_request.user.is_authenticated = False
        assert permission.has_permission(anon_request, view) is False

        # Free user request
        free_request = MagicMock()
        free_request.user = sample_user
        assert permission.has_permission(free_request, view) is False

        # Active pro user request
        pro_request = MagicMock()
        pro_request.user = pro_user
        assert permission.has_permission(pro_request, view) is True
