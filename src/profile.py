from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, model_validator


class RetryPolicy(BaseModel):
    timeout_seconds: float = Field(ge=0.1, le=120)
    max_attempts: int = Field(ge=1, le=5)
    backoff_seconds: float = Field(ge=0, le=10)


class AgentReliabilityProfile(BaseModel):
    api_version: Literal["reliability.agentic.redhat.com/v1alpha1"]
    kind: Literal["AgentReliabilityProfile"]
    name: str
    retry: RetryPolicy
    allowed_tools: list[str]
    guardrail_mode: Literal["enforce", "observe", "disabled"] = "enforce"
    required_evidence: list[str] = ["alarm", "telemetry", "runbook"]
    degraded_message: str
    lab_failure_injection: bool = False

    @model_validator(mode="after")
    def secure_defaults(self):
        if not self.allowed_tools:
            raise ValueError("allowed_tools must be an explicit non-empty allowlist")
        return self

    @classmethod
    def load(cls, path: str | Path) -> AgentReliabilityProfile:
        return cls.model_validate(yaml.safe_load(Path(path).read_text()))

