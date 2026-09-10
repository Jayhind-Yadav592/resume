from django.http import HttpResponse
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


def robots_txt_view(request):
    """
    SEO robots.txt file instructing search engine crawlers and linking XML sitemap.
    """
    content = """User-agent: *
Allow: /
Allow: /pricing/
Allow: /builder/
Allow: /resumes/upload/
Allow: /tools/salary-estimator/
Allow: /interviews/setup/
Allow: /interviews/companies/
Allow: /practice/mcq/
Allow: /practice/coding/
Allow: /login/
Allow: /register/
Allow: /p/

# Disallow authenticated/internal app routes
Disallow: /admin/
Disallow: /api/
Disallow: /dashboard/
Disallow: /resumes/dashboard/
Disallow: /resumes/processing/
Disallow: /resumes/report/
Disallow: /interviews/chat/

Sitemap: https://resume-hn9o.onrender.com/sitemap.xml
"""
    return HttpResponse(content.strip(), content_type="text/plain")


def sitemap_xml_view(request):
    """
    Dynamic SEO XML sitemap indexing all public landing pages and tools.
    """
    base_url = "https://resume-hn9o.onrender.com"
    pages = [
        {"loc": "/", "priority": "1.0", "changefreq": "daily"},
        {"loc": "/resumes/upload/", "priority": "0.9", "changefreq": "weekly"},
        {"loc": "/builder/", "priority": "0.9", "changefreq": "weekly"},
        {"loc": "/interviews/setup/", "priority": "0.9", "changefreq": "weekly"},
        {"loc": "/tools/salary-estimator/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": "/interviews/companies/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": "/practice/mcq/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": "/practice/coding/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": "/pricing/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": "/login/", "priority": "0.5", "changefreq": "monthly"},
        {"loc": "/register/", "priority": "0.5", "changefreq": "monthly"},
    ]

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for page in pages:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{base_url}{page["loc"]}</loc>')
        xml_lines.append(f'    <changefreq>{page["changefreq"]}</changefreq>')
        xml_lines.append(f'    <priority>{page["priority"]}</priority>')
        xml_lines.append('  </url>')
    xml_lines.append('</urlset>')

    return HttpResponse("\n".join(xml_lines), content_type="application/xml")
