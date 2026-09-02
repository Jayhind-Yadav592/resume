"""
URL routing for mock interviews endpoints and company question bank.
"""
from django.urls import path
from interviews.views import (
    StartInterviewView,
    AnswerInterviewQuestionView,
    InterviewSessionDetailView,
    CompanyQuestionsAPIView,
    MCQQuestionsAPIView,
    MCQEvaluateAPIView,
    CodingProblemsListAPIView,
    CodingProblemDetailAPIView,
    CodingRunCodeAPIView,
    CodingAIAssistantAPIView,
)

urlpatterns = [
    path('start/', StartInterviewView.as_view(), name='interview-start'),
    path('<int:session_id>/answer/', AnswerInterviewQuestionView.as_view(), name='interview-answer'),
    path('<int:session_id>/', InterviewSessionDetailView.as_view(), name='interview-detail'),
    path('company-questions/', CompanyQuestionsAPIView.as_view(), name='company-questions-api'),
    
    # Practice Suite APIs
    path('practice/mcq/', MCQQuestionsAPIView.as_view(), name='practice-mcq-api'),
    path('practice/mcq/evaluate/', MCQEvaluateAPIView.as_view(), name='practice-mcq-evaluate-api'),
    path('practice/coding/problems/', CodingProblemsListAPIView.as_view(), name='practice-coding-problems-api'),
    path('practice/coding/problems/<slug:slug>/', CodingProblemDetailAPIView.as_view(), name='practice-coding-detail-api'),
    path('practice/coding/run/', CodingRunCodeAPIView.as_view(), name='practice-coding-run-api'),
    path('practice/coding/ai-assist/', CodingAIAssistantAPIView.as_view(), name='practice-coding-ai-assist-api'),
]

