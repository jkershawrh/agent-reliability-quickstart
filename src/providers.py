from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass

import httpx


class InferenceUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class InferenceCompletion:
    content: str
    observed_model: str


class InferenceProvider(ABC):
    kind = "unknown"
    model_participates = False
    configured_model = ""

    @abstractmethod
    async def complete(self, messages: list[dict]) -> InferenceCompletion: ...


class OpenAICompatibleProvider(InferenceProvider):
    """Portable adapter for RHOAI/vLLM/LiteLLM OpenAI-compatible endpoints."""

    kind = "openai-compatible"
    model_participates = True

    def __init__(self, endpoint: str, model: str, api_key: str, timeout: float):
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.configured_model = model
        self.api_key = api_key
        self.timeout = timeout

    async def complete(self, messages: list[dict]) -> InferenceCompletion:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.endpoint}/chat/completions",
                    headers=headers,
                    json={"model": self.model, "messages": messages, "temperature": 0},
                )
                response.raise_for_status()
                payload = response.json()
                return InferenceCompletion(
                    content=payload["choices"][0]["message"]["content"],
                    observed_model=str(payload.get("model", "")),
                )
        except (httpx.HTTPError, KeyError, IndexError, TypeError, asyncio.TimeoutError) as exc:
            raise InferenceUnavailable("inference endpoint unavailable") from exc


class DemoProvider(InferenceProvider):
    kind = "deterministic-demo"
    model_participates = False

    async def complete(self, messages: list[dict]) -> InferenceCompletion:
        return InferenceCompletion(
            content="Probable transport congestion. Validate interface errors, then apply the approved traffic-shift runbook.",
            observed_model="",
        )
