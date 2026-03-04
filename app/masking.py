# Mask before embeddings/LLM. Keep raw CJIS separate. Tokenize consistently so joins still work.”

import re
import hashlib

PII_PATTERNS = [
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN]"),
    (re.compile(r"\b\d{10}\b"), "[PHONE]"),
]

def stable_token(value: str, salt: str = "demo-salt") -> str:
    h = hashlib.sha256((salt + value).encode("utf-8")).hexdigest()
    return f"TOK_{h[:10]}"

def mask_text(text: str) -> str:
    out = text
    for pat, repl in PII_PATTERNS:
        out = pat.sub(repl, out)
    return out

def mask_row(row: dict) -> dict:
    """
    Example: remove/mask DOB or other PII before sending to LLM.
    """
    row = dict(row)
    if "dob" in row and row["dob"]:
        row["dob"] = "[DOB_REDACTED]"
    return row