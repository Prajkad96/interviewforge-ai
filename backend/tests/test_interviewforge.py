import unittest
import os
import sys

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from models import User, UserProfile, ProjectKnowledge, Topic, DSAProblem
from services.project_kb_service import project_kb_service
from services.dsa_service import dsa_service
from services.groq_service import groq_service

class TestInterviewForge(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_health_check(self):
        res = self.client.get('/health')
        self.assertEqual(res.status_code, 200)
        self.assertIn("healthy", res.get_json()['status'])

    def test_project_kb_audit(self):
        projects = project_kb_service.get_all_projects()
        self.assertEqual(len(projects), 6)
        
        # Verify MobileNetV2 mock score audit in Skin Analysis AI
        skin_proj = project_kb_service.get_project_by_slug("skin-analysis-ai")
        self.assertIsNotNone(skin_proj)
        self.assertIn("MobileNetV2", skin_proj['tech_stack'])

        # Verify plaintext password audit in Placement Portal
        placement_proj = project_kb_service.get_project_by_slug("college-placement-portal")
        self.assertIsNotNone(placement_proj)
        self.assertTrue(any("PLAINTEXT" in a for a in placement_proj['security_audits']))

    def test_dsa_code_execution(self):
        valid_code = "def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target - n], i]\n        seen[n] = i\n    return []"
        res = dsa_service.execute_user_code("two-sum", valid_code)
        self.assertEqual(result := res.get('status'), "Passed")

    def test_groq_fallback_evaluation(self):
        eval_res = groq_service.evaluate_answer(
            question="Why did you choose Flask for your skin analysis application?",
            user_answer="Flask is lightweight, flexible, and provides easy routing for rapid web development."
        )
        self.assertIn("score", eval_res)
        self.assertGreaterEqual(eval_res['score'], 0)
        self.assertLessEqual(eval_res['score'], 5)

if __name__ == '__main__':
    unittest.main()
