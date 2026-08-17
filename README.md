# ⚡ InterviewForge AI

> Learn. Speak. Code. Defend. Improve. Get Hired.

InterviewForge AI is a voice-first AI interview preparation platform designed for freshers and junior software developers preparing for Python, Backend, AI/ML, SQL, DSA, and Software Engineering interviews.

Instead of only providing interview questions, InterviewForge AI follows a complete preparation cycle:

**Learn → Practice → Speak → Get Grilled → Get Feedback → Revise → Retest → Track Progress**

---

## 🚀 Features

### 🎙️ Voice-Based Mock Interviews

Practice interviews without typing answers.

- Voice-based interview interaction
- Speech-to-text answers
- AI-generated interview questions
- AI-based answer evaluation
- Follow-up questions
- Technical and communication feedback

---

### 🧠 AI Interviewer

InterviewForge AI uses the **Groq Cloud API** for AI-powered interview generation and evaluation.

The interviewer can evaluate:

- Technical accuracy
- Concept understanding
- Problem-solving ability
- Communication
- Completeness of answers
- Interview performance

The interviewer can also ask deeper follow-up questions when an answer is incomplete.

---

### 🔥 Strict Interview Mode

The interviewer is designed to challenge the candidate instead of simply accepting basic answers.

It can ask:

- Why did you choose this approach?
- How does it work internally?
- What are its limitations?
- How would you improve it?
- What happens in an edge case?
- How would you debug it?
- How would you make it production-ready?

---

### 📄 Resume-Based Interview Preparation

InterviewForge AI can use the candidate's resume and skills as a foundation for interview preparation.

Questions can be generated around:

- Python
- Flask
- Backend Development
- AI/ML
- Generative AI
- SQL
- DSA
- Projects
- Certifications
- Other technical skills

---

### 💻 Project Defense

Project-specific interview preparation is one of the core features of InterviewForge AI.

The interviewer can ask questions about:

- Project architecture
- Technology choices
- Database design
- APIs
- Authentication
- AI/ML implementation
- Error handling
- Security
- Performance
- Scalability
- Limitations
- Future improvements

The goal is to help candidates confidently explain and defend the projects listed on their resumes.

---

### 🧩 DSA Practice

InterviewForge includes fresher-focused DSA practice.

Topics include:

- Arrays
- Strings
- Hash Maps
- Searching
- Sorting
- Two Pointers
- Sliding Window
- Stack
- Queue
- Linked Lists
- Recursion
- Basic Trees
- Basic Dynamic Programming

The focus is on practical technical-interview preparation rather than competitive programming.

---

### 🗄️ SQL Practice

SQL preparation includes:

- SELECT
- WHERE
- GROUP BY
- ORDER BY
- Aggregate Functions
- JOINs
- Subqueries
- CASE
- NULL handling
- Database concepts
- Basic Window Functions

The goal is to help candidates both **write SQL queries and explain their logic during interviews**.

---

### 📚 Learning Platform

InterviewForge is designed to combine learning and interview practice in one platform.

Learning areas include:

- Python
- SQL
- DSA
- Flask
- Django
- REST APIs
- Git/GitHub
- AI/ML
- Generative AI
- Backend Development
- Software Engineering
- Interview Preparation



### 🔄 Revision

InterviewForge is designed around the idea that an incorrect answer should become a future learning opportunity.

Weak areas can be identified from:

- Incorrect interview answers
- Low interview scores
- Failed coding problems
- Quiz results
- Repeated mistakes
- Weak project explanations

These weaknesses can then be used for future revision and practice.

---

### 📊 Progress Tracking

The platform tracks preparation across areas such as:

- Python
- SQL
- Backend
- AI/ML
- DSA
- Projects
- Communication
- Interview performance

The goal is to help candidates understand their strengths, weaknesses, and overall interview readiness.

---

## 🎯 Interview Preparation Workflow

        LEARN
          ↓
       PRACTICE
          ↓
        SPEAK
          ↓
     GET GRILLED
          ↓
       FEEDBACK
          ↓
        REVISE
          ↓
        RETEST
          ↓
       IMPROVE
          ↓
        REPEAT


🛠️ Technology Stack
Backend
Python
Flask
Flask-SQLAlchemy
REST APIs
AI
Groq Cloud API
LLM-based interview generation
AI-based answer evaluation
Frontend
HTML
CSS
JavaScript
Web Speech API
Database
SQLite for development
Testing
Python testing tools
Flask test client
🏗️ Project Structure
interviewforge-ai/
│
├── backend/
│   ├── routes/
│   ├── services/
│   ├── tests/
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── requirements.txt
│   └── seed_data.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── index.html
│
├── .env.example
├── README.md
└── requirements.txt
⚙️ Installation
1. Clone the repository
git clone https://github.com/Prajkad96/interviewforge-ai.git
cd interviewforge-ai
2. Create a virtual environment

Windows:

python -m venv venv
venv\Scripts\activate

Linux/macOS:

python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt

If the required dependencies are maintained inside the backend folder:

pip install -r backend/requirements.txt
4. Configure environment variables

Create a .env file using .env.example as a reference.

Example:

GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key

Never commit your .env file or API keys to GitHub.

5. Run the application
python backend/app.py

Open the local URL displayed by Flask in your browser.

🤖 Groq Cloud API

InterviewForge AI uses the Groq Cloud API for AI-powered interview generation and evaluation.

You need your own Groq API key to use the AI features.

Store the API key securely using environment variables.

🔐 Security

Sensitive configuration should never be stored directly in source code.

The repository should contain:

.env.example

but should not contain:

.env
API keys
Passwords
Database credentials
Secret tokens
📌 Current Status

InterviewForge AI is currently an MVP under active development.

Implemented
 Flask backend
 Groq AI integration
 AI-powered interview functionality
 Voice-based interview interaction
 Interview evaluation
 Resume/project interview preparation
 DSA practice interface
 SQL practice interface
 Learning resources
 Progress dashboard
 Interview history
 Project-specific interview preparation
Planned Improvements
 Production-grade secure code execution sandbox
 Real SQL execution environment
 Dynamic GitHub repository ingestion
 Adaptive daily learning plans
 Spaced-repetition revision engine
 Advanced readiness scoring
 Job-description skill-gap analysis
 Advanced analytics
 Production deployment
 Expanded automated testing
🔮 Future Vision

The long-term goal of InterviewForge AI is to become a single platform for complete software interview preparation.

The platform aims to combine:

Learning
   +
Voice Practice
   +
AI Mock Interviews
   +
Project Defense
   +
DSA
   +
SQL
   +
Revision
   +
Progress Tracking

into one personalized interview preparation system.

🎓 Target Users

InterviewForge AI is designed primarily for:

Fresh graduates
Entry-level developers
Junior Python developers
Backend developers
AI/ML freshers
Software engineering candidates
Students preparing for technical interviews
📈 Future Development

Future versions will focus on making the platform more adaptive by using previous interview performance, weak topics, coding performance, revision history, and job descriptions to generate personalized daily preparation plans.

The planned architecture will also allow InterviewForge AI to analyze a candidate's GitHub projects and generate project-specific technical questions based on their actual implementation.

👩‍💻 Author

Prajakta Kadalagekar

Computer Engineering Graduate
Python | Flask | AI/ML | Backend Development

GitHub:
https://github.com/Prajkad96

⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

⚠️ Disclaimer

InterviewForge AI is an educational and interview-preparation project.

AI-generated feedback may not always be completely accurate and should be treated as preparation guidance rather than professional evaluation.


