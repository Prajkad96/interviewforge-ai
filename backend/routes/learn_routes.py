from flask import Blueprint, jsonify
from services.curriculum_service import curriculum_service

learn_bp = Blueprint('learn', __name__, url_prefix='/api/learn')

@learn_bp.route('/topics', methods=['GET'])
def get_topics():
    return jsonify({"topics": curriculum_service.get_all_topics()})

@learn_bp.route('/topics/<slug>', methods=['GET'])
def get_topic(slug):
    topic = curriculum_service.get_topic_by_slug(slug)
    if not topic:
        return jsonify({"error": "Topic not found."}), 404
    return jsonify({"topic": topic})
