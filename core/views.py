"""
Core views: Landing page (MVT TemplateView) and API Health Check.
"""
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from core.services import get_system_health
from core.serializers import HealthCheckSerializer


class HomeView(TemplateView):
    """
    Classic Django MVT Template View for the public landing page.
    """
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = 'ResumeForge AI'
        context['tagline'] = 'Supercharge your job search with AI ATS scoring and dynamic mock interviews.'
        return context


class DashboardView(TemplateView):
    """
    Interactive full-featured SaaS dashboard for resume scanning and mock interviews.
    """
    template_name = 'resumes/dashboard.html'


class PricingView(TemplateView):
    """
    Pricing plans page view.
    """
    template_name = 'core/pricing.html'


class HealthCheckView(APIView):
    """
    Public API Health Check endpoint.
    """
    permission_classes = [AllowAny]
    serializer_class = HealthCheckSerializer

    @extend_schema(
        summary="API Health Check",
        description="Returns current operational status of the service.",
        responses={200: HealthCheckSerializer}
    )
    def get(self, request, *args, **kwargs):
        health_data = get_system_health()
        return Response(health_data)
