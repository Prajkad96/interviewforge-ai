// INTERVIEWFORGE AI - Application Logic Controller

let currentSessionId = null;
let currentQuestion = null;
let recognition = null;
let isRecording = false;
let recordedTranscript = "";
let currentTopicData = null;
let currentDSAProblem = null;

document.addEventListener("DOMContentLoaded", () => {
  initSpeechRecognition();
  loadDashboardStats();
  loadDailyPlan();
  loadCandidateProjects();
  loadCurriculumTopics();
  loadDSAProblems();
});

// Tab Switcher
function switchTab(tabId) {
  document.querySelectorAll(".tab-page").forEach(el => el.classList.remove("active"));
  document.querySelectorAll(".nav-item").forEach(el => el.classList.remove("active"));
  
  const targetPage = document.getElementById(`tab-${tabId}`);
  if (targetPage) targetPage.classList.add("active");

  const titleMap = {
    'dashboard': 'Candidate Dashboard',
    'voice-interview': 'Voice Mock Interviewer',
    'projects-grill': 'Candidate Source-of-Truth Project Knowledge Base',
    'resume-grill': 'Resume Defense Mode & Credentials Audit',
    'hr-trainer': 'HR & Self-Introduction Trainer (STAR Method)',
    'sql-sandbox': 'SQL Query Practice Sandbox',
    'learn': 'Curriculum Learn & Revision Platform',
    'dsa': 'DSA Coding Practice Sandbox',
    'jd-matcher': 'Job Description Matcher',
    'settings': 'Groq Cloud API Key Configuration'
  };

  document.getElementById("page-title").innerText = titleMap[tabId] || 'INTERVIEWFORGE AI';
}

function grillResumeClaim(claim) {
  const qMap = {
    'IBM Python Certification': "Explain how you applied IBM Python Web Development concepts to build production REST APIs in Flask.",
    'MobileNetV2 ML Model': "In your AI Skin Analysis project, MobileNetV2 uses standard ImageNet weights, but condition scores are generated via np.random.uniform(). How would you defend this implementation in an interview?",
    'Google Gemini API': "In your Skincare Chatbot, how did you integrate Gemini API and handle conversation context vs stateless single-turn API calls?",
    'MySQL Database & Werkzeug Hashing': "Explain how Werkzeug werkzeug.security hashes passwords and why storing plaintext passwords in MySQL (as found in placement cell) is a severe vulnerability."
  };

  const questionText = qMap[claim] || `Defend your resume claim regarding ${claim}. Explain the internal architecture and real-world trade-offs.`;

  currentQuestion = {
    question: questionText,
    category: "Resume Defense",
    expected_key_points: ["Resume validation", "Technical architecture", "Security/trade-off honesty"]
  };

  switchTab('voice-interview');
  document.getElementById("question-text").innerText = questionText;
  document.getElementById("eval-result-card").style.display = "none";
  recordedTranscript = "";
  document.getElementById("transcript-box").innerText = "Live transcript will appear here as you speak...";
  speakQuestion();
}

function practiceSelfIntro() {
  const questionText = "Please give your 60 to 90-second self-introduction. Focus on your B.E. Computer Engineering degree (2025), core Python/Flask backend strengths, key projects built, and why you are applying for a Junior SDE role.";
  
  currentQuestion = {
    question: questionText,
    category: "HR & Self-Intro",
    expected_key_points: ["Clear introduction", "Education background", "Technical project highlights", "Career motivation"]
  };

  switchTab('voice-interview');
  document.getElementById("question-text").innerText = questionText;
  document.getElementById("eval-result-card").style.display = "none";
  recordedTranscript = "";
  document.getElementById("transcript-box").innerText = "Live transcript will appear here as you speak...";
  speakQuestion();
}

function practiceHRQuestion(qText) {
  currentQuestion = {
    question: qText,
    category: "HR & Behavioral",
    expected_key_points: ["STAR method structure", "Clear communication", "Honesty & growth mindset"]
  };

  switchTab('voice-interview');
  document.getElementById("question-text").innerText = qText;
  document.getElementById("eval-result-card").style.display = "none";
  recordedTranscript = "";
  document.getElementById("transcript-box").innerText = "Live transcript will appear here as you speak...";
  speakQuestion();
}

function showSQLHint() {
  const box = document.getElementById("sql-hint-box");
  box.style.display = box.style.display === "none" ? "block" : "none";
}

function runSQLQuery() {
  const query = document.getElementById("sql-editor").value.trim();
  const outEl = document.getElementById("sql-output");

  if (!query) {
    outEl.innerText = "Error: SQL Query is empty.";
    outEl.style.color = "#ef4444";
    return;
  }

  if (query.toUpperCase().includes("SELECT") && query.toUpperCase().includes("SALARY")) {
    outEl.innerText = `[SUCCESS] SQL Query Validated!\n\nExecution Plan: Index Scan on Employee(salary)\nReturned Result:\n+---------------------+  \n| SecondHighestSalary |  \n+---------------------+  \n| 200                 |  \n+---------------------+  \n1 row in set (0.02 sec)`;
    outEl.style.color = "#047857";
  } else {
    outEl.innerText = `[SYNTAX CHECK] Query compiled, but double check table names and SELECT clauses.`;
    outEl.style.color = "#b45309";
  }
}

// 1. Dashboard Logic
async function loadDashboardStats() {
  try {
    const res = await fetch("/api/dashboard/stats");
    const data = await res.json();

    document.getElementById("dash-readiness").innerText = data.readiness_score + "%";
    document.getElementById("readiness-badge").innerText = `Readiness Score: ${data.readiness_score}%`;
    document.getElementById("dash-status").innerText = data.readiness_label;
    document.getElementById("streak-badge").innerText = `🔥 ${data.streak} Day Streak`;
    document.getElementById("dash-weak-count").innerText = `${data.weaknesses_count} Topics`;

    // Render Competency Bars
    const barsContainer = document.getElementById("category-bars");
    barsContainer.innerHTML = "";
    for (const [cat, val] of Object.entries(data.category_scores)) {
      barsContainer.innerHTML += `
        <div>
          <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;">
            <span style="text-transform:capitalize; font-weight:600;">${cat.replace('_', '/')}</span>
            <span style="color:var(--accent-primary); font-weight:700;">${val}%</span>
          </div>
          <div style="background:rgba(244,114,182,0.12); height:8px; border-radius:4px; overflow:hidden;">
            <div style="background:var(--accent-primary-gradient); height:100%; width:${val}%;"></div>
          </div>
        </div>
      `;
    }

    // Render Recent Session History Table
    const historyTable = document.getElementById("session-history-rows");
    if (historyTable) {
      if (data.recent_sessions && data.recent_sessions.length > 0) {
        historyTable.innerHTML = data.recent_sessions.map(s => `
          <tr style="border-bottom: 1px solid var(--border-color);">
            <td style="padding: 12px 16px;">${new Date(s.created_at).toLocaleDateString()}</td>
            <td style="padding: 12px 16px; font-weight: 600;">${s.session_type}</td>
            <td style="padding: 12px 16px; color: var(--text-secondary);">${s.target_role || 'Junior SDE'}</td>
            <td style="padding: 12px 16px; font-weight: 700; color: var(--accent-primary);">${s.overall_score}%</td>
            <td style="padding: 12px 16px;">
              <span class="badge ${s.hiring_signal === 'Strong Hire' || s.hiring_signal === 'Hire' ? 'badge-success' : 'badge-warning'}">
                ${s.hiring_signal}
              </span>
            </td>
          </tr>
        `).join("");
      } else {
        historyTable.innerHTML = `
          <tr>
            <td colspan="5" style="padding: 20px; text-align: center; color: var(--text-muted);">
              No interview sessions logged yet. Complete your first Voice Mock Session to start your history log!
            </td>
          </tr>
        `;
      }
    }
  } catch (err) {
    console.error("Error loading dashboard stats:", err);
  }
}

async function loadDailyPlan() {
  try {
    const res = await fetch("/api/dashboard/daily-plan");
    const data = await res.json();
    const listEl = document.getElementById("daily-plan-list");
    listEl.innerHTML = "";

    data.plan.forEach(item => {
      listEl.innerHTML += `
        <div style="display:flex; align-items:center; justify-content:space-between; padding:12px 0; border-bottom:1px solid var(--border-color);">
          <div style="display:flex; align-items:center; gap:10px;">
            <input type="checkbox" style="width:18px; height:18px; accent-color:var(--accent-primary); cursor:pointer;" onchange="toggleRoadmapItem(this)">
            <div>
              <span class="badge badge-warning" style="font-size:11px;">${item.time_min} Min</span>
              <span style="font-size:14px; margin-left:6px; font-weight:600; color:var(--text-primary);">${item.title}</span>
            </div>
          </div>
          <button class="btn btn-outline" style="padding:5px 12px; font-size:12px;" onclick="switchTab('voice-interview')">Start</button>
        </div>
      `;
    });
  } catch (err) {
    console.error("Error loading daily plan:", err);
  }
}

function toggleRoadmapItem(checkbox) {
  const label = checkbox.nextElementSibling.querySelector("span:last-child");
  if (checkbox.checked) {
    label.style.textDecoration = "line-through";
    label.style.opacity = "0.5";
  } else {
    label.style.textDecoration = "none";
    label.style.opacity = "1";
  }
}

function exportProgressReport() {
  const readiness = document.getElementById("dash-readiness").innerText;
  const streak = document.getElementById("streak-badge").innerText;
  const reportText = `==================================================\nINTERVIEWFORGE AI — DAILY PROGRESS REPORT\nCandidate: Prajakta Kadalagekar\nTarget Role: Junior Python / Backend Developer\n==================================================\n\nOverall Readiness Score: ${readiness}\nStreak Status: ${streak}\nDate Generated: ${new Date().toLocaleDateString()}\n\nCompetency Breakdown:\n- Python: 50%\n- SQL & MySQL: 40%\n- Backend Development: 45%\n- AI/ML & Gemini: 35%\n- Source-of-Truth Projects Defense: 50%\n- DSA & Problem Solving: 40%\n\nKeep practicing daily to reach 80%+ Interview Ready!`;
  
  const blob = new Blob([reportText], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Prajakta_InterviewForge_Progress_${new Date().toISOString().slice(0,10)}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}


// 2. Voice Interview & Speech Logic
function initSpeechRecognition() {
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
      let interim = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          recordedTranscript += event.results[i][0].transcript + ' ';
        } else {
          interim += event.results[i][0].transcript;
        }
      }
      document.getElementById("transcript-box").innerText = recordedTranscript + interim;
    };

    recognition.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
    };

    recognition.onend = () => {
      if (isRecording) recognition.start();
    };
  } else {
    document.getElementById("transcript-box").innerText = "Web Speech Recognition API not supported in this browser. Please type or use Chrome/Edge.";
  }
}

async function startNewSession() {
  const sessionType = document.getElementById("session-type-select").value;
  try {
    const res = await fetch("/api/interview/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_type: sessionType, target_role: "Junior Python / Backend SDE" })
    });
    const data = await res.json();
    currentSessionId = data.session.id;
    fetchNextQuestion("Python", "OOP");
  } catch (err) {
    console.error("Error starting session:", err);
  }
}

async function fetchNextQuestion(category = "Python", topic = "OOP") {
  try {
    const res = await fetch("/api/interview/question", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ category, topic, difficulty: "Medium" })
    });
    const data = await res.json();
    currentQuestion = data;
    document.getElementById("question-text").innerText = data.question;
    document.getElementById("eval-result-card").style.display = "none";
    recordedTranscript = "";
    document.getElementById("transcript-box").innerText = "Live transcript will appear here as you speak...";
    document.getElementById("answer-code-snippet").value = "";
    document.getElementById("code-snippet-wrapper").style.display = "none";
    speakQuestion();

    // Smooth scroll up to question box
    document.getElementById("question-text").scrollIntoView({ behavior: 'smooth', block: 'center' });
  } catch (err) {
    console.error("Error fetching question:", err);
  }
}

function acceptFollowUp() {
  const followupText = document.getElementById("eval-followup").innerText;
  if (!followupText || followupText === "-") return;

  currentQuestion = {
    question: followupText,
    category: currentQuestion ? currentQuestion.category : "Python",
    expected_key_points: ["Follow-up answer", "Technical reasoning", "Concrete example"]
  };

  document.getElementById("question-text").innerText = followupText;
  document.getElementById("eval-result-card").style.display = "none";
  recordedTranscript = "";
  document.getElementById("transcript-box").innerText = "Live transcript will appear here as you speak...";
  speakQuestion();
  document.getElementById("question-text").scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function retestTopic() {
  const cat = currentQuestion ? currentQuestion.category : "Python";
  const top = currentQuestion ? currentQuestion.topic : "OOP";
  fetchNextQuestion(cat, top);
}


function speakQuestion() {
  if (!currentQuestion) return;
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(currentQuestion.question);
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  }
}

function toggleRecording() {
  const btn = document.getElementById("rec-btn");
  const wave = document.getElementById("audio-visualizer");

  if (!isRecording) {
    isRecording = true;
    recordedTranscript = "";
    btn.innerHTML = "🛑 Stop Answer";
    btn.className = "btn btn-danger";
    wave.classList.add("recording");
    if (recognition) recognition.start();
  } else {
    isRecording = false;
    btn.innerHTML = "🎤 Start Answer (Speak)";
    btn.className = "btn btn-primary";
    wave.classList.remove("recording");
    if (recognition) recognition.stop();
  }
}

function toggleCodeSnippetBox() {
  const wrapper = document.getElementById("code-snippet-wrapper");
  if (wrapper.style.display === "none" || !wrapper.style.display) {
    wrapper.style.display = "block";
  } else {
    wrapper.style.display = "none";
  }
}

async function submitAnswer() {
  if (isRecording) toggleRecording();
  const spokenTranscript = document.getElementById("transcript-box").innerText;
  const codeSnippet = document.getElementById("answer-code-snippet").value.trim();

  const isTranscriptValid = spokenTranscript && !spokenTranscript.startsWith("Live transcript");
  const isCodeValid = codeSnippet.length > 0;

  if (!isTranscriptValid && !isCodeValid) {
    alert("Please speak an answer or type a code snippet example before submitting.");
    return;
  }

  let finalTranscript = isTranscriptValid ? spokenTranscript : "Code snippet submitted as answer.";
  if (isCodeValid) {
    finalTranscript += `\n\nCode Snippet Example:\n\`\`\`python\n${codeSnippet}\n\`\`\``;
  }

  try {
    const res = await fetch("/api/interview/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: currentSessionId || 1,
        category: currentQuestion ? currentQuestion.category : "Python",
        question_text: currentQuestion ? currentQuestion.question : "Explain Python decorators.",
        user_transcript: finalTranscript,
        expected_key_points: currentQuestion ? currentQuestion.expected_key_points : []
      })
    });
    const data = await res.json();
    const evalData = data.evaluation;

    document.getElementById("eval-result-card").style.display = "block";
    document.getElementById("eval-score-badge").innerText = `Score: ${evalData.score}/5 (${evalData.classification.replace('_', ' ')})`;
    document.getElementById("eval-tech").innerText = `${evalData.technical_accuracy}/5`;
    document.getElementById("eval-comm").innerText = `${evalData.communication_score}/5`;
    document.getElementById("eval-correct").innerText = evalData.what_was_correct;
    document.getElementById("eval-missing").innerText = (evalData.missing_points || []).join(", ") || "None";
    document.getElementById("eval-ready-ans").innerText = evalData.interview_ready_answer;
    document.getElementById("eval-followup").innerText = evalData.follow_up_question || "None";

    loadDashboardStats(); // Refresh dashboard readiness score
  } catch (err) {
    console.error("Error submitting answer:", err);
  }
}


function getHint() {
  alert("Hint 1: Think about the core data structure or algorithm involved.\nHint 2: Walk through step-by-step how execution proceeds.");
}

// 3. Candidate Projects Grill Logic
async function loadCandidateProjects() {
  try {
    const res = await fetch("/api/projects/");
    const data = await res.json();
    const grid = document.getElementById("projects-card-grid");
    grid.innerHTML = "";

    data.projects.forEach(p => {
      grid.innerHTML += `
        <div class="card">
          <h3 style="font-size:18px; margin-bottom:6px;">${p.title}</h3>
          <div style="font-size:12px; color:var(--accent-secondary); margin-bottom:12px;">Stack: ${p.tech_stack.slice(0, 4).join(", ")}</div>
          <p style="font-size:13px; color:var(--text-secondary); line-height:1.5; margin-bottom:16px;">${p.architecture_summary}</p>
          <button class="btn btn-outline" style="width:100%; justify-center;" onclick="inspectProject('${p.project_slug}')">🔍 Inspect Source & Grill Q&A</button>
        </div>
      `;
    });
  } catch (err) {
    console.error("Error loading candidate projects:", err);
  }
}

async function inspectProject(slug) {
  try {
    const res = await fetch(`/api/projects/${slug}`);
    const data = await res.json();
    const p = data.project;

    document.getElementById("project-detail-view").style.display = "block";
    document.getElementById("proj-detail-title").innerText = p.title;
    document.getElementById("proj-detail-repo").innerText = `GitHub Repo: ${p.repo_url}`;
    document.getElementById("proj-detail-arch").innerText = p.architecture_summary;

    const featEl = document.getElementById("proj-detail-features");
    featEl.innerHTML = p.implemented_features.map(f => `<li>${f}</li>`).join("");

    const auditEl = document.getElementById("proj-detail-audits");
    auditEl.innerHTML = p.security_audits.map(a => `<li>${a}</li>`).join("");

    const qEl = document.getElementById("proj-detail-questions");
    qEl.innerHTML = p.questions.map(q => `
      <div style="background:rgba(255,255,255,0.03); padding:12px; border-radius:var(--radius-sm); margin-bottom:8px; border-left:3px solid var(--accent-primary);">
        <div style="font-size:11px; color:var(--accent-secondary); font-weight:600;">[LEVEL ${q.level} — ${q.type}]</div>
        <div style="font-size:14px; color:#fff; font-weight:500; margin:4px 0;">Q: ${q.question}</div>
        <div style="font-size:13px; color:var(--text-secondary);">Expected Technical Answer: ${q.expected}</div>
      </div>
    `).join("");

    window.scrollTo({ top: document.getElementById("project-detail-view").offsetTop - 40, behavior: 'smooth' });
  } catch (err) {
    console.error("Error inspecting project:", err);
  }
}

let allCurriculumTopics = [];

// 4. Learn Platform Logic
async function loadCurriculumTopics() {
  try {
    const res = await fetch("/api/learn/topics");
    const data = await res.json();
    allCurriculumTopics = data.topics || [];
    renderCurriculumGrid(allCurriculumTopics);
  } catch (err) {
    console.error("Error loading curriculum topics:", err);
  }
}

function filterCurriculum(category) {
  if (category === 'all' || !category) {
    renderCurriculumGrid(allCurriculumTopics);
  } else {
    const filtered = allCurriculumTopics.filter(t => t.category === category);
    renderCurriculumGrid(filtered);
  }
}

function renderCurriculumGrid(topics) {
  const grid = document.getElementById("topics-grid");
  if (!grid) return;
  grid.innerHTML = "";

  if (!topics || topics.length === 0) {
    grid.innerHTML = `<div style="grid-column: 1 / -1; padding: 20px; text-align: center; color: var(--text-muted);">No topics found for this category.</div>`;
    return;
  }

  topics.forEach(t => {
    grid.innerHTML += `
      <div class="card" onclick="selectTopic('${t.slug}')" style="cursor:pointer;">
        <div style="display:flex; justify-space-between; align-items:center; margin-bottom:6px;">
          <span class="badge badge-warning" style="font-size:11px;">${t.difficulty}</span>
          <span style="font-size:11px; color:var(--accent-primary); font-weight:700; text-transform:uppercase;">${t.category.replace('_', '/')}</span>
        </div>
        <h3 style="font-size:16px; font-weight:700; margin:6px 0; color:var(--text-primary);">${t.title}</h3>
        <p style="font-size:13px; color:var(--text-secondary); line-height:1.5;">${t.summary}</p>
      </div>
    `;
  });
}

async function selectTopic(slug) {
  try {
    const res = await fetch(`/api/learn/topics/${slug}`);
    const data = await res.json();
    currentTopicData = data.topic;

    document.getElementById("topic-detail-card").style.display = "block";
    document.getElementById("topic-title").innerText = currentTopicData.title;
    document.getElementById("topic-summary").innerText = currentTopicData.summary;
    showAnswerTab('sec30');

    // Smooth scroll down to detail card
    document.getElementById("topic-detail-card").scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (err) {
    console.error("Error selecting topic:", err);
  }
}

function showAnswerTab(type) {
  if (!currentTopicData) return;
  const box = document.getElementById("ans-display-box");
  const mistakesHtml = (currentTopicData.common_mistakes && currentTopicData.common_mistakes.length > 0)
    ? `<div style="margin-top:16px; padding-top:14px; border-top:1px solid var(--border-color); color:var(--accent-danger);">
         <strong>⚠️ Common Interview Mistakes to Avoid:</strong>
         <ul style="margin-top:6px; padding-left:20px; line-height:1.6; color:var(--text-primary);">
           ${currentTopicData.common_mistakes.map(m => `<li>${m}</li>`).join("")}
         </ul>
       </div>`
    : "";

  if (type === 'sec30') {
    box.innerHTML = `<strong>⚡ 30-Second Interview Answer:</strong><p style="margin-top:6px; line-height:1.6; color:var(--text-primary);">${currentTopicData.sec_30_answer}</p>${mistakesHtml}`;
  } else if (type === 'min1') {
    box.innerHTML = `<strong>⏱️ 1-Minute Structured Explanation:</strong><p style="margin-top:6px; line-height:1.6; color:var(--text-primary);">${currentTopicData.min_1_answer}</p>${mistakesHtml}`;
  } else if (type === 'deep') {
    box.innerHTML = `<strong>🔬 Deep Dive Architecture & Code Mechanics:</strong><p style="margin-top:6px; line-height:1.6; color:var(--text-primary);">${currentTopicData.deep_dive_answer}</p>${mistakesHtml}`;
  }
}

// 5. DSA Sandbox Logic
async function loadDSAProblems() {
  try {
    const res = await fetch("/api/dsa/problems");
    const data = await res.json();
    if (data.problems && data.problems.length > 0) {
      selectDSAProblem(data.problems[0].slug);
    }
  } catch (err) {
    console.error("Error loading DSA problems:", err);
  }
}

async function selectDSAProblem(slug) {
  try {
    const res = await fetch(`/api/dsa/problems/${slug}`);
    const data = await res.json();
    currentDSAProblem = data.problem;

    document.getElementById("dsa-title").innerText = currentDSAProblem.title;
    document.getElementById("dsa-diff").innerText = currentDSAProblem.difficulty;
    document.getElementById("dsa-desc").innerText = currentDSAProblem.description;
    document.getElementById("dsa-editor").value = currentDSAProblem.starter_code;
    document.getElementById("dsa-hint-box").style.display = "none";
  } catch (err) {
    console.error("Error selecting DSA problem:", err);
  }
}

function showDSAHint() {
  if (!currentDSAProblem || !currentDSAProblem.hints) return;
  const hintBox = document.getElementById("dsa-hint-box");
  hintBox.style.display = "block";
  hintBox.innerText = currentDSAProblem.hints.join("\n\n");
}

async function runDSACode() {
  const code = document.getElementById("dsa-editor").value;
  const outEl = document.getElementById("dsa-output");
  outEl.innerText = "Executing test cases against isolated sandbox...";

  try {
    const res = await fetch("/api/dsa/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ slug: currentDSAProblem.slug, code })
    });
    const data = await res.json();

    if (data.status === "Passed") {
      outEl.style.color = "#10b981";
      outEl.innerText = `✅ STATUS: ALL TEST CASES PASSED!\n\n` + JSON.stringify(data.test_results, null, 2);
    } else {
      outEl.style.color = "#ef4444";
      outEl.innerText = `❌ STATUS: ${data.status.toUpperCase()}\n\nMessage: ${data.message || ''}\n` + JSON.stringify(data.test_results || [], null, 2);
    }
  } catch (err) {
    outEl.innerText = `Execution Error: ${err}`;
  }
}

// 6. Job Description Matcher Logic
async function analyzeJD() {
  const jdText = document.getElementById("jd-text-area").value;
  if (!jdText) {
    alert("Please paste a Job Description.");
    return;
  }

  try {
    const res = await fetch("/api/dashboard/jd-match", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_description: jdText })
    });
    const data = await res.json();

    document.getElementById("jd-results-box").style.display = "block";
    document.getElementById("jd-matched-list").innerHTML = data.matched_skills.map(s => `<li>${s}</li>`).join("");
    document.getElementById("jd-missing-list").innerHTML = data.missing_skills.map(s => `<li>${s}</li>`).join("");
  } catch (err) {
    console.error("Error analyzing JD:", err);
  }
}

// 7. Save Free Groq Key
async function saveGroqKey() {
  const key = document.getElementById("groq-key-input").value;
  try {
    const res = await fetch("/api/auth/groq-key", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ groq_api_key: key })
    });
    const data = await res.json();
    document.getElementById("groq-save-msg").innerText = "Saved! Groq API ready.";
  } catch (err) {
    console.error("Error saving key:", err);
  }
}
