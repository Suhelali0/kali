from utils.validators import extract_domain, is_domain, has_ip, suspicious_tld

def analyze_url(url: str):
    url = url.strip()
    domain = extract_domain(url)

    if not is_domain(url):
        return {"url": url, "label": "invalid", "score": 0.0, "reason": "Not a valid domain format."}

    # simple heuristic scoring
    score = 0.0
    s = url.lower()

    # suspicious keywords in path or domain
    keywords = ["login", "secure", "verify", "confirm", "signin", "account", "bank", "password", "update"]
    for kw in keywords:
        if kw in s:
            score += 0.25

    # IP address in domain
    if has_ip(url):
        score += 0.35

    # suspicious TLD on domain
    if suspicious_tld(url):
        score += 0.3

    # domain length odd
    if domain and len(domain) > 20:
        score += 0.1

    # clamp
    if score > 1.0:
        score = 1.0

    label = "phishing" if score >= 0.5 else "safe"
    reason_parts = []
    if any(kw in s for kw in keywords):
        reason_parts.append("Contains suspicious keywords like 'login'/'secure'/'verify'.")
    if has_ip(url):
        reason_parts.append("Uses IP address for domain.")
    if suspicious_tld(url):
        reason_parts.append("Uses uncommon/suspicious top-level domain.")
    if domain and len(domain) > 20:
        reason_parts.append("Long/odd-looking domain.")

    reason = " ".join(reason_parts) if reason_parts else "No phishing pattern detected."
    return {"url": url, "label": label, "score": round(score, 2), "reason": reason}
