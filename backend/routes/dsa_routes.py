from flask import Blueprint, request, jsonify, session
from extensions import db
from models import DSASubmission, DSAProblem
from services.dsa_service import dsa_service

dsa_bp = Blueprint('dsa', __name__, url_prefix='/api/dsa')

@dsa_bp.route('/problems', methods=['GET'])
def get_problems():
    return jsonify({"problems": dsa_service.get_all_problems()})

@dsa_bp.route('/problems/<slug>', methods=['GET'])
def get_problem(slug):
    prob = dsa_service.get_problem_by_slug(slug)
    if not prob:
        return jsonify({"error": "Problem not found."}), 404
    return jsonify({"problem": prob})

@dsa_bp.route('/execute', methods=['POST'])
def execute_code():
    data = request.json or {}
    slug = data.get('slug')
    code = data.get('code', '')
    user_id = session.get('user_id', 1)

    if not slug or not code:
        return jsonify({"error": "Missing problem slug or code."}), 400

    result = dsa_service.execute_user_code(slug, code)

    # Save submission
    problem = dsa_service.get_problem_by_slug(slug)
    if problem:
        prob_db = DSAProblem.query.filter_by(slug=slug).first()
        if prob_db:
            sub = DSASubmission(
                user_id=user_id,
                problem_id=prob_db.id,
                code=code,
                status=result.get("status", "Failed"),
                feedback=f"Passed {sum(1 for r in result.get('test_results', []) if r['passed'])}/{len(result.get('test_results', []))} test cases."
            )
            db.session.add(sub)
            db.session.commit()

    return jsonify(result)
