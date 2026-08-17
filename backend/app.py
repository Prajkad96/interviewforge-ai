import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from config import Config
from extensions import db
from models import User, UserProfile
from seed_data import seed_initial_data


from routes.auth_routes import auth_bp
from routes.interview_routes import interview_bp
from routes.project_routes import project_bp
from routes.learn_routes import learn_bp
from routes.dsa_routes import dsa_bp
from routes.dashboard_routes import dashboard_bp

def create_app():
    static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    app = Flask(__name__, static_folder=static_folder, static_url_path='')
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(learn_bp)
    app.register_blueprint(dsa_bp)
    app.register_blueprint(dashboard_bp)

    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/favicon.ico')
    def favicon():
        return jsonify({"status": "ok"}), 200

    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "service": "INTERVIEWFORGE AI Core API"})

    with app.app_context():
        db.create_all()
        seed_initial_data()

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    print(f"INTERVIEWFORGE AI backend running on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
