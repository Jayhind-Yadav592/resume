"""
Models for Resume files, Job Descriptions, and ATS Scan Results.
"""
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


class Resume(models.Model):
    """
    Uploaded resume PDF and parsed raw text.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resumes',
        db_index=True
    )
    file = models.FileField(
        upload_to='resumes/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="PDF format only, maximum 5MB."
    )
    parsed_text = models.TextField(
        blank=True,
        help_text="Extracted plain text from the uploaded PDF resume."
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'

    def __str__(self) -> str:
        filename = self.file.name.split('/')[-1] if self.file else 'unnamed'
        return f"Resume #{self.id} ({filename}) - {self.user.username}"


class JobDescription(models.Model):
    """
    Target Job Description against which resumes are evaluated.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_descriptions',
        db_index=True
    )
    title = models.CharField(
        max_length=255,
        help_text="Role or job title (e.g. Senior Backend Engineer)."
    )
    raw_text = models.TextField(
        help_text="Full text of the job description or requirements."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job Description'
        verbose_name_plural = 'Job Descriptions'

    def __str__(self) -> str:
        return f"{self.title} - {self.user.username} (#{self.id})"


class ScanResult(models.Model):
    """
    ATS scoring analysis result produced by AI evaluation.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='scan_results',
        db_index=True
    )
    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.CASCADE,
        related_name='scan_results',
        db_index=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    overall_score = models.IntegerField(
        null=True,
        blank=True,
        help_text="Overall match percentage (0-100)."
    )
    keyword_score = models.IntegerField(
        null=True,
        blank=True,
        help_text="Keyword relevance score (0-100)."
    )
    formatting_score = models.IntegerField(
        null=True,
        blank=True,
        help_text="Structure and ATS formatting compliance score (0-100)."
    )
    experience_score = models.IntegerField(
        null=True,
        blank=True,
        help_text="Experience and skills alignment score (0-100)."
    )
    missing_keywords = models.JSONField(
        default=list,
        blank=True,
        help_text="List of important keywords identified in JD but missing in Resume."
    )
    suggestions = models.JSONField(
        default=list,
        blank=True,
        help_text="Actionable bullet points for improving the resume."
    )
    error_message = models.TextField(
        null=True,
        blank=True,
        help_text="Error message if scan processing failed."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Scan Result'
        verbose_name_plural = 'Scan Results'

    def __str__(self) -> str:
        return f"Scan #{self.id} [{self.status}] - Score: {self.overall_score}% (Resume #{self.resume_id})"
