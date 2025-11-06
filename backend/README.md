AI Cyber Sentinel - Phase 1 
========================================

Quick Start
-----------

1AI Cyber Sentinel — Short README (text only)

Project purpose:
Lightweight phishing detection tool — URL scanner, Email scanner (sender spoof/lookalike), File attachment analyzer, + GenAI explanation.

Folder (important):
kali-ai/
backend/
app.py
routers/
url_router.py
email_router.py
file_router.py
analysis.py
services/
url_service.py
email_service.py
file_service.py
ai_explain.py
utils/
validators.py
text_extractor.py
frontend/
index.html

Quick start (Windows):

Open terminal at project root (kali-ai)

python -m venv venv

venv\Scripts\activate

pip install -r backend\requirements.txt

uvicorn backend.app:app --reload

Open frontend/index.html in browser

Main endpoints:
POST /api/url/scan
body: {"url":"http://example.top/verify"}

returns: {url, label, score, reason}

POST /api/email/scan
body: {"sender":"hr@rnicrosoft.com
","subject":"...","body":"..."}
returns: {label, score, reason, sender_domain}

POST /api/file/scan
form-data key=file (upload)
returns: {label, score, reason, metadata{filename,size,sha256}}

POST /api/ai/explain
body: {"text":"...", "detection":"phishing"}
returns: {"explanation": "AI generated explanation"}

Gemini (GenAI) setup (optional):

Create API key in Google AI Studio

Put key in backend/.env as GEMINI_API_KEY=YOUR_KEY

pip install google-generativeai python-dotenv

Common fixes:
• If ModuleNotFoundError for services/backend: run server from project root:
uvicorn backend.app:app --reload
• Ensure backend/init.py, backend/services/init.py, backend/routers/init.py exist (can be empty)
• For python-magic on Windows: pip install python-magic-bin
• If frontend fetch fails: ensure CORS in app.py (allow_origins=["*"])

Demo script (30s):

Show URL scan (paste phishing URL) → explain rule-based reason.

Show Email scan (sender spoof example) → show lookalike detection.

Show File scan (upload sample doc) → show metadata + heuristics.

Click Explain → show GenAI explanation (if API key configured).

Notes:
• Keep .env private (do not commit).
• For judges, use guidance cards in frontend for safety tips.
• If you want PDF report or dashboard, say "PDF" or "DASH" and I’ll add.

— End of short README —