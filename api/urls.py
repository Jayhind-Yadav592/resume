"""
Unified API v1 routing connecting all application viewsets and endpoints.
Mounted under /api/v1/
"""
from django.urls import path, include

urlpatterns = [
    # Accounts & Authentication (/api/v1/auth/)
    path('auth/', include('accounts.urls')),

    # Resumes & ATS Scanning (/api/v1/resumes/)
    path('resumes/', include('resumes.urls')),

    # AI Mock Interviews (/api/v1/interviews/)
    path('interviews/', include('interviews.urls')),

    # Technical Practice Suite (/api/v1/practice/)
    path('', include('interviews.urls')),

    # Billing & Razorpay Subscriptions (/api/v1/billing/)
    path('billing/', include('billing.urls')),

    # Core System Endpoints (/api/v1/core/)
    path('core/', include('core.urls')),
]
