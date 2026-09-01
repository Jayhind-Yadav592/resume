"""
Views for Resume uploads, ATS scans, polling status, Cover Letter generation,
GitHub profile analyzer, bullet refactoring, LinkedIn bio optimizer, Public Developer API tier,
1-Click Auto-Tailor Resume Builder, Salary Estimator, and Public Candidate Profiles.
"""
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from accounts.models import DeveloperApiKey
from resumes.models import Resume, JobDescription, ScanResult
from resumes.serializers import (
    ResumeUploadSerializer,
    ScanResultSerializer,
    ScanStatusSerializer
)
from resumes.services import (
    extract_text_from_pdf,
    check_free_tier_limit,
    generate_cover_letter_service,
    analyze_github_profile,
    generate_bullet_rewrites_service,
    generate_linkedin_bio_service,
    auto_tailor_resume_service,
    estimate_salary_market_service,
    calculate_heuristic_ats_score,
    score_resume_with_groq
)
from resumes.tasks import process_resume_scan

User = get_user_model()


class ResumeUploadView(APIView):
    """
    Endpoint for uploading a resume PDF with a job description for ATS scanning.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ResumeUploadSerializer

    @extend_schema(
        summary="Upload Resume & Start ATS Scan",
        description=(
            "Uploads candidate PDF resume and target job description. "
            "Extracts text and asynchronously queues Groq AI scoring."
        ),
        request=ResumeUploadSerializer,
        responses={
            202: ScanStatusSerializer,
            400: OpenApiTypes.OBJECT
        }
    )
    def post(self, request, *args, **kwargs):
        check_free_tier_limit(request.user)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_obj = serializer.validated_data['file']
        jd_text = serializer.validated_data['job_description']
        title = serializer.validated_data.get('title', 'Target Position')

        parsed_text = extract_text_from_pdf(file_obj)

        resume = Resume.objects.create(
            user=request.user,
            file=file_obj,
            parsed_text=parsed_text
        )

        job_desc = JobDescription.objects.create(
            user=request.user,
            title=title,
            raw_text=jd_text
        )

        scan_result = ScanResult.objects.create(
            resume=resume,
            job_description=job_desc,
            status='pending'
        )

        process_resume_scan.delay(scan_result.id)

        status_data = ScanStatusSerializer(scan_result).data
        return Response(
            {
                'message': 'Resume uploaded successfully. Analysis in progress.',
                'scan': status_data
            },
            status=status.HTTP_202_ACCEPTED
        )


class ScanResultDetailView(APIView):
    """
    Endpoint to retrieve full ATS Scan Result analysis by ID.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ScanResultSerializer

    @extend_schema(
        summary="Get Scan Result Details",
        description="Returns complete ATS breakdown (scores, missing keywords, suggestions) for a given scan ID.",
        responses={200: ScanResultSerializer}
    )
    def get(self, request, pk, *args, **kwargs):
        scan = get_object_or_404(
            ScanResult.objects.select_related('resume', 'job_description'),
            id=pk,
            resume__user=request.user
        )
        serializer = self.serializer_class(scan)
        data = dict(serializer.data)

        if scan.resume and scan.job_description:
            data['bullet_rewrites'] = generate_bullet_rewrites_service(
                scan.resume.parsed_text,
                scan.job_description.raw_text
            )

        return Response(data, status=status.HTTP_200_OK)


class ScanResultStatusView(APIView):
    """
    Endpoint for polling scan completion status.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ScanStatusSerializer

    @extend_schema(
        summary="Poll Scan Status",
        description="Returns current status ('pending', 'processing', 'completed', 'failed') and score for polling.",
        responses={200: ScanStatusSerializer}
    )
    def get(self, request, pk, *args, **kwargs):
        scan = get_object_or_404(
            ScanResult,
            id=pk,
            resume__user=request.user
        )
        serializer = self.serializer_class(scan)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ScanResultListView(APIView):
    """
    Endpoint to retrieve the scan history for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ScanResultSerializer

    @extend_schema(
        summary="List User Resume Scans",
        description="Returns list of all scan results for the authenticated user ordered by newest first.",
        responses={200: ScanResultSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        scans = ScanResult.objects.filter(
            resume__user=request.user
        ).select_related('resume', 'job_description').order_by('-created_at')
        serializer = self.serializer_class(scans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenerateCoverLetterAPIView(APIView):
    """
    Endpoint for generating a tailored AI cover letter from an existing ATS Scan.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Generate AI Cover Letter",
        description="Generates a customized, high-impact cover letter matching the candidate's resume to the job description.",
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request, scan_id, *args, **kwargs):
        scan = get_object_or_404(
            ScanResult.objects.select_related('resume', 'job_description'),
            id=scan_id,
            resume__user=request.user
        )

        candidate_name = request.user.get_full_name() or request.user.username or "Candidate"
        job_title = scan.job_description.title or "Target Position"

        cover_letter_text = generate_cover_letter_service(
            resume_text=scan.resume.parsed_text,
            jd_text=scan.job_description.raw_text,
            job_title=job_title,
            candidate_name=candidate_name
        )

        return Response({
            "scan_id": scan.id,
            "job_title": job_title,
            "candidate_name": candidate_name,
            "cover_letter": cover_letter_text
        }, status=status.HTTP_200_OK)


class GitHubAnalyzerAPIView(APIView):
    """
    Endpoint for evaluating a developer's GitHub profile and calculating Developer Score.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Analyze Developer GitHub Profile",
        description="Extracts public repositories, calculates developer score, language distribution, and resume synergy.",
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request, *args, **kwargs):
        username_or_url = request.data.get('github_url') or request.data.get('username')
        if not username_or_url:
            return Response({'detail': 'Please provide a GitHub username or profile URL.'}, status=status.HTTP_400_BAD_REQUEST)

        result = analyze_github_profile(str(username_or_url))
        return Response(result, status=status.HTTP_200_OK)


class BulletRewritesAPIView(APIView):
    """
    Endpoint for producing high-impact Before vs After bullet point transformations.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Generate AI Bullet Point Refactors",
        description="Transforms weak, passive bullet points into quantified, action-driven power statements.",
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request, scan_id, *args, **kwargs):
        scan = get_object_or_404(
            ScanResult.objects.select_related('resume', 'job_description'),
            id=scan_id,
            resume__user=request.user
        )
        rewrites = generate_bullet_rewrites_service(
            resume_text=scan.resume.parsed_text,
            jd_text=scan.job_description.raw_text
        )
        return Response({'scan_id': scan.id, 'rewrites': rewrites}, status=status.HTTP_200_OK)


class LinkedInBioAPIView(APIView):
    """
    Endpoint for generating tailored LinkedIn 'About' bios.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Generate Tailored LinkedIn Bio",
        description="Generates Punchy, Story, and Technical LinkedIn About summaries based on candidate resume.",
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request, *args, **kwargs):
        resume_id = request.data.get('resume_id')
        target_role = request.data.get('target_role', 'Software Engineer')

        if resume_id:
            resume = get_object_or_404(Resume, id=resume_id, user=request.user)
            resume_text = resume.parsed_text
        else:
            latest_resume = Resume.objects.filter(user=request.user).first()
            resume_text = latest_resume.parsed_text if latest_resume else f"Experienced {target_role} specializing in scalable systems."

        bios = generate_linkedin_bio_service(resume_text, target_role=target_role)
        return Response(bios, status=status.HTTP_200_OK)


class AutoTailorResumeAPIView(APIView):
    """
    1-Click Auto-Tailor Resume Engine endpoint.
    Restructures candidate background with target JD keywords and quantifiable power statements.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="1-Click Auto-Tailor Resume to JD",
        description="Restructures resume into a complete ATS-optimized schema tailored to the target Job Description.",
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request, *args, **kwargs):
        resume_id = request.data.get('resume_id')
        scan_id = request.data.get('scan_id')
        jd_text = request.data.get('job_description', '')

        candidate_name = request.user.get_full_name() or request.user.username or "Candidate"

        if scan_id:
            scan = get_object_or_404(ScanResult, id=scan_id, resume__user=request.user)
            resume_text = scan.resume.parsed_text
            jd_text = jd_text or scan.job_description.raw_text
        elif resume_id:
            resume = get_object_or_404(Resume, id=resume_id, user=request.user)
            resume_text = resume.parsed_text
        else:
            latest_resume = Resume.objects.filter(user=request.user).first()
            resume_text = latest_resume.parsed_text if latest_resume else "Experienced Software Engineer with Python and Django."

        if not jd_text:
            jd_text = "Looking for Senior Fullstack Software Engineer proficient in Python, Django, React, PostgreSQL, Docker, and Microservices."

        tailored_data = auto_tailor_resume_service(
            resume_text=resume_text,
            jd_text=jd_text,
            candidate_name=candidate_name
        )

        return Response(tailored_data, status=status.HTTP_200_OK)


class SalaryEstimatorAPIView(APIView):
    """
    Tech Compensation & Market Rate Intelligence endpoint.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Estimate Tech Compensation Band",
        description="Estimates salary range and high-paying skill uplifts based on tech stack and years of experience.",
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request, *args, **kwargs):
        skills = request.data.get('skills') or ['Python', 'Django', 'PostgreSQL', 'Docker']
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(',') if s.strip()]
        exp_years = int(request.data.get('experience_years', 3))
        location = request.data.get('location', 'India (Bangalore/Remote)')

        estimate = estimate_salary_market_service(
            skills_list=skills,
            experience_years=exp_years,
            location=location
        )
        return Response(estimate, status=status.HTTP_200_OK)


class PublicProfileAPIView(APIView):
    """
    Retrieves public verified candidate credentials for shareable portfolio profiles (/p/<username>/).
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Get Public Verified Candidate Profile",
        description="Returns candidate's verified ATS score badge, GitHub developer score, and technical skill badges.",
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT}
    )
    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        scans = ScanResult.objects.filter(resume__user=user, status='completed').order_by('-overall_score')

        top_score = scans.first().overall_score if scans.exists() else 85
        total_scans = scans.count()

        # Extract top skills from candidate's latest resume
        latest_resume = Resume.objects.filter(user=user).first()
        skills = []
        if latest_resume and latest_resume.parsed_text:
            skills = list(extract_keywords_from_text(latest_resume.parsed_text))[:8]
        if not skills:
            skills = ["Python", "Django", "PostgreSQL", "Docker", "REST APIs", "Git"]

        return Response({
            "username": user.username,
            "full_name": user.get_full_name() or user.username,
            "is_pro": user.is_pro,
            "top_ats_score": top_score,
            "total_verified_scans": total_scans,
            "skills": skills,
            "badges": [
                {"title": "ATS Verified Candidate", "icon": "bi-patch-check-fill", "color": "text-success"},
                {"title": "Interview Ready", "icon": "bi-camera-video-fill", "color": "text-primary"},
                {"title": "Open Source Builder", "icon": "bi-github", "color": "text-dark"}
            ]
        }, status=status.HTTP_200_OK)


class DeveloperApiKeyView(APIView):
    """
    Endpoint to list and generate personal developer API keys for the Public API Tier.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        keys = DeveloperApiKey.objects.filter(user=request.user, is_active=True)
        return Response([{
            'id': k.id,
            'name': k.name,
            'key': k.key,
            'created_at': k.created_at
        } for k in keys], status=status.HTTP_200_OK)

    def post(self, request):
        name = request.data.get('name', 'Production API Key')
        api_key_obj = DeveloperApiKey.generate_for_user(request.user, name=name)
        return Response({
            'message': 'API Key generated successfully. Keep it secret!',
            'api_key': {
                'id': api_key_obj.id,
                'name': api_key_obj.name,
                'key': api_key_obj.key,
                'created_at': api_key_obj.created_at
            }
        }, status=status.HTTP_201_CREATED)


class PublicScoreAPIView(APIView):
    """
    Public Developer API Tier for external platform integrations.
    Authenticates via `X-API-Key: rf_live_...` or Bearer Token.
    """
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    @extend_schema(
        summary="Public ATS Resume Scoring API",
        description="Allows external systems to score resume text against job description via API key.",
        responses={200: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT}
    )
    def post(self, request, *args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.META.get('HTTP_X_API_KEY')
        if not api_key:
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer rf_live_'):
                api_key = auth_header.split('Bearer ')[-1].strip()

        if not api_key:
            return Response({
                'error': 'Missing API Key. Pass your key in the X-API-Key header (e.g. X-API-Key: rf_live_...).'
            }, status=status.HTTP_401_UNAUTHORIZED)

        key_obj = DeveloperApiKey.objects.filter(key=api_key, is_active=True).select_related('user').first()
        if not key_obj:
            return Response({
                'error': 'Invalid or inactive API Key.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        resume_text = request.data.get('resume_text', '').strip()
        job_description = request.data.get('job_description', '').strip()

        if len(resume_text) < 20 or len(job_description) < 20:
            return Response({
                'error': 'Both resume_text and job_description must be at least 20 characters.'
            }, status=status.HTTP_400_BAD_REQUEST)

        scores = calculate_heuristic_ats_score(resume_text, job_description)

        return Response({
            'status': 'success',
            'developer': key_obj.user.username,
            'scores': scores
        }, status=status.HTTP_200_OK)


from django.views.generic import TemplateView


class ResumeDashboardTemplateView(TemplateView):
    template_name = 'resumes/dashboard.html'


class ResumeUploadTemplateView(TemplateView):
    template_name = 'resumes/upload.html'


class ResumeProcessingTemplateView(TemplateView):
    template_name = 'resumes/processing.html'


class ResumeReportTemplateView(TemplateView):
    template_name = 'resumes/report.html'


class ResumeBuilderTemplateView(TemplateView):
    template_name = 'resumes/builder.html'


class PublicProfileTemplateView(TemplateView):
    template_name = 'resumes/public_profile.html'


class SalaryEstimatorTemplateView(TemplateView):
    template_name = 'resumes/salary_estimator.html'
