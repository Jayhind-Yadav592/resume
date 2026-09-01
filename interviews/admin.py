"""
Admin registrations for mock interviews app.
"""
from django.contrib import admin
from interviews.models import InterviewSession, InterviewQuestion


class InterviewQuestionInline(admin.TabularInline):
    model = InterviewQuestion
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('order', 'question_text', 'answer_text', 'ai_feedback', 'created_at')


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job_role', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'job_role', 'summary')
    inlines = [InterviewQuestionInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'order', 'created_at')
    list_filter = ('order', 'created_at')
    search_fields = ('session__user__username', 'question_text', 'answer_text')
    readonly_fields = ('created_at',)
