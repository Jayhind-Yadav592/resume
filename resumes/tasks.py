"""
Celery asynchronous tasks for resume scanning and periodic digests.
"""
import logging
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=10,
    time_limit=300
)
def process_resume_scan(self, scan_result_id: int):
    """
    Asynchronous task to parse and score a resume against a job description using Groq AI.
    """
    from resumes.services import process_scan_task

    logger.info(f"Starting async processing for ScanResult #{scan_result_id}")
    try:
        process_scan_task(scan_result_id)
        logger.info(f"Successfully processed ScanResult #{scan_result_id}")
    except Exception as exc:
        logger.error(f"Error processing ScanResult #{scan_result_id}: {exc}")
        # Retry with exponential backoff if transient failure
        raise self.retry(exc=exc)


@shared_task
def send_weekly_pro_digest():
    """
    Celery Beat periodic task: Sends weekly ATS scan summary & tips to Pro subscribers.
    """
    from resumes.models import ScanResult

    pro_users = User.objects.filter(is_pro=True, is_active=True)
    sent_count = 0
    one_week_ago = timezone.now() - timedelta(days=7)

    for user in pro_users:
        if user.pro_expires_at and user.pro_expires_at < timezone.now():
            continue

        recent_scans = ScanResult.objects.filter(
            resume__user=user,
            created_at__gte=one_week_ago
        ).order_by('-created_at')[:5]

        context = {
            'user': user,
            'recent_scans': recent_scans,
            'scan_count': recent_scans.count(),
            'weekly_tip': (
                "Tailor the top one-third of your resume with high-impact quantifiable achievements "
                "and exact keywords found in your target job descriptions."
            )
        }

        html_content = render_to_string('emails/weekly_summary.html', context)
        plain_content = (
            f"Hi {user.first_name or user.username},\n\n"
            f"You had {recent_scans.count()} ATS scans in the last 7 days.\n\n"
            f"Pro Resume Tip: {context['weekly_tip']}\n\n"
            f"Keep optimizing with ResumeForge AI!"
        )

        try:
            send_mail(
                subject="Your Weekly ResumeForge Pro ATS Digest & Tips",
                message=plain_content,
                html_message=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email] if user.email else [],
                fail_silently=True
            )
            sent_count += 1
        except Exception as e:
            logger.error(f"Failed to send weekly digest email to {user.email}: {e}")

    logger.info(f"Weekly Pro digest sent to {sent_count} active Pro subscribers.")
    return sent_count
