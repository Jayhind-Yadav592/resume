"""
Tests for AI Mock Interview session creation, turn progression, feedback, and summary generation.
"""
from unittest.mock import MagicMock
import json
import pytest
from django.urls import reverse
from rest_framework import status

from interviews.models import InterviewSession, InterviewQuestion


@pytest.mark.django_db
class TestMockInterviewEngine:
    """Test suite for turn-based AI Mock Interview engine."""

    def test_start_interview_success(self, auth_client, sample_user, sample_resume, mock_groq_interview, monkeypatch):
        """Test starting an interview session initializes Question 1."""
        monkeypatch.setattr(
            "interviews.services.generate_initial_question",
            lambda job_role, resume_text: f"Tell me about your experience as a {job_role}."
        )

        url = reverse('interview-start')
        payload = {
            'job_role': 'Senior Backend Engineer',
            'resume_id': sample_resume.id
        }

        response = auth_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['job_role'] == 'Senior Backend Engineer'
        assert response.data['status'] == 'in_progress'
        assert len(response.data['questions']) == 1
        assert response.data['questions'][0]['order'] == 1
        assert "Senior Backend Engineer" in response.data['questions'][0]['question_text']

    def test_answer_interview_question_turn_progression(self, auth_client, sample_user, mock_groq_interview):
        """Test submitting an answer generates feedback and advances to the next question."""
        session = InterviewSession.objects.create(
            user=sample_user,
            job_role='DevOps Specialist',
            status='in_progress'
        )
        q1 = InterviewQuestion.objects.create(
            session=session,
            question_text="How do you manage Docker containers in production?",
            order=1
        )

        url = reverse('interview-answer', kwargs={'session_id': session.id})
        payload = {
            'answer_text': 'I use Kubernetes clusters managed with Terraform and Helm charts with Prometheus monitoring.'
        }

        response = auth_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['current_question_order'] == 1
        assert response.data['feedback'] is not None
        assert response.data['is_completed'] is False
        assert response.data['next_question'] is not None
        assert response.data['next_question']['order'] == 2

        # Verify DB state
        q1.refresh_from_db()
        assert q1.answer_text == payload['answer_text']
        assert q1.ai_feedback is not None
        assert session.questions.count() == 2

    def test_answer_final_question_completes_session(self, auth_client, sample_user, mock_groq_interview):
        """Test answering the 6th question completes the session and stores the summary."""
        session = InterviewSession.objects.create(
            user=sample_user,
            job_role='Fullstack Developer',
            status='in_progress'
        )
        # Seed 5 answered questions
        for i in range(1, 6):
            InterviewQuestion.objects.create(
                session=session,
                question_text=f"Question {i}",
                answer_text=f"Answer {i}",
                ai_feedback=f"Feedback {i}",
                order=i
            )

        # 6th active question
        q6 = InterviewQuestion.objects.create(
            session=session,
            question_text="What is your long-term engineering vision?",
            order=6
        )

        url = reverse('interview-answer', kwargs={'session_id': session.id})
        payload = {
            'answer_text': 'I aim to architect resilient distributed systems while mentoring juniors.'
        }

        response = auth_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_completed'] is True
        assert response.data['summary'] is not None
        assert response.data['next_question'] is None

        # Verify DB session is completed
        session.refresh_from_db()
        assert session.status == 'completed'
        assert session.summary is not None

    def test_get_interview_session_details(self, auth_client, sample_user):
        """Test retrieving complete session history and Q&A turns."""
        session = InterviewSession.objects.create(
            user=sample_user,
            job_role='Data Scientist',
            status='in_progress'
        )
        InterviewQuestion.objects.create(
            session=session,
            question_text="Explain gradient boosting.",
            answer_text="It is an ensemble tree technique...",
            ai_feedback="Clear explanation.",
            order=1
        )

        url = reverse('interview-detail', kwargs={'session_id': session.id})
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['job_role'] == 'Data Scientist'
        assert len(response.data['questions']) == 1

    def test_cannot_access_other_users_interview(self, api_client, sample_user, pro_user):
        """Test that users cannot view or answer another user's session."""
        session = InterviewSession.objects.create(
            user=pro_user,
            job_role='Staff Engineer',
            status='in_progress'
        )
        api_client.force_authenticate(user=sample_user)

        url = reverse('interview-detail', kwargs={'session_id': session.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPracticeSuite:
    """Test suite for MCQ Practice and Coding Practice Arena."""

    def test_mcq_questions_list_api(self, client):
        """Test retrieving MCQ questions and topics."""
        url = reverse('practice-mcq-api')
        res = client.get(url)
        assert res.status_code == status.HTTP_200_OK
        assert 'topics' in res.data
        assert 'questions' in res.data
        assert len(res.data['questions']) > 0

    def test_mcq_evaluate_api(self, client):
        """Test evaluating submitted MCQ quiz answers."""
        url = reverse('practice-mcq-evaluate-api')
        payload = {
            "answers": {"1": 1, "2": 1, "3": 2},
            "time_taken": 120
        }
        res = client.post(url, json.dumps(payload), content_type='application/json')
        assert res.status_code == status.HTTP_200_OK
        assert 'score' in res.data
        assert 'percentage' in res.data
        assert 'grade' in res.data
        assert 'breakdown' in res.data

    def test_coding_problems_list_and_detail_api(self, client):
        """Test retrieving coding problems list and detail."""
        list_url = reverse('practice-coding-problems-api')
        res = client.get(list_url)
        assert res.status_code == status.HTTP_200_OK
        assert 'problems' in res.data
        assert len(res.data['problems']) >= 4

        detail_url = reverse('practice-coding-detail-api', kwargs={'slug': 'two-sum'})
        res_detail = client.get(detail_url)
        assert res_detail.status_code == status.HTTP_200_OK
        assert res_detail.data['title'] == 'Two Sum'
        assert 'starter_code' in res_detail.data

    def test_coding_run_code_api_python_success(self, client):
        """Test executing valid Python solution in coding arena."""
        url = reverse('practice-coding-run-api')
        payload = {
            "slug": "two-sum",
            "code": "def twoSum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        diff = target - n\n        if diff in seen:\n            return [seen[diff], i]\n        seen[n] = i\n    return []",
            "language": "python"
        }
        res = client.post(url, json.dumps(payload), content_type='application/json')
        assert res.status_code == status.HTTP_200_OK
        assert res.data['status'] == 'Accepted'
        assert res.data['all_passed'] is True
        assert len(res.data['test_results']) == 3

    def test_practice_templates_render(self, client):
        """Test that MCQ and Coding practice web pages return HTTP 200."""
        res_mcq = client.get('/practice/mcq/')
        assert res_mcq.status_code == status.HTTP_200_OK

        res_coding = client.get('/practice/coding/')
        assert res_coding.status_code == status.HTTP_200_OK

