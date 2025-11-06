import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def explain_threat(label, reason, content):
    prompt = f"""
    You are a Cyber Security Threat Analyzer.

    Detection Result:
    - Label: {label}
    - Reason: {reason}

    Suspicious Content:
    {content}

    Explain to a non-technical person why this is dangerous and how to avoid it.
    Keep it short, clear, and helpful.
    """

    response = model.generate_content(prompt)
    return response.text
