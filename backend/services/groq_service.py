import os
import json
import urllib.request
import urllib.error
import time

class GroqService:
    def __init__(self, api_key=None, model=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        # Groq provides 100% free API keys at https://console.groq.com
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"

    def set_api_key(self, key):
        self.api_key = key.strip() if key else ""

    def get_info(self):
        return {
            "has_key": bool(self.api_key),
            "free_key_url": "https://console.groq.com/keys",
            "message": "Groq Cloud API is 100% free for developer use. Get your free key at https://console.groq.com/keys"
        }


    def _call_groq_api(self, messages, temperature=0.7, max_tokens=1000, json_mode=True):
        """Sends a request to Groq Cloud API using standard urllib for portability."""
        if not self.api_key or self.api_key.strip() == "" or self.api_key == "YOUR_GROQ_API_KEY":
            print("Groq API key not provided. Utilizing deterministic fallback mode.")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.endpoint, data=data, headers=headers, method="POST")

        # Attempt API call with backoff retries
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                with urllib.request.urlopen(req, timeout=20) as response:
                    res_body = response.read().decode("utf-8")
                    parsed = json.loads(res_body)
                    content = parsed["choices"][0]["message"]["content"]
                    return content
            except urllib.error.HTTPError as e:
                err_msg = e.read().decode("utf-8") if e.fp else str(e)
                print(f"Groq API HTTP Error {e.code} (Attempt {attempt+1}/{max_attempts}): {err_msg}")
                if e.code in [429, 503, 504] and attempt < max_attempts - 1:
                    time.sleep(1.5 * (attempt + 1))
                else:
                    break
            except Exception as e:
                print(f"Groq API call exception (Attempt {attempt+1}/{max_attempts}): {e}")
                if attempt < max_attempts - 1:
                    time.sleep(1.5 * (attempt + 1))
                else:
                    break

        return None

    def generate_interview_question(self, category, topic, difficulty="Medium", project_context=None, previously_asked=None):
        """Generates a strict, non-repetitive technical interview question testing different angles."""
        angles = [
            "internal implementation & runtime mechanics",
            "practical real-world project usage scenario",
            "trade-offs, limitations, and edge cases",
            "debugging a specific failure or anti-pattern",
            "why this approach was chosen over alternatives"
        ]
        import random
        selected_angle = random.choice(angles)

        system_prompt = (
            "You are a Senior Technical Engineering Interviewer conducting a strict junior software engineer interview. "
            "Formulate unique, non-repetitive technical questions. "
            "IMPORTANT: Do NOT repeat simple definitions. Test deep understanding from different angles. "
            "Return valid JSON with keys: 'question', 'category', 'topic', 'expected_key_points', 'angle'."
        )
        
        user_prompt = f"Category: {category}\nTopic: {topic}\nDifficulty: {difficulty}\nQuestion Angle: Focus on {selected_angle}."
        if project_context:
            user_prompt += f"\nProject Context: {project_context}"
        if previously_asked and len(previously_asked) > 0:
            user_prompt += f"\nDo NOT repeat or closely mirror any of these previously asked questions:\n" + json.dumps(previously_asked[:10])

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        raw_res = self._call_groq_api(messages)
        if raw_res:
            try:
                return json.loads(raw_res)
            except Exception:
                pass

        # Deterministic Fallback Question with Angle Variation
        fallback_questions = [
            f"Explain the internal runtime mechanics of {topic} in {category}. How does Python or the underlying database handle this under the hood?",
            f"In what scenario would using {topic} be inefficient or problematic in a production {category} application?",
            f"If you were reviewing code using {topic}, what edge cases or security anti-patterns would you watch out for?",
            f"How does {topic} differ from its main alternative in {category}, and why would you choose one over the other?"
        ]
        chosen_q = random.choice(fallback_questions)
        return {
            "question": chosen_q,
            "category": category,
            "topic": topic,
            "expected_key_points": ["Core technical mechanism", "Trade-offs and edge cases", "Practical implementation example"],
            "angle": selected_angle
        }


    def evaluate_answer(self, question, user_answer, expected_points=None):
        """Evaluates candidate response on a 0-5 scale with detailed feedback."""
        system_prompt = """You are a strict, objective Technical Interviewer. Evaluate the candidate's answer.
Do not artificially inflate scores.
Score Scale:
0 = Completely wrong / blank
1 = Very weak
2 = Partially correct but shallow
3 = Acceptable
4 = Strong
5 = Interview-ready / Exceptional

Return valid JSON with keys:
- 'score': (integer 0-5)
- 'technical_accuracy': (integer 0-5)
- 'communication_score': (integer 0-5)
- 'classification': ('completely_wrong', 'weak', 'partially_correct', 'acceptable', 'strong', 'interview_ready')
- 'what_was_correct': (string summary)
- 'missing_points': (list of strings)
- 'mistakes': (list of strings)
- 'interview_ready_answer': (clear 2-3 sentence exemplary answer)
- 'follow_up_question': (challenging follow-up question)
"""
        user_prompt = f"Question: {question}\nCandidate Answer: {user_answer}"
        if expected_points:
            user_prompt += f"\nExpected Key Points: {json.dumps(expected_points)}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        raw_res = self._call_groq_api(messages)
        if raw_res:
            try:
                return json.loads(raw_res)
            except Exception:
                pass

        # Deterministic Fallback Evaluation
        ans_len = len(user_answer.strip().split())
        score = 4 if ans_len > 30 else (3 if ans_len > 15 else (2 if ans_len > 5 else 1))
        return {
            "score": score,
            "technical_accuracy": score,
            "communication_score": score,
            "classification": "partially_correct" if score <= 3 else "strong",
            "what_was_correct": "You addressed the fundamental question.",
            "missing_points": ["Deep internal mechanics explanation", "Concrete code snippet or example"],
            "mistakes": [],
            "interview_ready_answer": f"For {question}, an ideal candidate explains the underlying data structures, runtime complexity, and practical implementation context.",
            "follow_up_question": "Can you walk through a concrete example or trade-off of this approach?"
        }

    def analyze_job_description(self, job_description, candidate_profile):
        """Extracts key skills and matches against candidate profile."""
        system_prompt = """Analyze the provided Job Description against the candidate's profile.
Return valid JSON with:
- 'matched_skills': (list of strings)
- 'missing_skills': (list of strings)
- 'match_percentage': (integer 0-100)
- 'recommended_focus_areas': (list of strings)
- 'tailored_interview_questions': (list of strings)
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Job Description:\n{job_description}\n\nCandidate Profile:\n{json.dumps(candidate_profile)}"}
        ]

        raw_res = self._call_groq_api(messages)
        if raw_res:
            try:
                return json.loads(raw_res)
            except Exception:
                pass

        return {
            "matched_skills": ["Python", "Flask", "MySQL", "REST APIs"],
            "missing_skills": ["Docker", "Redis", "Celery"],
            "match_percentage": 75,
            "recommended_focus_areas": ["FastAPI dependency injection", "SQL query indexing", "System design basics"],
            "tailored_interview_questions": [
                "How would you scale a Flask REST API handling 1,000 requests per minute?",
                "How do you optimize MySQL queries using indexes?"
            ]
        }

groq_service = GroqService()
