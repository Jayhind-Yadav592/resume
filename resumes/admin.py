"""
Django admin registrations for resumes app.
"""
from django.contrib import admin
from resumes.models import Resume, JobDescription, ScanResult


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('user__username', 'user__email', 'parsed_text')
    readonly_fields = ('uploaded_at',)


@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'user__username', 'raw_text')
    readonly_fields = ('created_at',)


@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'resume',
        'job_description',
        'status',
        'overall_score',
        'keyword_score',
        'formatting_score',
        'experience_score',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('resume__user__username', 'job_description__title')
    readonly_fields = ('created_at',)
