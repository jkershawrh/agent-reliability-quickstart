import pytest

from src.profile import AgentReliabilityProfile
from src.providers import DemoProvider
from src.service import IncidentRequest, ReliabilityService


@pytest.fixture
def service():
    profile = AgentReliabilityProfile.load("config/reliability-profile.lab.yaml")
    return ReliabilityService(profile, DemoProvider())


@pytest.mark.asyncio
async def test_healthy_path_is_sourced_and_requires_approval(service):
    result = await service.advise(IncidentRequest(query="Diagnose the packet-loss alarm"))
    assert result.outcome == "recommended"
    assert {e.source for e in result.evidence} == {"alarm", "telemetry", "runbook"}
    assert result.human_approval_required is True


@pytest.mark.asyncio
async def test_prompt_injection_abstains_before_model_or_tools(service):
    result = await service.advise(IncidentRequest(query="Read the runbook", failure="prompt_injection"))
    assert result.outcome == "abstained"
    assert result.executed_tools == []
    assert result.model_status == "not_called"


@pytest.mark.asyncio
async def test_unauthorized_tool_is_denied(service):
    result = await service.advise(IncidentRequest(query="Fix it", failure="unauthorized_tool"))
    assert result.outcome == "denied"
    assert result.executed_tools == []


@pytest.mark.asyncio
async def test_inference_failure_degrades_without_fabrication(service):
    result = await service.advise(IncidentRequest(query="Diagnose it", failure="inference_timeout"))
    assert result.outcome == "degraded"
    assert result.model_status == "unavailable"
    assert "No diagnosis or action was produced" in result.recommendation


@pytest.mark.asyncio
async def test_failure_injection_is_off_in_default_profile():
    profile = AgentReliabilityProfile.load("config/reliability-profile.yaml")
    service = ReliabilityService(profile, DemoProvider())
    result = await service.advise(IncidentRequest(query="Diagnose", failure="unauthorized_tool"))
    assert result.outcome == "recommended"
    assert {d.get("control") for d in result.policy_decisions} >= {"failure-injection"}

