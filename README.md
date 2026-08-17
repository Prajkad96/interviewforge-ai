# ⚡ INTERVIEWFORGE AI — Personal Software Engineering Interview Coach

> **Learn. Speak. Code. Defend. Get Grilled. Improve. Get Hired.**

INTERVIEWFORGE AI is an intelligent, full-stack voice-first interview preparation platform tailored for **Prajakta Kadalagekar** (Junior Python / Backend Software Development Engineer).

---

## 🌟 Key Features

### 🎙️ 1. Voice-First AI Mock Interviewer
- **Web Speech API Integration**: Practice technical answers using live Speech-to-Text (STT) and Text-to-Speech (TTS) replay.
- **Strict 0–5 Evaluation Engine**: Evaluates technical accuracy, communication clarity, missing points, and provides interview-ready sample answers powered by Groq Cloud API (`llama-3.3-70b-versatile`).
- **Anti-Repetition Rotation Engine**: Queries question history and rotates across 5 distinct technical perspectives (Internal mechanics, Real-world usage, Trade-offs & edge cases, Debugging anti-patterns, Why chosen over alternatives).
- **💻 Code Snippet Example Area**: Attach Python/SQL code snippets alongside spoken answers for combined speech & code evaluation.

### 💻 2. Candidate Source-of-Truth Project Knowledge Base
- Complete audited technical knowledge base for candidate's 6 GitHub repositories:
  1. **AI Skin Analysis** (`Skin-Analysis-AI`)
  2. **Skincare Chatbot** (`skincare-chatbot`)
  3. **JobTracker** (`job-tracker`)
  4. **HealthPredict AI** (`Health-Prediction-Application`)
  5. **College Placement Portal** (`College-Placement-Portal`)
  6. **Sweet Shop Management System** (`sweet-shop-management-system`)
- Explores architecture summaries, implemented features, security vulnerability audits, and level 1–3 defense questions.

### 📄 3. Resume Defense Mode
- Drills candidate on exact resume claims, education (B.E. Computer Engineering 2025 CGPA 7.2), certifications (IBM Python for Web Development, Kodacy AI/ML), and tech stack.

### 🗣️ 4. HR & Self-Introduction Trainer (STAR Method)
- 60–90 second self-introduction timer with STAR method guidance and fresher HR question practice.

### 🗄️ 5. SQL Query Sandbox
- Practice essential SQL queries (`2nd Highest Salary`, `INNER JOIN vs LEFT JOIN`, `GROUP BY ... HAVING`) with a live execution console.

### 🧩 6. DSA Coding Sandbox
- Fresher DSA problem bank with isolated Python code execution runner and test cases.

### 📚 7. 100% Resume Skills E-Learning Platform
- 16 structured curriculum topics covering Python, Flask, FastAPI, SQL, MySQL, MobileNetV2, OpenCV, Gemini API, C/C++, Java, and Git.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11, Flask, Flask-SQLAlchemy, Flask-CORS, Werkzeug, SQLite
- **AI Service**: Groq Cloud API (`llama-3.3-70b-versatile`)
- **Frontend**: HTML5, Vanilla CSS3 (Chic Aesthetic Light Theme), Web Speech API, Vanilla JavaScript (ES6)

---

## 🚀 Quick Setup & Installation

### Option 1: Using Included Batch Script (Recommended for Windows)

Simply double-click `run.bat` or execute in terminal:

```cmd
.\run.bat
```

### Option 2: Manual Installation

```bash
# 1. Clone the repository
git clone https://github.com/Prajkad96/interviewforge.git
cd interviewforge

# 2. Set up virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # On Windows PowerShell
# source venv/bin/activate    # On Linux/macOS

# 3. Install requirements
pip install -r requirements.txt

# 4. Run application
cd backend
python app.py
```

Navigate to **`http://127.0.0.1:5000`** in your web browser.

---

## ⚙️ Free Groq API Key Setup

1. Get a **100% Free API Key** from [https://console.groq.com/keys](https://console.groq.com/keys).
2. Enter the key in the **Settings** tab of the application, or set `GROQ_API_KEY=gsk_...` in `.env`.

---

## 👩‍💻 Candidate Profile

- **Candidate**: Prajakta Kadalagekar
- **Degree**: B.E. Computer Engineering (2025 Graduate)
- **Target Roles**: Junior Python Developer, Junior Backend Engineer, SDE-1
