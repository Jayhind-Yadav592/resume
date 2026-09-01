"""
Serializers for Resume uploads, Job Descriptions, and Scan Results.
"""
from rest_framework import serializers
from resumes.models import Resume, JobDescription, ScanResult


class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ('id', 'title', 'raw_text', 'created_at')
        read_only_fields = ('id', 'created_at')


class ResumeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('id', 'file', 'parsed_text', 'uploaded_at')
        read_only_fields = ('id', 'parsed_text', 'uploaded_at')


class ResumeUploadSerializer(serializers.Serializer):
    """
    Serializer for uploading resume PDF and job description text.
    Validates file format (PDF) and size (max 5MB).
    """
    file = serializers.FileField(required=True)
    job_description = serializers.CharField(required=True, min_length=20)
    title = serializers.CharField(required=False, default="Target Position", max_length=255)

    def validate_file(self, value):
        # Validate extension
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are supported.")

        # Validate max size (5MB = 5 * 1024 * 1024 bytes)
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(
                f"File size cannot exceed 5MB. Uploaded file is {value.size / (1024 * 1024):.2f}MB."
            )

        return value


class ScanResultSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for complete ATS Scan Result analysis.
    """
    resume_file_url = serializers.SerializerMethodField()
    job_title = serializers.ReadOnlyField(source='job_description.title')

    class Meta:
        model = ScanResult
        fields = (
            'id',
            'status',
            'overall_score',
            'keyword_score',
            'formatting_score',
            'experience_score',
            'missing_keywords',
            'suggestions',
            'error_message',
            'resume',
            'job_description',
            'job_title',
            'resume_file_url',
            'created_at',
        )
        read_only_fields = fields

    def get_resume_file_url(self, obj) -> str:
        if obj.resume and obj.resume.file:
            return obj.resume.file.url
        return ""


class ScanStatusSerializer(serializers.ModelSerializer):
    """
    Lightweight status serializer for polling progress.
    """
    class Meta:
        model = ScanResult
        fields = ('id', 'status', 'overall_score', 'error_message', 'created_at')
        read_only_fields = fields
