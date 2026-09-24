from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import httpx

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


class NemoGuardrailClient:
    """Call the supported RHOAI NeMo checks API without generating a response."""

    def __init__(
        self,
        endpoint: str,
        *,
        token_file: str = "/var/run/secrets/guardrails/token",
        ca_file: str = "/etc/guardrails-ca/service-ca.crt",
        timeout: float = 10,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        self.endpoint = endpoint.rstrip("/")
        self.token_file = Path(token_file)
        self.ca_file = ca_file
        self.timeout = timeout
        self.transport = transport

    async def screen(self, text: str, mode: str = "enforce") -> GuardrailDecision:
        if mode == "disabled":
            return GuardrailDecision(True, "disabled", "rhoai-nemo")
        token = self.token_file.read_text().strip()
        async with httpx.AsyncClient(
            verify=self.ca_file,
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            response = await client.post(
                f"{self.endpoint}/v1/guardrail/checks",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "model": "input-policy",
                    "messages": [{"role": "user", "content": text}],
                },
            )
            response.raise_for_status()
            payload = response.json()
        blocked = payload.get("status") == "blocked"
        if blocked and mode == "enforce":
            return GuardrailDecision(False, "prompt_injection_detected", "rhoai-nemo")
        if blocked:
            return GuardrailDecision(True, "prompt_injection_observed", "rhoai-nemo")
        return GuardrailDecision(True, "clean", "rhoai-nemo")
