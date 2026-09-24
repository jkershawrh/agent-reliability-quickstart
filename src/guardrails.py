from __future__ import annotations

import re
from dataclasses import dataclass

INJECTION_PATTERNS = (
    re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions", re.IGNORECASE),
    re.compile(r"reveal\s+(the\s+)?system\s+prompt", re.IGNORECASE),
    re.compile(r"disregard\s+(the\s+)?runbook", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+", re.IGNORECASE),
)


@dataclass(frozen=True)
class GuardrailDecision:
    allowed: bool
    reason: str
    provider: str = "local-policy"


def screen(text: str, mode: str = "enforce") -> GuardrailDecision:
    detected = any(pattern.search(text) for pattern in INJECTION_PATTERNS)
    if detected and mode == "enforce":
        return GuardrailDecision(False, "prompt_injection_detected")
    if detected:
        return GuardrailDecision(True, "prompt_injection_observed")
    return GuardrailDecision(True, "clean")

