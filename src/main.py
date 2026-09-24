import os

from fastapi import FastAPI

from .guardrails import NemoGuardrailClient
from .profile import AgentReliabilityProfile
from .service import IncidentRequest, ReliabilityService, provider_from_env

PROFILE_PATH = os.getenv("RELIABILITY_PROFILE", "config/reliability-profile.yaml")
profile = AgentReliabilityProfile.load(PROFILE_PATH)
guardrail_endpoint = os.getenv("GUARDRAILS_ENDPOINT", "")
guardrail_client = NemoGuardrailClient(guardrail_endpoint) if guardrail_endpoint else None
service = ReliabilityService(profile, provider_from_env(profile), os.getenv("MCP_URL", ""), guardrail_client)

app = FastAPI(title="When Agents Fail", version="0.1.0")


@app.get("/health")
async def health():
    return {"status": "healthy", "profile": profile.name, "failure_injection": profile.lab_failure_injection}


@app.post("/api/v1/advise")
async def advise(request: IncidentRequest):
    return await service.advise(request)
