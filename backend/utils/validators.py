import re
from urllib.parse import urlparse

IP_PATTERN = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}")

SUSPICIOUS_TLDS = [".xyz", ".top", ".click", ".shop", ".fit", ".kim", ".review", ".bid"]

def extract_domain(url: str) -> str:
    """Return netloc/domain (no port)."""
    try:
        if not url.startswith("http"):
            url = "http://" + url
        parsed = urlparse(url)
        domain = parsed.netloc.split(":")[0]  # remove port if any
        return domain.lower()
    except Exception:
        return ""

def is_domain(url: str) -> bool:
    domain = extract_domain(url)
    return domain != ""

def has_ip(url: str) -> bool:
    domain = extract_domain(url)
    return bool(IP_PATTERN.fullmatch(domain)) or bool(IP_PATTERN.search(url))

def suspicious_tld(url: str) -> bool:
    """
    Check TLD against the domain (not the full path).
    This handles URLs like example.top/verify correctly.
    """
    domain = extract_domain(url)
    for t in SUSPICIOUS_TLDS:
        if domain.endswith(t):
            return True
    return False
