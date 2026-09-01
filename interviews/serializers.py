"""
Serializers for Interview sessions, questions, and responses.
"""
from rest_framework import serializers
from interviews.models import InterviewSession, InterviewQuestion


class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = (
            'id',
            'order',
            'question_text',
            'answer_text',
            'ai_feedback',
            'created_at',
        )
        read_only_fields = fields


class InterviewSessionSerializer(serializers.ModelSerializer):
    questions = InterviewQuestionSerializer(many=True, read_only=True)
    resume_id = serializers.ReadOnlyField(source='resume.id')

    class Meta:
        model = InterviewSession
        fields = (
            'id',
            'job_role',
            'resume',
            'resume_id',
            'status',
            'summary',
            'created_at',
            'updated_at',
            'questions',
        )
        read_only_fields = fields


class StartInterviewSerializer(serializers.Serializer):
    job_role = serializers.CharField(max_length=255, required=True)
    resume_id = serializers.IntegerField(required=False, allow_null=True)


class AnswerQuestionSerializer(serializers.Serializer):
    answer_text = serializers.CharField(required=True, min_length=2)


class AnswerResponseSerializer(serializers.Serializer):
    current_question_order = serializers.IntegerField()
    feedback = serializers.CharField()
    next_question = serializers.DictField(required=False, allow_null=True)
    is_completed = serializers.BooleanField()
    summary = serializers.CharField(required=False, allow_null=True)
