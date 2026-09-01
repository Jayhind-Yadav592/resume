"""
Service layer for AI Mock Interview orchestration, Groq AI conversational turns, and session summarization.
Features a warm, highly perceptive, human Senior Engineering Manager persona.
"""
import json
import logging
import re
from typing import Dict, Any, Tuple, Optional
from django.conf import settings
from rest_framework.exceptions import ValidationError, APIException
from groq import Groq

from interviews.models import InterviewSession, InterviewQuestion
from resumes.models import Resume

logger = logging.getLogger(__name__)

MAX_INTERVIEW_QUESTIONS = 6


def clean_json_response(raw_text: str) -> str:
    """Strips markdown code blocks from JSON string."""
    raw_text = raw_text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text)
    if match:
        return match.group(1).strip()
    return raw_text


def get_groq_client() -> Groq:
    api_key = getattr(settings, 'GROQ_API_KEY', '') or 'mock_groq_api_key'
    return Groq(api_key=api_key)


def generate_initial_question(job_role: str, resume_text: Optional[str] = None) -> str:
    """
    Generates a warm, natural opening question tailored to the candidate's background and target role.
    """
    model = getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
    client = get_groq_client()

    resume_context = f"\nCandidate Background Excerpt:\n{resume_text[:2500]}" if resume_text else ""

    system_prompt = (
        f"You are a friendly, experienced Senior Engineering Leader & Technical Hiring Manager conducting a live video interview for the role of '{job_role}'.\n"
        "Your tone is warm, respectful, conversational, and genuinely interested in the candidate.\n"
        "Generate a natural, realistic opening question to break the ice and dive into their relevant technical experience.\n"
        "Respond ONLY with the question text. Do not add intro or outro markdown."
    )

    user_prompt = f"Target Role: {job_role}{resume_context}\n\nPlease ask the opening interview question."

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=250,
        )
        question_text = response.choices[0].message.content.strip()
        if question_text.startswith('"') and question_text.endswith('"'):
            question_text = question_text[1:-1].strip()
        return question_text
    except Exception as exc:
        logger.error(f"Groq API error on initial question generation: {exc}")
        return f"Hey there! Thanks for joining today. To kick things off, could you walk me through your technical background and a project you built for {job_role} that you're particularly proud of?"


def start_interview_session(user, job_role: str, resume_id: Optional[int] = None) -> InterviewSession:
    """
    Creates an InterviewSession and generates the first question (order=1).
    """
    resume = None
    resume_text = None
    if resume_id:
        try:
            resume = Resume.objects.get(id=resume_id, user=user)
            resume_text = resume.parsed_text
        except Resume.DoesNotExist:
            raise ValidationError("Specified resume not found or does not belong to the user.")

    session = InterviewSession.objects.create(
        user=user,
        job_role=job_role,
        resume=resume,
        status='in_progress'
    )

    first_question_text = generate_initial_question(job_role=job_role, resume_text=resume_text)

    InterviewQuestion.objects.create(
        session=session,
        question_text=first_question_text,
        order=1
    )

    return session


def submit_interview_answer(session: InterviewSession, answer_text: str) -> Dict[str, Any]:
    """
    Processes candidate answer, retrieves empathetic, human-like AI feedback, and generates the next turn.
    """
    if session.status == 'completed':
        raise ValidationError("This interview session has already been completed.")

    current_question = session.questions.filter(answer_text__isnull=True).order_by('order').first()
    if not current_question:
        current_question = session.questions.order_by('-order').first()
        if not current_question or current_question.order >= MAX_INTERVIEW_QUESTIONS:
            session.status = 'completed'
            session.save(update_fields=['status'])
            raise ValidationError("All questions in this session have already been answered.")

    current_question.answer_text = answer_text.strip()
    current_question.save(update_fields=['answer_text'])

    humanized_interviewer_prompt = (
        f"You are a Senior Principal Staff Engineer & Technical Hiring Manager interviewing a candidate for '{session.job_role}'.\n"
        f"Resume context: {session.resume.parsed_text[:1500] if session.resume else 'None provided'}.\n\n"
        "Guidelines for your response:\n"
        "1. Speak naturally like a real human interviewer at a top company (Google/Swiggy/Razorpay). Acknowledge specific points they made with genuine curiosity and technical nuance.\n"
        "2. Provide 2-3 sentences of constructive, encouraging feedback ('Great point on X, and I liked how you considered Y... to take it further, consider mentioning Z').\n"
        "3. Ask the next question as a natural conversational progression or dive deeper into architecture, edge cases, and real-world trade-offs.\n\n"
        "You MUST return STRICT JSON adhering EXACTLY to this schema:\n"
        "{\n"
        '  "feedback": "<2-3 empathetic, human constructive sentences analyzing their response>",\n'
        '  "next_question": "<the next follow-up or new question, or empty string if this was question 6>",\n'
        '  "summary": "<thorough humanized candidate assessment with Key Highlights, Opportunities for Growth, and Hiring Recommendation if question 6, else empty string>"\n'
        "}"
    )

    messages = [{"role": "system", "content": humanized_interviewer_prompt}]

    past_questions = session.questions.order_by('order')
    for q in past_questions:
        messages.append({"role": "assistant", "content": q.question_text})
        if q.answer_text:
            messages.append({"role": "user", "content": q.answer_text})

    current_order = current_question.order
    is_final_question = (current_order >= MAX_INTERVIEW_QUESTIONS)

    if is_final_question:
        messages.append({
            "role": "user",
            "content": (
                f"[SYSTEM INSTRUCTION]: Candidate just completed Question {current_order} of {MAX_INTERVIEW_QUESTIONS}. "
                "Give brief feedback on their final answer, leave next_question empty, and write a thorough, encouraging, "
                "humanized performance debrief covering Technical Strengths, Communication Clarity, Edge-Case Handling, and Final Hiring Recommendation."
            )
        })
    else:
        messages.append({
            "role": "user",
            "content": (
                f"[SYSTEM INSTRUCTION]: Candidate just answered Question {current_order} of {MAX_INTERVIEW_QUESTIONS}. "
                f"Give natural human feedback and ask Question {current_order + 1}."
            )
        })

    model = getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
    client = get_groq_client()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            response_format={"type": "json_object"} if hasattr(client.chat.completions, 'create') else None
        )
        raw_content = response.choices[0].message.content
        cleaned = clean_json_response(raw_content)
        data = json.loads(cleaned)
    except Exception as exc:
        logger.warning(f"Groq conversational fallback ({exc}).")
        data = {
            "feedback": "I appreciate how clearly you broke down that approach—structuring the problem into modular steps makes the design much easier to reason about.",
            "next_question": f"When scaling this architecture under heavy concurrent traffic, what caching or asynchronous strategies would you prioritize?" if not is_final_question else "",
            "summary": "Demonstrated strong core technical knowledge, clear articulation, and thoughtful reasoning throughout the session." if is_final_question else ""
        }

    feedback = data.get('feedback', 'Thank you for walking me through your thoughts.')
    current_question.ai_feedback = feedback
    current_question.save(update_fields=['ai_feedback'])

    if is_final_question:
        summary_text = data.get('summary') or (
            "🎉 Interview Performance Debrief:\n\n"
            "✨ Key Strengths:\n"
            "• Communicated architectural ideas with structured clarity.\n"
            "• Showed sound understanding of backend fundamentals and practical trade-offs.\n\n"
            "📈 Recommendations for Improvement:\n"
            "• When discussing past projects, anchor your results with specific business metrics (e.g., latency dropped by 30%, served 10k RPS).\n"
            "• Proactively bring up failure modes and disaster recovery scenarios."
        )
        session.status = 'completed'
        session.summary = summary_text
        session.save(update_fields=['status', 'summary'])

        return {
            "current_question_order": current_order,
            "feedback": feedback,
            "next_question": None,
            "is_completed": True,
            "summary": summary_text
        }
    else:
        next_q_text = data.get('next_question') or (
            f"How do you typically approach automated testing, code reviews, and reliability in your team sprints as a {session.job_role}?"
        )
        next_order = current_order + 1
        next_question = InterviewQuestion.objects.create(
            session=session,
            question_text=next_q_text,
            order=next_order
        )

        return {
            "current_question_order": current_order,
            "feedback": feedback,
            "next_question": {
                "id": next_question.id,
                "order": next_question.order,
                "question_text": next_question.question_text
            },
            "is_completed": False,
            "summary": None
        }
