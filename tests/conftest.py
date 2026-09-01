"""
Pytest configuration and shared fixtures for ResumeForge test suite.
"""
import io
import json
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from rest_framework.test import APIClient

from resumes.models import Resume, JobDescription, ScanResult
from billing.models import SubscriptionPlan, Subscription

User = get_user_model()


@pytest.fixture
def api_client():
    """Anonymous DRF API Client."""
    return APIClient()


@pytest.fixture
def sample_user(db):
    """Standard free-tier user fixture."""
    return User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='StrongPassword123!',
        first_name='Test',
        last_name='User',
        phone_number='+1234567890',
        is_pro=False
    )


@pytest.fixture
def pro_user(db):
    """Pro-tier user fixture with active subscription."""
    return User.objects.create_user(
        username='prouser',
        email='prouser@example.com',
        password='StrongPassword123!',
        first_name='Pro',
        last_name='Subscriber',
        is_pro=True,
        pro_expires_at=timezone.now() + timezone.timedelta(days=30)
    )


@pytest.fixture
def auth_client(api_client, sample_user):
    """API Client authenticated as standard sample_user."""
    api_client.force_authenticate(user=sample_user)
    return api_client


@pytest.fixture
def pro_client(api_client, pro_user):
    """API Client authenticated as pro_user."""
    api_client.force_authenticate(user=pro_user)
    return api_client


@pytest.fixture
def sample_pdf_file():
    """Returns a valid dummy PDF file for upload testing."""
    # Minimal valid PDF file byte string
    pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000117 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n193\n%%EOF"
    return SimpleUploadedFile(
        name="sample_resume.pdf",
        content=pdf_content,
        content_type="application/pdf"
    )


@pytest.fixture
def sample_resume(db, sample_user, sample_pdf_file):
    """Resume model instance attached to sample_user."""
    return Resume.objects.create(
        user=sample_user,
        file=sample_pdf_file,
        parsed_text=(
            "John Doe - Senior Software Engineer\n"
            "Experience with Python, Django, PostgreSQL, Docker, Kubernetes, AWS.\n"
            "Led backend architecture and scalable microservices."
        )
    )


@pytest.fixture
def sample_plan(db):
    """Pro Monthly SubscriptionPlan fixture."""
    return SubscriptionPlan.objects.create(
        name="Pro Monthly",
        price=Decimal("499.00"),
        currency="INR",
        scan_limit_per_month=-1,
        features=[
            "Unlimited ATS Resume Scans",
            "Full AI Mock Interviews",
            "Weekly Pro Career Digest"
        ],
        is_active=True
    )


@pytest.fixture
def mock_groq_scoring(monkeypatch):
    """
    Mocks the Groq API completion for ATS resume scoring.
    """
    mock_score_data = {
        "overall_score": 88,
        "keyword_score": 90,
        "formatting_score": 85,
        "experience_score": 89,
        "missing_keywords": ["Kubernetes Helm", "GraphQL"],
        "suggestions": [
            "Quantify impact with percentage growth metrics.",
            "Add AWS certifications under qualifications."
        ]
    }

    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = json.dumps(mock_score_data)
    mock_response.choices = [mock_choice]

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    monkeypatch.setattr("resumes.services.Groq", lambda *args, **kwargs: mock_client)
    return mock_score_data


@pytest.fixture
def mock_groq_interview(monkeypatch):
    """
    Mocks the Groq API completion for turn-based mock interviews.
    """
    mock_interview_data = {
        "feedback": "Strong answer demonstrating good grasp of system architecture and concurrency.",
        "next_question": "How would you handle cache invalidation across distributed instances?",
        "summary": "Solid technical performance with clear communication."
    }

    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = json.dumps(mock_interview_data)
    mock_response.choices = [mock_choice]

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    monkeypatch.setattr("interviews.services.Groq", lambda *args, **kwargs: mock_client)
    monkeypatch.setattr("interviews.services.get_groq_client", lambda: mock_client)
    return mock_interview_data
