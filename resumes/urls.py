"""
URL routing for resumes, ATS scanning, GitHub analysis, bullet rewrites, LinkedIn bio,
Auto-Tailor, Salary Estimator, Public Profile, and Public API.
"""
from django.urls import path
from resumes.views import (
    ResumeUploadView,
    ScanResultDetailView,
    ScanResultStatusView,
    ScanResultListView,
    GenerateCoverLetterAPIView,
    GitHubAnalyzerAPIView,
    BulletRewritesAPIView,
    LinkedInBioAPIView,
    AutoTailorResumeAPIView,
    SalaryEstimatorAPIView,
    PublicProfileAPIView,
    DeveloperApiKeyView,
    PublicScoreAPIView,
)

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('scans/', ScanResultListView.as_view(), name='scan-list'),
    path('scan/<int:pk>/', ScanResultDetailView.as_view(), name='scan-detail'),
    path('scan/<int:pk>/status/', ScanResultStatusView.as_view(), name='scan-status'),
    path('scan/<int:scan_id>/cover-letter/', GenerateCoverLetterAPIView.as_view(), name='generate-cover-letter'),
    path('scan/<int:scan_id>/rewrites/', BulletRewritesAPIView.as_view(), name='bullet-rewrites'),
    path('auto-tailor/', AutoTailorResumeAPIView.as_view(), name='auto-tailor-resume'),
    path('salary-estimate/', SalaryEstimatorAPIView.as_view(), name='salary-estimate'),
    path('profile/<str:username>/', PublicProfileAPIView.as_view(), name='public-profile-api'),
    path('github-analyze/', GitHubAnalyzerAPIView.as_view(), name='github-analyze'),
    path('linkedin-bio/', LinkedInBioAPIView.as_view(), name='linkedin-bio'),
    path('developer/api-keys/', DeveloperApiKeyView.as_view(), name='developer-api-keys'),
    path('public/score/', PublicScoreAPIView.as_view(), name='public-score-api'),
]
