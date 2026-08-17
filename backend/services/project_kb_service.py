import json

PROJECTS_DATABASE = [
    {
        "project_slug": "skin-analysis-ai",
        "title": "AI-Based Skin Analysis Application",
        "repo_url": "https://github.com/Prajkad96/Skin-Analysis-AI",
        "tech_stack": ["Python", "Flask", "OpenCV", "TensorFlow", "MobileNetV2", "SQLite", "Flask-SQLAlchemy", "JavaScript", "HTML/CSS"],
        "architecture_summary": "Full-stack web application with base64 camera image capture, OpenCV Haar cascades face detection, CLAHE enhancement, and MobileNetV2 inference pipeline.",
        "implemented_features": [
            "Camera image acquisition & multi-view handling (front, left, right views)",
            "OpenCV enhancement pipeline (Haar Cascades, LAB space CLAHE, Laplacian denoising)",
            "MobileNetV2 model loading via TensorFlow/Keras with ImageNet weights",
            "User registration/login with Werkzeug password hashing",
            "Consultation booking & progress tracking timeline in SQLite"
        ],
        "security_audits": [
            "CRITICAL SECURITY ISSUE: Hardcoded secret key `app.secret_key = 'your_secret_key'` in `app.py`.",
            "CRITICAL DATA LOSS ISSUE: Startup routine in `app.py` executes `db.drop_all()` and `db.create_all()`, destroying all stored SQLite user data on every app launch.",
            "IMPLEMENTATION SCENARIO: MobileNetV2 model is loaded with ImageNet weights, but skin condition scores (`acne`, `eczema`, etc.) are generated using `np.random.uniform()` mock random values rather than a trained classification head."
        ],
        "questions": [
            {
                "level": 1,
                "type": "IMPLEMENTED FEATURE",
                "question": "What does your AI Skin Analysis application do and what is its core workflow?",
                "expected": "Takes user face images via web camera/file upload, processes images with OpenCV, evaluates skin health, and stores progress history."
            },
            {
                "level": 2,
                "type": "INTERVIEW SCENARIO",
                "question": "In your code, MobileNetV2 is initialized with ImageNet weights, but skin condition scores are generated using `np.random.uniform()`. Why did you use mock random scores here?",
                "expected": "ImageNet classifies 1000 general categories (dogs, cars), not dermatological conditions. For demonstration, random scores simulated condition predictions before training a custom fine-tuned classification head."
            },
            {
                "level": 3,
                "type": "SECURITY AUDIT",
                "question": "I noticed line 784 of app.py executes `db.drop_all()` and `db.create_all()` inside `app.app_context()`. What happens when the app restarts in production?",
                "expected": "All existing user data, consultations, and progress logs are completely erased. In production, database migrations (like Flask-Migrate / Alembic) must be used instead."
            },
            {
                "level": 4,
                "type": "HOW IT WORKS INTERNALLY",
                "question": "Explain the image enhancement pipeline in your project before inference.",
                "expected": "Image converted to LAB color space, CLAHE (Contrast Limited Adaptive Histogram Equalization) applied to L channel for brightness correction, followed by OpenCV Laplacian variance check and bilateral/NLMeans denoising."
            },
            {
                "level": 5,
                "type": "HYPOTHETICAL IMPROVEMENT",
                "question": "How would you redesign the inference architecture if 10,000 users upload skin images simultaneously?",
                "expected": "Decouple image processing from web server using an asynchronous task queue (Celery + Redis), store uploads on S3, run GPU model inference as a dedicated microservice, and push results via WebSockets/polling."
            }
        ]
    },
    {
        "project_slug": "skincare-chatbot",
        "title": "Skincare AI Advisor Chatbot",
        "repo_url": "https://github.com/Prajkad96/skincare-chatbot",
        "tech_stack": ["Python", "Flask", "Google Gemini API (google-genai SDK)", "JavaScript", "HTML/CSS"],
        "architecture_summary": "Lightweight Flask web application integrating Google Gemini 2.5 Flash API with domain-specific system context prompting for skincare advisory.",
        "implemented_features": [
            "Flask route POST `/chat` interfacing with `google-genai` SDK",
            "Gemini 2.5 Flash model prompt execution (`client.models.generate_content`)",
            "System prompt defining specialized persona for 6 skin conditions",
            "Error handling matching strings for 429 rate limit and 503 service unavailable"
        ],
        "security_audits": [
            "SECURITY ISSUE: The `/chat` API endpoint lacks authentication, allowing unauthenticated requests to exhaust Gemini API quota.",
            "LIMITATION: Chat is stateless; conversation history is not retained or passed back in requests."
        ],
        "questions": [
            {
                "level": 1,
                "type": "IMPLEMENTED FEATURE",
                "question": "Why did you choose Google Gemini 2.5 Flash for your skincare chatbot?",
                "expected": "Gemini 2.5 Flash is lightweight, low-latency, cost-efficient, and capable of fast text generation with domain-specific system prompting."
            },
            {
                "level": 2,
                "type": "HOW IT WORKS INTERNALLY",
                "question": "How does your chatbot send requests to Gemini and handle conversation context?",
                "expected": "In `app.py`, system context string is prepended directly to `user_message`. Requests are single-turn stateless `generate_content` calls."
            },
            {
                "level": 3,
                "type": "HYPOTHETICAL IMPROVEMENT",
                "question": "How would you maintain multi-turn chat history without ballooning token costs?",
                "expected": "Store recent conversation history array in session/Redis, pass structured contents messages, and summarize older context when token limits are approached."
            },
            {
                "level": 4,
                "type": "SECURITY AUDIT",
                "question": "What happens if a user submits prompt injection attacks or medical advice queries that could cause hallucinations?",
                "expected": "System instruction needs strict guardrails and medical disclaimers, plus input validation and fallback responses for out-of-scope advice."
            }
        ]
    },
    {
        "project_slug": "job-tracker",
        "title": "Job Application Tracker",
        "repo_url": "https://github.com/Prajkad96/job-tracker",
        "tech_stack": ["Python", "Flask", "MySQL", "Flask-Login", "Werkzeug", "JavaScript"],
        "architecture_summary": "Full-stack job tracking application with Flask-Login session authentication, MySQL relational database with foreign keys, and per-user data isolation.",
        "implemented_features": [
            "Flask-Login authentication (`UserMixin`, `login_user`, `@login_required`)",
            "MySQL database schema with `users` and `applications` table (`FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`)",
            "Password hashing using Werkzeug `generate_password_hash` / `check_password_hash`",
            "User data isolation enforcing `WHERE user_id = current_user.id` on all queries",
            "CRUD status pipeline (Applied → Interview → Offered → Rejected) with dashboard stats"
        ],
        "security_audits": [
            "CRITICAL SECURITY VULNERABILITY: The `/forgot-password` route accepts POST with `email` and `new_password` without OTP or email token verification, allowing unauthorized password resets for any user."
        ],
        "questions": [
            {
                "level": 1,
                "type": "IMPLEMENTED FEATURE",
                "question": "How does Flask-Login manage session state in your Job Tracker application?",
                "expected": "`@login_manager.user_loader` queries MySQL for the user ID stored in the session cookie, instantiating the `User` object for `current_user`."
            },
            {
                "level": 2,
                "type": "HOW IT WORKS INTERNALLY",
                "question": "How do you enforce user data isolation so User A cannot see User B's job applications?",
                "expected": "All SQL query statements explicitly append `WHERE user_id = %s` bound to `current_user.id`, combined with database foreign key constraints."
            },
            {
                "level": 3,
                "type": "SECURITY AUDIT",
                "question": "Your `/forgot-password` endpoint directly updates `password_hash` when given an email and new password. Why is this insecure and how would you fix it?",
                "expected": "Anyone can reset any user's password without proof of email ownership. Fix: Send a cryptographically signed timed token via email (e.g. `itsdangerous` or SendGrid) before allowing password updates."
            },
            {
                "level": 4,
                "type": "WHAT WOULD YOU IMPROVE",
                "question": "Which database columns would you index to speed up dashboard filtering and search?",
                "expected": "Create composite index on `(user_id, status)` and index on `user_id` for join performance."
            }
        ]
    },
    {
        "project_slug": "healthpredict-ai",
        "title": "HealthPredict AI Application",
        "repo_url": "https://github.com/Prajkad96/Health-Prediction-Application",
        "tech_stack": ["Python", "Flask", "MySQL", "Google Gemini API", "Flask-CORS", "JavaScript"],
        "architecture_summary": "Patient medical record management REST API with automated Gemini AI disease risk assessment generation from blood test metrics.",
        "implemented_features": [
            "REST API endpoints (`/api/patients` GET, POST, PUT, DELETE)",
            "Gemini AI integration (`generate_health_remarks`) analyzing glucose, haemoglobin, and cholesterol",
            "Regex email validation and DOB date/future validation",
            "Environment configuration loading (`load_dotenv`)"
        ],
        "security_audits": [
            "CRITICAL SECURITY ISSUE: No authentication middleware exists on any patient API endpoint; anyone can view, edit, or delete patient records.",
            "VALIDATION ISSUE: Numeric metrics (`glucose`, `haemoglobin`, `cholesterol`) are not validated for numeric ranges or negative bounds."
        ],
        "questions": [
            {
                "level": 1,
                "type": "IMPLEMENTED FEATURE",
                "question": "How does HealthPredict AI generate disease risk assessments from blood test results?",
                "expected": "The POST/PUT endpoints format patient metrics into a prompt sent to `gemini-flash-latest`, generating a 2-3 sentence AI remark stored in MySQL `patients.remarks`."
            },
            {
                "level": 2,
                "type": "SECURITY AUDIT",
                "question": "What is the biggest security issue in your `/api/patients` REST API implementation?",
                "expected": "All CRUD endpoints lack authentication/authorization. Anyone can send `DELETE /api/patients/<id>` or modify medical records."
            },
            {
                "level": 3,
                "type": "VALIDATION & ERROR HANDLING",
                "question": "What happens if a user submits `glucose = -500` or `haemoglobin = 'abc'`?",
                "expected": "Missing numeric bounds validation means negative or invalid types corrupt the AI prompt or cause DB insertion exceptions. Must validate with Pydantic/Marshmallow or explicit float range checks."
            }
        ]
    },
    {
        "project_slug": "college-placement-portal",
        "title": "College Placement Cell Portal",
        "repo_url": "https://github.com/Prajkad96/College-Placement-Portal",
        "tech_stack": ["Python", "Flask", "MySQL", "HTML/CSS"],
        "architecture_summary": "Role-based web portal for college students and Training & Placement Officers (TPO) to post and review campus job opportunities.",
        "implemented_features": [
            "Dual-role portal (Student dashboard & TPO dashboard)",
            "TPO job posting CRUD (`job_postings` table with `title`, `company`, `description`, `deadline`)",
            "Student resume file upload (`uploads/` folder using `secure_filename`)"
        ],
        "security_audits": [
            "CRITICAL SECURITY VULNERABILITY: Passwords are stored in PLAINTEXT in MySQL database (`SELECT * FROM {table} WHERE email=%s AND password=%s`). No password hashing function is used.",
            "DATA PERSISTENCE ISSUE: `/apply_job` route returns a success message but does NOT write application records to a database table.",
            "SESSION ISSUE: `session['userType']` is set, but `user_id` is never saved in the session."
        ],
        "questions": [
            {
                "level": 1,
                "type": "SECURITY AUDIT",
                "question": "In Placement Portal, lines 67, 110, and 137 store and compare passwords in plaintext. Why is this extremely dangerous?",
                "expected": "If database access is compromised, all user passwords are exposed. Passwords must always be salted and hashed using strong algorithms like bcrypt, Argon2, or PBKDF2."
            },
            {
                "level": 2,
                "type": "INTERVIEW SCENARIO",
                "question": "Your `/apply_job` route returns 'Application submitted successfully', but doesn't write to MySQL. How would you design an `applications` table for student job applications?",
                "expected": "Create `student_applications` table with `id`, `student_id (FK -> students.id)`, `job_id (FK -> job_postings.id)`, `applied_at`, `status`, and unique constraint on `(student_id, job_id)`."
            }
        ]
    },
    {
        "project_slug": "sweet-shop-management-system",
        "title": "Sweet Shop Management System",
        "repo_url": "https://github.com/Prajkad96/sweet-shop-management-system",
        "tech_stack": ["Python", "FastAPI", "SQLAlchemy", "SQLite", "Pydantic v2", "JWT (python-jose)", "JavaScript", "HTML/CSS"],
        "architecture_summary": "RESTful API built with FastAPI, SQLAlchemy ORM, and Pydantic schemas, featuring JWT authentication and role-based admin authorization for inventory management.",
        "implemented_features": [
            "FastAPI async framework with Pydantic v2 schemas (`model_dump()`)",
            "JWT bearer token authentication (`jose.jwt`) with 24-hour expiration",
            "Role-based authorization via FastAPI dependency injection (`Depends(get_admin_user)`)",
            "SQLAlchemy ORM models with unique constraints and dynamic index creation",
            "Inventory purchasing and restocking endpoints (`/api/sweets/{id}/purchase`)"
        ],
        "security_audits": [
            "CONCURRENCY / RACE CONDITION ISSUE: The `/purchase` endpoint reads `sweet.quantity`, checks stock, subtracts, and commits. Under concurrent requests, two users can buy the last item simultaneously resulting in negative stock or double sales."
        ],
        "questions": [
            {
                "level": 1,
                "type": "WHY DID YOU CHOOSE THIS",
                "question": "Why did you choose FastAPI over Flask for the Sweet Shop Management System?",
                "expected": "FastAPI provides automatic OpenAPI docs, high performance with async support, strict data validation using Pydantic, and clean dependency injection."
            },
            {
                "level": 2,
                "type": "HOW IT WORKS INTERNALLY",
                "question": "How does dependency injection work in your FastAPI JWT authorization?",
                "expected": "`get_current_user` depends on `HTTPBearer` security, decodes JWT token, fetches user from SQLAlchemy DB, and passes `current_user` to endpoint functions."
            },
            {
                "level": 3,
                "type": "DEBUGGING / CONCURRENCY",
                "question": "In `/api/sweets/{id}/purchase`, what happens if two users attempt to purchase the last remaining item at the exact same millisecond? How do you prevent it?",
                "expected": "Race condition occurs. Solution: Use database row locking (`with_for_update()`) in SQLAlchemy, or atomic SQL update `UPDATE sweets SET quantity = quantity - %s WHERE id = %s AND quantity >= %s`."
            }
        ]
    }
]

class ProjectKBService:
    def get_all_projects(self):
        return PROJECTS_DATABASE

    def get_project_by_slug(self, slug):
        for p in PROJECTS_DATABASE:
            if p["project_slug"] == slug:
                return p
        return None

project_kb_service = ProjectKBService()
