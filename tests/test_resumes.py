"""
Tests for resume uploading, PDF validation, free tier quota limits, Celery ATS scoring, and polling.
"""
from decimal import Decimal
from unittest.mock import patch, MagicMock
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from resumes.models import Resume, JobDescription, ScanResult
from resumes.services import (
    score_resume_with_groq,
    check_free_tier_limit,
    PaymentRequiredException,
    extract_text_from_pdf,
    clean_json_response,
)
from resumes.tasks import process_resume_scan, send_weekly_pro_digest


@pytest.mark.django_db
class TestResumeUploadAndValidation:
    """Test suite for resume upload and PDF parsing."""

    def test_upload_resume_success(self, auth_client, sample_pdf_file, mock_groq_scoring, monkeypatch):
        """Test valid PDF upload starts async scan and returns 202."""
        # Monkeypatch celery task delay
        mock_delay = MagicMock()
        monkeypatch.setattr("resumes.tasks.process_resume_scan.delay", mock_delay)
        monkeypatch.setattr("resumes.views.extract_text_from_pdf", lambda f: "Sample parsed resume text.")

        url = reverse('resume-upload')
        payload = {
            'file': sample_pdf_file,
            'job_description': 'Senior Backend Engineer with Python, Django, PostgreSQL, and AWS experience.',
            'title': 'Senior Python Developer'
        }

        response = auth_client.post(url, payload, format='multipart')
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert 'scan' in response.data
        assert response.data['scan']['status'] == 'pending'
        assert mock_delay.called

        # Check DB records
        scan_id = response.data['scan']['id']
        scan = ScanResult.objects.get(id=scan_id)
        assert scan.resume.parsed_text == "Sample parsed resume text."
        assert scan.job_description.title == "Senior Python Developer"

    def test_upload_resume_rejects_non_pdf(self, auth_client):
        """Test uploading a non-PDF file (e.g. .docx or .txt) fails validation."""
        text_file = SimpleUploadedFile("resume.txt", b"plain text resume", content_type="text/plain")
        url = reverse('resume-upload')
        payload = {
            'file': text_file,
            'job_description': 'Software Engineer required.'
        }
        response = auth_client.post(url, payload, format='multipart')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'file' in response.data

    def test_upload_resume_rejects_oversized_file(self, auth_client):
        """Test uploading a file larger than 5MB fails validation."""
        # 6MB dummy content
        big_content = b"0" * (6 * 1024 * 1024)
        big_file = SimpleUploadedFile("big_resume.pdf", big_content, content_type="application/pdf")
        url = reverse('resume-upload')
        payload = {
            'file': big_file,
            'job_description': 'Software Engineer required.'
        }
        response = auth_client.post(url, payload, format='multipart')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'file' in response.data

    def test_upload_resume_short_job_description(self, auth_client, sample_pdf_file):
        """Test uploading with too short job description fails validation."""
        url = reverse('resume-upload')
        payload = {
            'file': sample_pdf_file,
            'job_description': 'short'  # less than 20 chars
        }
        response = auth_client.post(url, payload, format='multipart')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'job_description' in response.data


@pytest.mark.django_db
class TestFreeTierScanQuota:
    """Test suite for free-tier unlimited scanning policy for students and candidates."""

    def test_free_tier_unlimited_scans_allowed(self, auth_client, sample_user, sample_resume, monkeypatch):
        """Test that multiple scans in a month are allowed without 402 blocking."""
        jd = JobDescription.objects.create(user=sample_user, title="Dev", raw_text="Django Dev")

        # Create 5 scans in current month
        for _ in range(5):
            ScanResult.objects.create(
                resume=sample_resume,
                job_description=jd,
                status='completed',
                overall_score=80
            )

        # Quota checker should not raise any exception
        check_free_tier_limit(sample_user)

        # Upload endpoint allows unlimited uploads
        monkeypatch.setattr("resumes.tasks.process_resume_scan.delay", MagicMock())
        monkeypatch.setattr("resumes.views.extract_text_from_pdf", lambda f: "Parsed text")

        pdf_file = SimpleUploadedFile("resume4.pdf", b"%PDF-1.4 dummy", content_type="application/pdf")
        url = reverse('resume-upload')
        response = auth_client.post(url, {
            'file': pdf_file,
            'job_description': 'Valid job description with enough length.'
        }, format='multipart')
        assert response.status_code == status.HTTP_202_ACCEPTED

    def test_pro_user_bypasses_scan_limit(self, pro_client, pro_user, sample_pdf_file, monkeypatch):
        """Test that Pro users have unlimited scans."""
        resume = Resume.objects.create(user=pro_user, file=sample_pdf_file, parsed_text="Pro Text")
        jd = JobDescription.objects.create(user=pro_user, title="Dev", raw_text="Pro Dev")

        for _ in range(5):
            ScanResult.objects.create(
                resume=resume,
                job_description=jd,
                status='completed',
                overall_score=95
            )

        check_free_tier_limit(pro_user)

        monkeypatch.setattr("resumes.tasks.process_resume_scan.delay", MagicMock())
        monkeypatch.setattr("resumes.views.extract_text_from_pdf", lambda f: "Pro parsed text")

        url = reverse('resume-upload')
        pdf_file = SimpleUploadedFile("resume6.pdf", b"%PDF-1.4 dummy", content_type="application/pdf")
        response = pro_client.post(url, {
            'file': pdf_file,
            'job_description': 'Senior Cloud Architect position with AWS.'
        }, format='multipart')
        assert response.status_code == status.HTTP_202_ACCEPTED


@pytest.mark.django_db
class TestGroqScoringAndCeleryTask:
    """Test suite for AI ATS scoring and task execution."""

    def test_clean_json_response_helper(self):
        """Test stripping markdown fences from model responses."""
        raw = "```json\n{\"overall_score\": 90}\n```"
        assert clean_json_response(raw) == "{\"overall_score\": 90}"

    def test_score_resume_service_mocked(self, mock_groq_scoring):
        """Test score_resume_with_groq parses JSON output properly."""
        scores = score_resume_with_groq(
            resume_text="Experienced Python Engineer",
            jd_text="Looking for Senior Python Developer with AWS and Django."
        )
        assert scores['overall_score'] == 88
        assert scores['keyword_score'] == 90
        assert "Kubernetes Helm" in scores['missing_keywords']

    def test_celery_process_resume_scan_task(self, sample_user, sample_resume, mock_groq_scoring):
        """Test executing Celery process_resume_scan updates database state to completed."""
        jd = JobDescription.objects.create(
            user=sample_user,
            title="Backend Lead",
            raw_text="Lead engineer with distributed systems knowledge."
        )
        scan = ScanResult.objects.create(
            resume=sample_resume,
            job_description=jd,
            status='pending'
        )

        # Execute task synchronously
        process_resume_scan(scan.id)

        scan.refresh_from_db()
        assert scan.status == 'completed'
        assert scan.overall_score == 88
        assert scan.keyword_score == 90
        assert len(scan.suggestions) > 0

    def test_scan_detail_and_status_endpoints(self, auth_client, sample_user, sample_resume):
        """Test polling status and getting complete scan breakdown."""
        jd = JobDescription.objects.create(user=sample_user, title="Dev", raw_text="Django Dev")
        scan = ScanResult.objects.create(
            resume=sample_resume,
            job_description=jd,
            status='completed',
            overall_score=85,
            keyword_score=80,
            formatting_score=90,
            experience_score=85,
            missing_keywords=['Docker'],
            suggestions=['Add metrics']
        )

        # Poll status
        status_url = reverse('scan-status', kwargs={'pk': scan.id})
        res_status = auth_client.get(status_url)
        assert res_status.status_code == status.HTTP_200_OK
        assert res_status.data['status'] == 'completed'
        assert res_status.data['overall_score'] == 85

        # Get full detail
        detail_url = reverse('scan-detail', kwargs={'pk': scan.id})
        res_detail = auth_client.get(detail_url)
        assert res_detail.status_code == status.HTTP_200_OK
        assert res_detail.data['overall_score'] == 85
        assert res_detail.data['missing_keywords'] == ['Docker']

        # List scans
        list_url = reverse('scan-list')
        res_list = auth_client.get(list_url)
        assert res_list.status_code == status.HTTP_200_OK
        assert len(res_list.data) >= 1

    def test_weekly_pro_digest_celery_task(self, pro_user, sample_pdf_file):
        """Test Celery Beat weekly pro digest task."""
        resume = Resume.objects.create(user=pro_user, file=sample_pdf_file, parsed_text="Pro Text")
        jd = JobDescription.objects.create(user=pro_user, title="Dev", raw_text="Pro Dev")
        ScanResult.objects.create(
            resume=resume,
            job_description=jd,
            status='completed',
            overall_score=92
        )

        sent = send_weekly_pro_digest()
        assert sent >= 1

    def test_generate_cover_letter_endpoint_success(self, auth_client, sample_user, sample_resume):
        """Test generating a tailored cover letter via API."""
        jd = JobDescription.objects.create(
            user=sample_user,
            title="Senior Python Backend Developer",
            raw_text="Required: Python, Django, PostgreSQL, Docker, AWS."
        )
        scan = ScanResult.objects.create(
            resume=sample_resume,
            job_description=jd,
            status='completed',
            overall_score=88
        )

        url = reverse('generate-cover-letter', kwargs={'scan_id': scan.id})
        res = auth_client.post(url)
        assert res.status_code == status.HTTP_200_OK
        assert "cover_letter" in res.data
        assert "Senior Python Backend Developer" in res.data['cover_letter'] or "Dear Hiring" in res.data['cover_letter']
        assert res.data['scan_id'] == scan.id

    def test_github_profile_analyzer_endpoint(self, auth_client):
        """Test GitHub profile analysis endpoint."""
        url = reverse('github-analyze')
        res = auth_client.post(url, {'username': 'torvalds'}, format='json')
        assert res.status_code == status.HTTP_200_OK
        assert 'developer_score' in res.data
        assert 'top_languages' in res.data
        assert 'badges' in res.data
        assert res.data['developer_score'] >= 40

    def test_bullet_rewrites_endpoint(self, auth_client, sample_user, sample_resume):
        """Test AI bullet refactoring Before vs After endpoint."""
        jd = JobDescription.objects.create(user=sample_user, title="Dev", raw_text="Python Django Redis")
        scan = ScanResult.objects.create(resume=sample_resume, job_description=jd, status='completed', overall_score=80)
        url = reverse('bullet-rewrites', kwargs={'scan_id': scan.id})
        res = auth_client.post(url)
        assert res.status_code == status.HTTP_200_OK
        assert 'rewrites' in res.data
        assert len(res.data['rewrites']) > 0
        assert 'before' in res.data['rewrites'][0]
        assert 'after' in res.data['rewrites'][0]

    def test_linkedin_bio_endpoint(self, auth_client, sample_resume):
        """Test LinkedIn Bio optimizer endpoint."""
        url = reverse('linkedin-bio')
        res = auth_client.post(url, {'resume_id': sample_resume.id, 'target_role': 'Lead Backend Engineer'}, format='json')
        assert res.status_code == status.HTTP_200_OK
        assert 'story' in res.data or 'punchy' in res.data

    def test_developer_api_key_and_public_score_endpoint(self, auth_client, client, sample_user):
        """Test Developer API key generation and Public Score API."""
        # 1. Generate key
        keys_url = reverse('developer-api-keys')
        res_key = auth_client.post(keys_url, {'name': 'Testing Key'}, format='json')
        assert res_key.status_code == status.HTTP_201_CREATED
        api_key = res_key.data['api_key']['key']

        # 2. Query public endpoint with X-API-Key
        public_url = reverse('public-score-api')
        payload = {
            'resume_text': 'Senior Software Engineer with 5 years in Python, Django, PostgreSQL, and Docker.',
            'job_description': 'Looking for Python Backend Engineer with Django, Docker, and PostgreSQL experience.'
        }
        res_public = client.post(public_url, payload, format='json', HTTP_X_API_KEY=api_key)
        assert res_public.status_code == status.HTTP_200_OK
        assert res_public.data['status'] == 'success'
        assert res_public.data['scores']['overall_score'] >= 50

    def test_company_question_bank_endpoint(self, client):
        """Test retrieving curated company questions."""
        url = reverse('company-questions-api')
        res = client.get(url + '?company=Google')
        assert res.status_code == status.HTTP_200_OK
        assert 'questions' in res.data
        assert len(res.data['questions']) >= 1
        assert res.data['questions'][0]['company'] == 'Google'

    def test_auto_tailor_resume_endpoint(self, auth_client):
        """Test 1-click auto-tailor resume endpoint."""
        url = reverse('auto-tailor-resume')
        res = auth_client.post(url, {
            'job_description': 'Senior Backend Engineer with Python, Django, Redis, and AWS.'
        }, format='json')
        assert res.status_code == status.HTTP_200_OK
        assert 'summary' in res.data
        assert 'experience' in res.data
        assert 'skills' in res.data

    def test_salary_estimator_endpoint(self, client):
        """Test tech salary estimation endpoint."""
        url = reverse('salary-estimate')
        res = client.post(url, {
            'skills': ['Python', 'Django', 'Kubernetes', 'AWS'],
            'experience_years': 4,
            'location': 'India (Bangalore/Remote)'
        }, format='json')
        assert res.status_code == status.HTTP_200_OK
        assert 'salary_inr_range' in res.data
        assert 'boost_skills' in res.data

    def test_public_candidate_profile_endpoint(self, client, pro_user):
        """Test public candidate verified profile endpoint."""
        url = reverse('public-profile-api', kwargs={'username': pro_user.username})
        res = client.get(url)
        assert res.status_code == status.HTTP_200_OK
        assert res.data['username'] == pro_user.username
        assert 'top_ats_score' in res.data
        assert 'badges' in res.data

    def test_resume_builder_and_tools_template_renders(self, client):
        """Test that new frontend templates render HTTP 200."""
        urls = ['/resumes/builder/', '/tools/salary-estimator/', '/p/testuser/']
        for u in urls:
            res = client.get(u)
            assert res.status_code == status.HTTP_200_OK


