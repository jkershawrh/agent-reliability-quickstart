from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod

import httpx


class InferenceUnavailable(RuntimeError):
    pass


class InferenceProvider(ABC):
    @abstractmethod
    async def complete(self, messages: list[dict]) -> str: ...


class OpenAICompatibleProvider(InferenceProvider):
    """Portable adapter for RHOAI/vLLM/LiteLLM OpenAI-compatible endpoints."""

    def __init__(self, endpoint: str, model: str, api_key: str, timeout: float):
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.timeout = timeout

    async def complete(self, messages: list[dict]) -> str:
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
                return response.json()["choices"][0]["message"]["content"]
        except (httpx.HTTPError, KeyError, IndexError, asyncio.TimeoutError) as exc:
            raise InferenceUnavailable("inference endpoint unavailable") from exc


class DemoProvider(InferenceProvider):
    async def complete(self, messages: list[dict]) -> str:
        return "Probable transport congestion. Validate interface errors, then apply the approved traffic-shift runbook."

