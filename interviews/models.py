"""
Models for AI Mock Interview Sessions and Questions.
"""
from django.conf import settings
from django.db import models


class InterviewSession(models.Model):
    """
    Tracks a candidate's mock interview session.
    """
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interview_sessions',
        db_index=True
    )
    job_role = models.CharField(
        max_length=255,
        help_text="Target role (e.g. Senior Frontend Engineer, Product Manager)."
    )
    resume = models.ForeignKey(
        'resumes.Resume',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interview_sessions',
        help_text="Optional resume providing candidate background context."
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress',
        db_index=True
    )
    summary = models.TextField(
        null=True,
        blank=True,
        help_text="Overall assessment, strengths, and areas for improvement upon completion."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Interview Session'
        verbose_name_plural = 'Interview Sessions'

    def __str__(self) -> str:
        return f"Interview #{self.id} ({self.job_role}) - {self.user.username} [{self.status}]"


class InterviewQuestion(models.Model):
    """
    Individual turn in an interview: AI question, user response, and AI feedback.
    """
    session = models.ForeignKey(
        InterviewSession,
        on_delete=models.CASCADE,
        related_name='questions',
        db_index=True
    )
    question_text = models.TextField(
        help_text="Question prompted by the AI interviewer."
    )
    answer_text = models.TextField(
        null=True,
        blank=True,
        help_text="Candidate's submitted answer."
    )
    ai_feedback = models.TextField(
        null=True,
        blank=True,
        help_text="Immediate feedback on candidate's answer."
    )
    order = models.PositiveIntegerField(
        default=1,
        help_text="Sequential question number in session (1 through 6)."
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Interview Question'
        verbose_name_plural = 'Interview Questions'
        unique_together = ('session', 'order')

    def __str__(self) -> str:
        return f"Q{self.order} for Session #{self.session_id}"
