from extensions import db
from models import User, UserProfile, ProjectKnowledge, Topic, DSAProblem
from services.project_kb_service import PROJECTS_DATABASE
from services.curriculum_service import CURRICULUM_DATA
from services.dsa_service import DSA_PROBLEMS_DATABASE
import json

def seed_initial_data():
    # 1. Seed Candidate User
    user = User.query.filter_by(username="Prajakta").first()
    if not user:
        user = User(username="Prajakta", email="prajaktakadalagekar72@gmail.com")
        user.set_password("prajakta123")
        db.session.add(user)
        db.session.commit()

        profile = UserProfile(
            user_id=user.id,
            target_role="Junior Python / Backend Developer",
            daily_goal_minutes=60,
            current_streak=3,
            readiness_score=68.5
        )
        db.session.add(profile)
        db.session.commit()

    # 2. Seed Projects Knowledge Base
    for p in PROJECTS_DATABASE:
        existing = ProjectKnowledge.query.filter_by(project_slug=p["project_slug"]).first()
        if not existing:
            pk = ProjectKnowledge(
                project_slug=p["project_slug"],
                title=p["title"],
                repo_url=p["repo_url"],
                tech_stack_json=json.dumps(p["tech_stack"]),
                architecture_summary=p["architecture_summary"],
                implemented_features_json=json.dumps(p["implemented_features"]),
                security_audits_json=json.dumps(p["security_audits"]),
                questions_json=json.dumps(p["questions"])
            )
            db.session.add(pk)
    db.session.commit()

    # 3. Seed Curriculum Topics
    for t in CURRICULUM_DATA:
        existing = Topic.query.filter_by(slug=t["slug"]).first()
        if existing:
            existing.category = t["category"]
            existing.title = t["title"]
            existing.difficulty = t["difficulty"]
            existing.summary = t["summary"]
            existing.sec_30_answer = t["sec_30_answer"]
            existing.min_1_answer = t["min_1_answer"]
            existing.deep_dive_answer = t["deep_dive_answer"]
            existing.common_mistakes_json = json.dumps(t["common_mistakes"])
        else:
            top = Topic(
                category=t["category"],
                slug=t["slug"],
                title=t["title"],
                difficulty=t["difficulty"],
                summary=t["summary"],
                sec_30_answer=t["sec_30_answer"],
                min_1_answer=t["min_1_answer"],
                deep_dive_answer=t["deep_dive_answer"],
                common_mistakes_json=json.dumps(t["common_mistakes"])
            )
            db.session.add(top)
        db.session.commit()

    # 4. Seed DSA Problems
    for d in DSA_PROBLEMS_DATABASE:
        existing = DSAProblem.query.filter_by(slug=d["slug"]).first()
        if not existing:
            dsa = DSAProblem(
                slug=d["slug"],
                title=d["title"],
                category=d["category"],
                difficulty=d["difficulty"],
                description=d["description"],
                starter_code=d["starter_code"],
                solution_code=d["solution_code"],
                test_cases_json=json.dumps(d["test_cases"]),
                hints_json=json.dumps(d["hints"])
            )
            db.session.add(dsa)
    db.session.commit()
    print("Database successfully seeded with initial candidate projects, curriculum, and DSA problem bank.")
