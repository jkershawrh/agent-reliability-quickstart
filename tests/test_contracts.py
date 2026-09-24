import re
from pathlib import Path

import pytest

from src.mcp import Request, mcp


@pytest.mark.asyncio
async def test_mcp_lists_only_read_only_tools():
    response = await mcp(Request(id="1", method="tools/list"))
    names = {tool["name"] for tool in response["result"]["tools"]}
    assert names == {"get_alarm", "get_telemetry", "get_runbook"}


def test_no_literal_secret_in_tracked_content():
    suspicious = re.compile(r"(?:sk-|sha256~)[A-Za-z0-9_-]{12,}")
    files = [*Path("src").rglob("*"), *Path("deploy").rglob("*"), *Path("modules").rglob("*")]
    leaks = [str(path) for path in files if path.is_file() and suspicious.search(path.read_text(errors="ignore"))]
    assert leaks == []


def test_failure_injection_is_disabled_in_base():
    assert "lab_failure_injection: false" in Path("deploy/base/configmap.yaml").read_text()

