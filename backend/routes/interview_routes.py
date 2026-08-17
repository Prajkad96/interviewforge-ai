from flask import Blueprint, request, jsonify, session
from extensions import db
from models import User, UserProfile, InterviewSession, QuestionAttempt, Weakness
from services.groq_service import groq_service
from datetime import datetime, timedelta
import json

interview_bp = Blueprint('interview', __name__, url_prefix='/api/interview')

@interview_bp.route('/start', methods=['POST'])
def start_session():
    data = request.json or {}
    user_id = session.get('user_id', 1)
    session_type = data.get('session_type', 'Technical 30')
    target_role = data.get('target_role', 'Junior Python Developer')

    sess = InterviewSession(
        user_id=user_id,
        session_type=session_type,
        target_role=target_role,
        hiring_signal="In Progress"
    )
    db.session.add(sess)
    db.session.commit()

    return jsonify({"session": sess.to_dict()})

@interview_bp.route('/question', methods=['POST'])
def get_next_question():
    data = request.json or {}
    category = data.get('category', 'Python')
    topic = data.get('topic', 'OOP')
    difficulty = data.get('difficulty', 'Medium')
    project_context = data.get('project_context', None)
    user_id = session.get('user_id', 1)

    # Fetch last 15 questions asked to the candidate to guarantee non-repetition
    recent_attempts = QuestionAttempt.query.join(InterviewSession).filter(
        InterviewSession.user_id == user_id,
        QuestionAttempt.category == category
    ).order_by(QuestionAttempt.created_at.desc()).limit(15).all()

    previously_asked = [a.question_text for a in recent_attempts]

    q_data = groq_service.generate_interview_question(
        category, topic, difficulty, project_context, previously_asked=previously_asked
    )
    return jsonify(q_data)


@interview_bp.route('/evaluate', methods=['POST'])
def evaluate_answer():
    data = request.json or {}
    user_id = session.get('user_id', 1)
    session_id = data.get('session_id')
    category = data.get('category', 'Python')
    question_text = data.get('question_text', '')
    user_transcript = data.get('user_transcript', '')
    expected_points = data.get('expected_key_points', None)

    if not question_text or not user_transcript:
        return jsonify({"error": "Missing question or answer transcript."}), 400

    # Evaluate answer using Groq API or Fallback
    eval_res = groq_service.evaluate_answer(question_text, user_transcript, expected_points)

    attempt = QuestionAttempt(
        session_id=session_id or 1,
        category=category,
        question_text=question_text,
        user_transcript=user_transcript,
        score=eval_res.get('score', 3),
        technical_accuracy=eval_res.get('technical_accuracy', 3),
        communication_score=eval_res.get('communication_score', 3),
        feedback_json=json.dumps(eval_res),
        follow_up_question=eval_res.get('follow_up_question', '')
    )
    db.session.add(attempt)

    # Track weakness if score <= 2
    if eval_res.get('score', 3) <= 2:
        weakness = Weakness(
            user_id=user_id,
            topic_name=category,
            category=category.lower(),
            mistake_summary=f"Weak answer on: {question_text[:80]}...",
            review_stage=1,
            next_review_at=datetime.utcnow() + timedelta(days=1)
        )
        db.session.add(weakness)

    db.session.commit()

    return jsonify({
        "attempt_id": attempt.id,
        "evaluation": eval_res
    })

@interview_bp.route('/finish-session/<int:session_id>', methods=['POST'])
def finish_session(session_id):
    sess = InterviewSession.query.get_or_404(session_id)
    attempts = sess.attempts.all()

    if attempts:
        avg_score = sum(a.score for a in attempts) / len(attempts)
        sess.overall_score = round(avg_score * 20, 1) # convert 0-5 to 0-100%
        if sess.overall_score >= 80:
            sess.hiring_signal = "Strong Hire"
        elif sess.overall_score >= 65:
            sess.hiring_signal = "Hire"
        elif sess.overall_score >= 50:
            sess.hiring_signal = "Borderline"
        else:
            sess.hiring_signal = "Needs Improvement"
    else:
        sess.overall_score = 50.0
        sess.hiring_signal = "Completed"

    sess.summary_feedback = f"Completed {len(attempts)} technical questions. Average technical accuracy: {sess.overall_score}%."
    db.session.commit()

    return jsonify({"session": sess.to_dict()})

@interview_bp.route('/history', methods=['GET'])
def get_history():
    user_id = session.get('user_id', 1)
    sessions = InterviewSession.query.filter_by(user_id=user_id).order_by(InterviewSession.created_at.desc()).all()
    return jsonify({"sessions": [s.to_dict() for s in sessions]})
