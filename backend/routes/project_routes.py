from flask import Blueprint, jsonify, request
from services.project_kb_service import project_kb_service

project_bp = Blueprint('project', __name__, url_prefix='/api/projects')

@project_bp.route('/', methods=['GET'])
def get_projects():
    return jsonify({"projects": project_kb_service.get_all_projects()})

@project_bp.route('/<slug>', methods=['GET'])
def get_project_by_slug(slug):
    proj = project_kb_service.get_project_by_slug(slug)
    if not proj:
        return jsonify({"error": "Project not found."}), 404
    return jsonify({"project": proj})
