# services/email_service.py
import re
from difflib import SequenceMatcher

# Simple trusted brand list (extend as needed)
TRUSTED_BRANDS = {
    "microsoft": ["microsoft.com", "office.com"],
    "google": ["google.com", "gmail.com"],
    "paypal": ["paypal.com"],
    "amazon": ["amazon.com"],
    "bankofamerica": ["bankofamerica.com"],
    # add more brands here if you want
}

# common deceptive patterns mapping (multiple characters that look like single)
VISUAL_SUBS = [
    ("rn", "m"),
    ("vv", "w"),
    ("0", "o"),
    ("1", "l"),
    ("l", "i"),  # optional, may increase false positives
    ("s", "5"),
]

def normalize_domain(domain: str) -> str:
    domain = domain.strip().lower()
    if domain.startswith("www."):
        domain = domain[4:]
    domain = domain.split(":")[0]
    return domain

def domain_from_email(email: str) -> str:
    try:
        parts = email.split("@")
        if len(parts) != 2:
            return ""
        return normalize_domain(parts[1])
    except Exception:
        return ""

def sequence_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def apply_visual_subs(s: str) -> str:
    s = s.lower()
    out = s
    for pat, rep in VISUAL_SUBS:
        out = out.replace(pat, rep)
    return out

def is_lookalike_domain(domain: str, trusted_domain: str):
    """
    Return (is_lookalike:bool, score:float, reason:str)
    """
    d = normalize_domain(domain)
    t = normalize_domain(trusted_domain)

    # compare SLDs (second-level domain)
    def sld(x):
        return x.split(".")[0] if x else x

    sd = sld(d)
    st = sld(t)

    if not sd or not st:
        return (False, 0.0, "Missing parts for comparison")

    # direct equality -> likely exact match
    if sd == st:
        return (False, 1.0, f"Exact match with trusted domain {t}")

    base_sim = sequence_similarity(sd, st)
    sd_sub = apply_visual_subs(sd)
    sub_sim = sequence_similarity(sd_sub, st)

    # if substitution makes them equal -> very suspicious
    if sd_sub == st:
        reason = f"Visual-substitution match: '{sd}' -> '{sd_sub}' equals '{st}'"
        return (True, 0.99, reason)

    score = max(base_sim, sub_sim)

    # threshold heuristics (tuneable)
    threshold = 0.85 if len(st) <= 4 else 0.80
    is_lookalike = score >= threshold
    reason = f"Similarity between '{sd}' and '{st}' = {score:.2f}"
    return (is_lookalike, score, reason)

def analyze_email(sender: str, subject: str, body: str):
    """
    Analyze email content + sender domain for phishing signals.
    Returns: { label, score, reason, sender_domain }
    """
    text = (subject or "") + " " + (body or "")
    text = text.lower()

    score = 0.0
    reasons = []

    # content heuristics
    urgent_words = ["urgent", "immediately", "warning", "suspended", "expire"]
    phishing_words = ["verify", "reset", "confirm", "account", "password", "login", "click here"]
    threaten_words = ["locked", "close", "compromised"]

    if any(w in text for w in urgent_words):
        score += 0.30
        reasons.append("Urgency detected.")

    if any(w in text for w in phishing_words):
        score += 0.30
        reasons.append("Sensitive verification request detected.")

    if any(w in text for w in threaten_words):
        score += 0.20
        reasons.append("Threat/fear language detected.")

    # sender-based heuristics
    sender_domain = domain_from_email(sender)
    if sender_domain:
        is_look = False
        for brand, domains in TRUSTED_BRANDS.items():
            for td in domains:
                look, sim_score, reason_text = is_lookalike_domain(sender_domain, td)
                if look:
                    score += 0.35
                    reasons.append(f"Sender domain looks like trusted '{td}': {reason_text}")
                    is_look = True
                    break
            if is_look:
                break

        # IP address used as domain?
        if re.match(r"^\d+\.\d+\.\d+\.\d+$", sender_domain):
            score += 0.30
            reasons.append("Sender uses IP address as domain.")

        # suspicious TLD quick-check
        if sender_domain.endswith((".top", ".xyz", ".click", ".review", ".bid")):
            score += 0.25
            reasons.append("Sender uses suspicious top-level domain.")
    else:
        reasons.append("Sender malformed or missing.")

    # clamp
    if score > 1.0:
        score = 1.0

    label = "phishing" if score >= 0.5 else "safe"
    reason = " ".join(reasons) if reasons else "No phishing patterns detected."

    return {"label": label, "score": round(score, 2), "reason": reason, "sender_domain": sender_domain}
