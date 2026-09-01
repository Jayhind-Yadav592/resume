"""
URL Configuration for resumeforge.
Wires Django MVT views, admin, DRF endpoints, and OpenAPI documentation.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from core.views import HomeView, PricingView
from accounts.views import LoginTemplateView, RegisterTemplateView
from resumes.views import (
    ResumeDashboardTemplateView,
    ResumeUploadTemplateView,
    ResumeProcessingTemplateView,
    ResumeReportTemplateView,
    ResumeBuilderTemplateView,
    PublicProfileTemplateView,
    SalaryEstimatorTemplateView,
)
from interviews.views import (
    InterviewSetupTemplateView,
    InterviewChatTemplateView,
    CompanyQuestionsTemplateView,
    MCQPracticeTemplateView,
    CodingPracticeTemplateView,
)

from django.http import HttpResponse

def favicon_view(request):
    svg = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='#4F46E5'/><path d='M30 70 L50 30 L70 70 Z' fill='#FFFFFF'/></svg>"""
    return HttpResponse(svg, content_type="image/svg+xml")

urlpatterns = [
    # Favicon
    path('favicon.ico', favicon_view, name='favicon'),

    # Admin Interface
    path('admin/', admin.site.urls),

    # Public Template Views
    path('', HomeView.as_view(), name='home'),
    path('pricing/', PricingView.as_view(), name='pricing-page'),
    path('login/', LoginTemplateView.as_view(), name='login-page'),
    path('register/', RegisterTemplateView.as_view(), name='register-page'),

    # User App Template Views (Bootstrap 5 Frontend)
    path('dashboard/', ResumeDashboardTemplateView.as_view(), name='dashboard'),
    path('resumes/dashboard/', ResumeDashboardTemplateView.as_view(), name='resume-dashboard'),
    path('resumes/upload/', ResumeUploadTemplateView.as_view(), name='resume-upload-page'),
    path('resumes/processing/', ResumeProcessingTemplateView.as_view(), name='resume-processing-page'),
    path('resumes/report/', ResumeReportTemplateView.as_view(), name='resume-report-page'),
    path('resumes/builder/', ResumeBuilderTemplateView.as_view(), name='resume-builder-page'),
    path('builder/', ResumeBuilderTemplateView.as_view(), name='resume-builder-alias'),
    path('tools/salary-estimator/', SalaryEstimatorTemplateView.as_view(), name='salary-estimator-page'),
    path('p/<str:username>/', PublicProfileTemplateView.as_view(), name='public-profile-page'),
    path('interviews/setup/', InterviewSetupTemplateView.as_view(), name='interview-setup-page'),
    path('interviews/chat/', InterviewChatTemplateView.as_view(), name='interview-chat-page'),
    path('interviews/companies/', CompanyQuestionsTemplateView.as_view(), name='company-questions-page'),
    
    # Practice Suite Template Routes
    path('practice/mcq/', MCQPracticeTemplateView.as_view(), name='practice-mcq-page'),
    path('practice/coding/', CodingPracticeTemplateView.as_view(), name='practice-coding-page'),


    # Core App URLs
    path('', include('core.urls')),

    # REST API v1
    path('api/v1/', include('api.urls')),

    # OpenAPI 3.0 & Swagger / Redoc Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='redoc'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
