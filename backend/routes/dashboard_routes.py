from flask import Blueprint, request, jsonify, session
from extensions import db
from models import User, UserProfile, Weakness, InterviewSession, QuestionAttempt
from services.groq_service import groq_service
from services.project_kb_service import project_kb_service
from services.curriculum_service import curriculum_service
from services.dsa_service import dsa_service
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/stats', methods=['GET'])
def get_stats():
    user_id = session.get('user_id', 1)
    user = User.query.get(user_id)
    profile = user.profile if user else None

    scores = profile.get_scores() if profile else {"python": 50, "sql": 40, "backend": 45, "ai_ml": 35, "projects": 50, "dsa": 40, "communication": 50, "hr": 50}

    # Weighting: Python 15%, SQL 10%, Backend 15%, AI/ML 10%, Projects 15%, DSA 15%, Communication 10%, HR 10%
    overall_readiness = round(
        scores.get("python", 50) * 0.15 +
        scores.get("sql", 40) * 0.10 +
        scores.get("backend", 45) * 0.15 +
        scores.get("ai_ml", 35) * 0.10 +
        scores.get("projects", 50) * 0.15 +
        scores.get("dsa", 40) * 0.15 +
        scores.get("communication", 50) * 0.10 +
        scores.get("hr", 50) * 0.10,
        1
    )

    if profile:
        profile.readiness_score = overall_readiness
        db.session.commit()

    weaknesses = Weakness.query.filter_by(user_id=user_id).order_by(Weakness.next_review_at.asc()).all()
    sessions = InterviewSession.query.filter_by(user_id=user_id).order_by(InterviewSession.created_at.desc()).limit(5).all()

    return jsonify({
        "readiness_score": overall_readiness,
        "readiness_label": "Interview Ready" if overall_readiness >= 76 else ("Almost Ready" if overall_readiness >= 61 else ("Needs Improvement" if overall_readiness >= 41 else "Not Ready")),
        "category_scores": scores,
        "streak": profile.current_streak if profile else 1,
        "target_role": profile.target_role if profile else "Junior Python Developer",
        "daily_goal_minutes": profile.daily_goal_minutes if profile else 60,
        "weaknesses_count": len(weaknesses),
        "weaknesses": [w.to_dict() for w in weaknesses[:5]],
        "recent_sessions": [s.to_dict() for s in sessions]
    })

@dashboard_bp.route('/daily-plan', methods=['GET'])
def get_daily_plan():
    user_id = session.get('user_id', 1)
    user = User.query.get(user_id)
    profile = user.profile if user else None
    goal = profile.daily_goal_minutes if profile else 60

    plan_items = [
        {"id": 1, "time_min": 10, "category": "Revision", "title": "Spaced Revision: SQL JOINs & MySQL Indexing", "status": "Pending"},
        {"id": 2, "time_min": 15, "category": "Python", "title": "Python Concept: Generators & Yield Deep Dive", "status": "Pending"},
        {"id": 3, "time_min": 15, "category": "DSA", "title": "DSA Challenge: Valid Palindrome (Two Pointers)", "status": "Pending"},
        {"id": 4, "time_min": 15, "category": "Project Defense", "title": "Project Defense: AI Skin Analysis (MobileNetV2 vs Mock Scores)", "status": "Pending"},
        {"id": 5, "time_min": 15, "category": "Voice Mock", "title": "15-Min Voice Interview: Backend & FastAPI Security", "status": "Pending"}
    ]

    return jsonify({"goal_minutes": goal, "plan": plan_items})

@dashboard_bp.route('/jd-match', methods=['POST'])
def match_jd():
    data = request.json or {}
    jd_text = data.get('job_description', '')
    if not jd_text:
        return jsonify({"error": "Please paste a job description."}), 400

    user_id = session.get('user_id', 1)
    user = User.query.get(user_id)
    profile = user.profile.to_dict() if user and user.profile else {}

    res = groq_service.analyze_job_description(jd_text, profile)
    return jsonify(res)
