"""
Tests for core views: landing page MVT template rendering and health check.
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCoreViews:
    """Test suite for core app templates and endpoints."""

    def test_home_page_renders_template(self, api_client):
        """Test public home page returns 200 and contains app name."""
        url = reverse('home')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "ResumeForge" in response.content.decode('utf-8')

    def test_login_page_renders_template(self, api_client):
        """Test web login page returns 200 and contains JWT script."""
        url = reverse('login-page')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "resumeforge_access_token" in response.content.decode('utf-8')

    def test_pricing_page_renders_template(self, api_client):
        """Test pricing page returns 200 and displays subscription plans."""
        url = reverse('pricing-page')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "Free Starter" in response.content.decode('utf-8')
        assert "Pro Monthly" in response.content.decode('utf-8')

    def test_register_page_renders_template(self, api_client):
        """Test register page returns 200."""
        url = reverse('register-page')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "Create Your Account" in response.content.decode('utf-8')

    def test_resume_dashboard_page_renders(self, api_client):
        """Test resumes dashboard page returns 200."""
        url = reverse('resume-dashboard')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "Dashboard" in response.content.decode('utf-8')

    def test_resume_upload_page_renders(self, api_client):
        """Test resume upload page returns 200."""
        url = reverse('resume-upload-page')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "Scan Your Resume" in response.content.decode('utf-8')

    def test_interview_setup_page_renders(self, api_client):
        """Test interview setup page returns 200."""
        url = reverse('interview-setup-page')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "Setup Your Mock Session" in response.content.decode('utf-8')

    def test_health_check_endpoint(self, api_client):
        """Test API health check returns healthy status."""
        url = reverse('health-check')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'healthy'
        assert response.data['service'] == 'resumeforge-api'
