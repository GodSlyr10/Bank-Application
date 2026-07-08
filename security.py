import re

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all|previous|above)?\s*instructions",
    r"forget\s+(all|everything|previous)",
    r"system\s+prompt",
    r"developer\s+message",
    r"developer\s+instructions",
    r"reveal\s+your\s+instructions",
    r"show\s+your\s+prompt",
    r"print\s+your\s+prompt",
    r"bypass\s+safety",
    r"disable\s+safety",
    r"jailbreak",
    r"act\s+as",
    r"you\s+are\s+now",
]

def detect_prompt_injection(text: str) -> bool:
    """
    Detects common prompt injection attempts from the user.
    """
    text = text.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text):
            return True

    return False