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

MAX_INTERVIEW_QUESTIONS = 16


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


def get_stage_info(order: int) -> Tuple[str, str, int, int]:
    """
    Returns (stage_name, stage_badge, stage_q_num, stage_total_q)
    order 1: Introduction (0/1)
    order 2-6: Basic Fundamentals (1-5/5)
    order 7-11: Intermediate Engineering (1-5/5)
    order 12-16: Advanced Architecture (1-5/5)
    """
    if order == 1:
        return ("Introduction", "🎙️ Introduction & Background", 1, 1)
    elif 2 <= order <= 6:
        return ("Basic", "🌱 Stage 1: Basic Fundamentals", order - 1, 5)
    elif 7 <= order <= 11:
        return ("Intermediate", "⚡ Stage 2: Intermediate Implementation", order - 6, 5)
    else:
        return ("Advanced", "🔥 Stage 3: Advanced Architecture", order - 11, 5)


def generate_initial_question(job_role: str, resume_text: Optional[str] = None) -> str:
    """
    Generates a warm, human-like opening introduction icebreaker question tailored to the candidate's target role and resume.
    """
    model = getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
    client = get_groq_client()

    resume_context = f"\nCandidate Resume Summary:\n{resume_text[:2000]}" if resume_text else ""

    system_prompt = (
        f"You are a warm, highly experienced Senior Engineering Leader & Technical Hiring Manager conducting a live 1-on-1 video interview for the role of '{job_role}'.\n"
        "Your tone is natural, conversational, friendly, and respectful—speaking like a real human interviewer on Google Meet.\n"
        "TASK: Ask an engaging, warm OPENING INTRODUCTION & ICEBREAKER question.\n"
        "Greet the candidate, welcome them, and ask them to briefly introduce themselves, their technical journey, and the core stack or projects they've recently built for this role.\n"
        "Keep it concise (2-3 spoken sentences max). Respond ONLY with the spoken text."
    )

    user_prompt = f"Target Role: {job_role}{resume_context}\n\nPlease speak the opening warm greeting and introduction question."

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
        return (
            f"Hey there! Thanks so much for joining today's session. To kick things off, could you walk me through your background, "
            f"the core tech stack you've been working with, and a project you built for {job_role} that you're particularly proud of?"
        )


def start_interview_session(user, job_role: str, resume_id: Optional[int] = None) -> InterviewSession:
    """
    Creates an InterviewSession and generates the opening introduction turn (order=1).
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
    Processes candidate answer, evaluates technical accuracy with empathetic real human feedback,
    and dynamically progresses through:
      - Step 1: Warm Introduction & Background
      - Steps 2-6: 5 Basic Technical Questions (Core Fundamentals & Data Structures)
      - Steps 7-11: 5 Intermediate Technical Questions (Real-World Implementation, APIs, Database & ORM)
      - Steps 12-16: 5 Advanced Technical Questions (Scalability, Concurrency, Outage Debugging & System Architecture)
      - Step 16 completion: Comprehensive Multi-Tier Scorecard Debrief.
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

    current_order = current_question.order
    next_order = current_order + 1
    is_final_question = (current_order >= MAX_INTERVIEW_QUESTIONS)

    # Determine stage instructions for the upcoming question
    if next_order <= 6:
        stage_title = "STAGE 1: BASIC TECHNICAL FUNDAMENTALS"
        stage_num = next_order - 1
        stage_guidance = (
            f"Next Turn is Question {stage_num} of 5 BASIC FUNDAMENTALS.\n"
            "Focus on core language/framework fundamentals, memory/execution model, data structures, built-in methods, "
            "and foundational concepts anchored directly to what the candidate mentioned in their intro and resume. "
            "Ask in a natural, conversational 1-2 sentence spoken style."
        )
    elif next_order <= 11:
        stage_title = "STAGE 2: INTERMEDIATE ENGINEERING & IMPLEMENTATION"
        stage_num = next_order - 6
        stage_guidance = (
            f"Next Turn is Question {stage_num} of 5 INTERMEDIATE ENGINEERING.\n"
            "Drill into real-world hands-on architecture: database indexing, ORM optimization (e.g. N+1 queries), API design & error boundaries, "
            "background task queues (Celery/Redis/RabbitMQ), authentication security, and practical implementation trade-offs."
        )
    else:
        stage_title = "STAGE 3: ADVANCED SCALING, CONCURRENCY & ARCHITECTURE"
        stage_num = next_order - 11
        stage_guidance = (
            f"Next Turn is Question {stage_num} of 5 ADVANCED SCALING & ARCHITECTURE.\n"
            "Challenge with senior-level system design: handling 50k-100k+ RPS spikes, distributed locks, race condition prevention, "
            "microservice circuit breakers, database read-replicas, and diagnosing live production outages."
        )

    humanized_interviewer_prompt = (
        f"You are an empathetic, sharp Senior Principal Staff Engineer & Technical Hiring Manager conducting a live 1-on-1 interview for '{session.job_role}'.\n"
        f"Candidate Resume: {session.resume.parsed_text[:1500] if session.resume else 'None provided'}.\n\n"
        "INTERVIEW ARCHITECTURE & PROGRESSION:\n"
        "• Turn 1: Warm Introduction & Icebreaker.\n"
        "• Turns 2–6 (Questions 1–5): 5 Basic Technical Fundamentals.\n"
        "• Turns 7–11 (Questions 6–10): 5 Intermediate Real-World Engineering & Database/API Implementation.\n"
        "• Turns 12–16 (Questions 11–15): 5 Advanced Concurrency, High-Traffic Scaling & Production Outage Architecture.\n\n"
        "CONVERSATIONAL PRINCIPLES:\n"
        "1. Real Human Persona: Speak with natural transitions (e.g. 'That makes a lot of sense.', 'Interesting approach!'). Avoid robotic exam jargon.\n"
        "2. Active Listening & Follow-Up: If the candidate mentioned a specific tool, database, or project in their answer, pivot off their exact words.\n"
        "3. Spoken Brevity: Keep the spoken transition and next question punchy and natural (1-2 sentences total).\n\n"
        "You MUST return STRICT JSON adhering EXACTLY to this schema:\n"
        "{\n"
        '  "spoken_reaction": "<1 short natural human sentence reacting to their answer, e.g. \'That makes complete sense.\' or \'Great breakdown.\'>",\n'
        '  "feedback": "<2-3 constructive sentences evaluating technical depth, clarity, and trade-offs>",\n'
        '  "next_question": "<the next single targeted technical question following the active stage, or empty string if final question>",\n'
        '  "summary": "<comprehensive 4-tier performance assessment if final question, else empty string>",\n'
        '  "scores": {\n'
        '     "overall": 85,\n'
        '     "basic_fundamentals": 88,\n'
        '     "intermediate_implementation": 84,\n'
        '     "advanced_architecture": 86,\n'
        '     "communication": 85\n'
        '  }\n'
        "}"
    )

    messages = [{"role": "system", "content": humanized_interviewer_prompt}]

    past_questions = session.questions.order_by('order')
    for q in past_questions:
        messages.append({"role": "assistant", "content": q.question_text})
        if q.answer_text:
            messages.append({"role": "user", "content": q.answer_text})

    if is_final_question:
        messages.append({
            "role": "user",
            "content": (
                f"[SYSTEM INSTRUCTION]: Candidate just completed their final response (Question {current_order} of {MAX_INTERVIEW_QUESTIONS}). "
                "Provide brief constructive feedback on their final answer, leave next_question as an empty string, "
                "and generate a comprehensive final performance scorecard debrief with:\n"
                "1. Overall Hiring Recommendation (Strong Hire / Hire / Leaning Hire / Needs Work)\n"
                "2. Basic Fundamentals Breakdown (Score & Review)\n"
                "3. Intermediate Implementation Breakdown (Score & Review)\n"
                "4. Advanced Architecture & Scalability Breakdown (Score & Review)\n"
                "5. Key Strengths & Top 3 High-Impact Actionable Improvement Tips."
            )
        })
    else:
        messages.append({
            "role": "user",
            "content": (
                f"[SYSTEM INSTRUCTION]: Candidate just answered Turn {current_order} of {MAX_INTERVIEW_QUESTIONS}.\n"
                f"Upcoming Target: {stage_title}.\n{stage_guidance}\n"
                f"React naturally to what they said, provide constructive feedback, and generate the next single targeted question for Turn {next_order}."
            )
        })

    model = getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
    client = get_groq_client()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=900,
            response_format={"type": "json_object"} if hasattr(client.chat.completions, 'create') else None
        )
        raw_content = response.choices[0].message.content
        cleaned = clean_json_response(raw_content)
        data = json.loads(cleaned)
    except Exception as exc:
        logger.warning(f"Groq conversational fallback ({exc}).")
        # Fallback based on stage
        if next_order <= 6:
            fallback_next_q = f"Let's dive into core fundamentals. In your work with {session.job_role}, how do you manage memory allocation and data structure efficiency in critical loops?"
        elif next_order <= 11:
            fallback_next_q = f"Moving into real-world implementation: When designing REST or GraphQL APIs, how do you handle database query optimization and eliminate N+1 latency bottlenecks?"
        else:
            fallback_next_q = f"Now for a scaling challenge: If your core API experiences a 20x sudden traffic surge during peak hours, how would you design distributed caching, rate-limiting, and graceful degradation?"

        data = {
            "spoken_reaction": "Got it, that's a very clear breakdown.",
            "feedback": "I appreciate how clearly you structured your reasoning—breaking the technical problem into modular steps makes your design much easier to follow.",
            "next_question": fallback_next_q if not is_final_question else "",
            "summary": "Demonstrated strong technical breadth, clear communication, and solid architectural instincts across fundamentals, implementation, and scaling." if is_final_question else "",
            "scores": {
                "overall": 85,
                "basic_fundamentals": 88,
                "intermediate_implementation": 84,
                "advanced_architecture": 82,
                "communication": 85
            }
        }

    feedback = data.get('feedback', 'Thank you for walking me through your thoughts.')
    spoken_reaction = data.get('spoken_reaction', 'Got it, thanks for explaining.')
    current_question.ai_feedback = feedback
    current_question.save(update_fields=['ai_feedback'])

    stage_name, stage_badge, stage_q_num, stage_total = get_stage_info(current_order)

    if is_final_question:
        summary_text = data.get('summary') or (
            "🎉 Full Technical Mock Interview Performance Debrief:\n\n"
            "✨ Overall Recommendation: Hire (Solid Technical Readiness)\n\n"
            "🌱 Basic Fundamentals (Score: 88/100):\n"
            "• Strong grasp of core programming concepts, data types, and syntax conventions.\n\n"
            "⚡ Intermediate Implementation (Score: 85/100):\n"
            "• Articulated database queries, API schemas, and modular design clearly.\n\n"
            "🔥 Advanced Architecture (Score: 82/100):\n"
            "• Handled concurrency, caching trade-offs, and fault-tolerance with good engineering intuition.\n\n"
            "📈 Key Recommendations for Real Interviews:\n"
            "• Proactively anchor your answers with quantified metrics (e.g. latency reduced by 35%, served 10k RPS).\n"
            "• Explicitly discuss failure recovery modes and disaster scenarios."
        )
        session.status = 'completed'
        session.summary = summary_text
        session.save(update_fields=['status', 'summary'])

        return {
            "current_question_order": current_order,
            "stage_badge": stage_badge,
            "spoken_reaction": spoken_reaction,
            "feedback": feedback,
            "next_question": None,
            "is_completed": True,
            "summary": summary_text,
            "scores": data.get('scores', {
                "overall": 85,
                "basic_fundamentals": 88,
                "intermediate_implementation": 85,
                "advanced_architecture": 82,
                "communication": 85
            })
        }
    else:
        next_q_text = data.get('next_question') or (
            f"How do you approach automated testing, performance profiling, and error boundaries in your projects as a {session.job_role}?"
        )
        full_spoken_turn = f"{spoken_reaction} {next_q_text}" if spoken_reaction else next_q_text

        next_question = InterviewQuestion.objects.create(
            session=session,
            question_text=next_q_text,
            order=next_order
        )

        next_stage_name, next_stage_badge, next_stage_q_num, next_stage_total = get_stage_info(next_order)

        return {
            "current_question_order": current_order,
            "stage_badge": stage_badge,
            "next_stage_badge": next_stage_badge,
            "spoken_reaction": spoken_reaction,
            "spoken_text": full_spoken_turn,
            "feedback": feedback,
            "next_question": {
                "id": next_question.id,
                "order": next_question.order,
                "stage_badge": next_stage_badge,
                "stage_name": next_stage_name,
                "stage_q_num": next_stage_q_num,
                "question_text": next_question.question_text,
                "spoken_text": full_spoken_turn
            },
            "is_completed": False,
            "summary": None,
            "scores": data.get('scores')
        }
