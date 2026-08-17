from flask import Blueprint, request, jsonify, session
from extensions import db
from models import User, UserProfile
from services.groq_service import groq_service

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields."}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "Username or Email already exists."}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    profile = UserProfile(user_id=user.id)
    db.session.add(profile)
    db.session.commit()

    session['user_id'] = user.id
    return jsonify({"message": "Registration successful", "user": user.to_dict(), "profile": profile.to_dict()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    email_or_user = data.get('email', '').strip()
    password = data.get('password', '')

    user = User.query.filter((User.username == email_or_user) | (User.email == email_or_user.lower())).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password."}), 401

    session['user_id'] = user.id
    profile = user.profile or UserProfile(user_id=user.id)
    return jsonify({"message": "Login successful", "user": user.to_dict(), "profile": profile.to_dict()})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        # Default candidate profile for instant demo access
        user = User.query.first()
        if not user:
            user = User(username="Prajakta", email="prajakta@interviewforge.ai")
            user.set_password("prajakta123")
            db.session.add(user)
            db.session.commit()
            profile = UserProfile(user_id=user.id)
            db.session.add(profile)
            db.session.commit()
        session['user_id'] = user.id

    user = User.query.get(session['user_id'])
    profile = user.profile.to_dict() if user.profile else {}
    return jsonify({
        "user": user.to_dict(),
        "profile": profile,
        "groq": groq_service.get_info()
    })

@auth_bp.route('/groq-key', methods=['POST'])
def set_groq_key():
    data = request.json or {}
    key = data.get('groq_api_key', '')
    groq_service.set_api_key(key)
    return jsonify({"message": "Groq API Key updated successfully", "groq": groq_service.get_info()})
