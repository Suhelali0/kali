import magic
import hashlib

def analyze_file(filename, content):
    # Detect MIME type
    file_type = magic.from_buffer(content, mime=True)

    # Generate hash for malware identification
    file_hash = hashlib.sha256(content).hexdigest()

    suspicious = False
    reason = "File appears safe."

    # Basic rule: Executables = Risky
    if file_type in ["application/x-dosexec", "application/x-executable", "application/vnd.microsoft.portable-executable"]:
        suspicious = True
        reason = "Executable file detected. Potential malware risk."

    return {
        "filename": filename,
        "file_type": file_type,
        "file_hash": file_hash,
        "label": "suspicious" if suspicious else "safe",
        "reason": reason
    }
