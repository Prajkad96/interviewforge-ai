from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    sessions = db.relationship('InterviewSession', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    dsa_attempts = db.relationship('DSASubmission', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    weaknesses = db.relationship('Weakness', backref='user', lazy='dynamic', cascade="all, delete-orphan")


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    target_role = db.Column(db.String(100), default="Junior Python Developer")
    daily_goal_minutes = db.Column(db.Integer, default=60)
    current_streak = db.Column(db.Integer, default=1)
    last_active_date = db.Column(db.String(20), default=datetime.utcnow().strftime('%Y-%m-%d'))
    readiness_score = db.Column(db.Float, default=45.0)
    
    # Category score JSON strings
    scores_json = db.Column(db.Text, default='{"python": 50, "sql": 40, "backend": 45, "ai_ml": 35, "projects": 50, "dsa": 40, "communication": 50, "hr": 50}')

    def get_scores(self):
        try:
            return json.loads(self.scores_json)
        except Exception:
            return {"python": 50, "sql": 40, "backend": 45, "ai_ml": 35, "projects": 50, "dsa": 40, "communication": 50, "hr": 50}

    def set_scores(self, scores_dict):
        self.scores_json = json.dumps(scores_dict)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "target_role": self.target_role,
            "daily_goal_minutes": self.daily_goal_minutes,
            "current_streak": self.current_streak,
            "last_active_date": self.last_active_date,
            "readiness_score": self.readiness_score,
            "scores": self.get_scores()
        }

class ProjectKnowledge(db.Model):
    __tablename__ = 'project_knowledge'
    id = db.Column(db.Integer, primary_key=True)
    project_slug = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    repo_url = db.Column(db.String(255))
    tech_stack_json = db.Column(db.Text)
    architecture_summary = db.Column(db.Text)
    implemented_features_json = db.Column(db.Text)
    security_audits_json = db.Column(db.Text)
    questions_json = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "project_slug": self.project_slug,
            "title": self.title,
            "repo_url": self.repo_url,
            "tech_stack": json.loads(self.tech_stack_json or "[]"),
            "architecture_summary": self.architecture_summary,
            "implemented_features": json.loads(self.implemented_features_json or "[]"),
            "security_audits": json.loads(self.security_audits_json or "[]"),
            "questions": json.loads(self.questions_json or "[]")
        }

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False) # python, sql, backend, ai_ml, hr, dsa
    slug = db.Column(db.String(80), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    summary = db.Column(db.Text)
    notes_markdown = db.Column(db.Text)
    sec_30_answer = db.Column(db.Text)
    min_1_answer = db.Column(db.Text)
    deep_dive_answer = db.Column(db.Text)
    common_mistakes_json = db.Column(db.Text)
    difficulty = db.Column(db.String(20), default="Easy") # Easy, Medium, Hard

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "slug": self.slug,
            "title": self.title,
            "summary": self.summary,
            "notes_markdown": self.notes_markdown,
            "sec_30_answer": self.sec_30_answer,
            "min_1_answer": self.min_1_answer,
            "deep_dive_answer": self.deep_dive_answer,
            "common_mistakes": json.loads(self.common_mistakes_json or "[]"),
            "difficulty": self.difficulty
        }

class DSAProblem(db.Model):
    __tablename__ = 'dsa_problems'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False) # Arrays, Strings, Two Pointers, Stack, Queue, Linked List, Binary Search
    difficulty = db.Column(db.String(20), default="Easy")
    description = db.Column(db.Text, nullable=False)
    starter_code = db.Column(db.Text)
    solution_code = db.Column(db.Text)
    test_cases_json = db.Column(db.Text) # List of {"input": ..., "expected": ...}
    hints_json = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "category": self.category,
            "difficulty": self.difficulty,
            "description": self.description,
            "starter_code": self.starter_code,
            "test_cases": json.loads(self.test_cases_json or "[]"),
            "hints": json.loads(self.hints_json or "[]")
        }

class DSASubmission(db.Model):
    __tablename__ = 'dsa_submissions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('dsa_problems.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30)) # Passed, Failed, Error
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    problem = db.relationship('DSAProblem')

class InterviewSession(db.Model):
    __tablename__ = 'interview_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    session_type = db.Column(db.String(50), nullable=False) # Quick 15, Technical 30, Full 60, Project Grill, Resume Grill, JD Round
    target_role = db.Column(db.String(100))
    overall_score = db.Column(db.Float, default=0.0)
    summary_feedback = db.Column(db.Text)
    hiring_signal = db.Column(db.String(50), default="Pending") # Strong Hire, Hire, Borderline, Weak, Do Not Hire Yet
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attempts = db.relationship('QuestionAttempt', backref='session', lazy='dynamic', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "session_type": self.session_type,
            "target_role": self.target_role,
            "overall_score": self.overall_score,
            "summary_feedback": self.summary_feedback,
            "hiring_signal": self.hiring_signal,
            "created_at": self.created_at.isoformat(),
            "questions_count": self.attempts.count()
        }

class QuestionAttempt(db.Model):
    __tablename__ = 'question_attempts'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('interview_sessions.id', ondelete='CASCADE'), nullable=False)
    category = db.Column(db.String(50)) # Python, SQL, Backend, AI/ML, Project, HR, DSA
    question_text = db.Column(db.Text, nullable=False)
    user_transcript = db.Column(db.Text)
    audio_seconds = db.Column(db.Float, default=0.0)
    score = db.Column(db.Integer, default=0) # 0 to 5
    technical_accuracy = db.Column(db.Integer, default=0)
    communication_score = db.Column(db.Integer, default=0)
    feedback_json = db.Column(db.Text) # {"missing_points": [...], "mistakes": [...], "interview_ready_answer": "..."}
    follow_up_question = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "category": self.category,
            "question_text": self.question_text,
            "user_transcript": self.user_transcript,
            "score": self.score,
            "technical_accuracy": self.technical_accuracy,
            "communication_score": self.communication_score,
            "feedback": json.loads(self.feedback_json or "{}"),
            "follow_up_question": self.follow_up_question,
            "created_at": self.created_at.isoformat()
        }

class Weakness(db.Model):
    __tablename__ = 'weaknesses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    topic_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    mistake_summary = db.Column(db.Text)
    review_stage = db.Column(db.Integer, default=1) # 1=Same day, 2=Next day, 3=3 days, 4=7 days, 5=Mastered
    last_reviewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    next_review_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "topic_name": self.topic_name,
            "category": self.category,
            "mistake_summary": self.mistake_summary,
            "review_stage": self.review_stage,
            "last_reviewed_at": self.last_reviewed_at.isoformat(),
            "next_review_at": self.next_review_at.isoformat()
        }
