from __future__ import annotations

from typing import Any, Optional, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="NOC Evidence MCP Server", version="0.1.0")

TOOLS = [
    {"name": name, "description": description, "inputSchema": {"type": "object", "properties": {"alarm_id": {"type": "string"}}, "required": ["alarm_id"]}}
    for name, description in (
        ("get_alarm", "Read a simulated NOC alarm."),
        ("get_telemetry", "Read telemetry associated with an alarm."),
        ("get_runbook", "Read the approved response runbook."),
    )
]

DATA = {
    "get_alarm": {"source": "alarm", "reference": "NOC-1042", "summary": "Packet loss exceeded 8% on cell group west-7."},
    "get_telemetry": {"source": "telemetry", "reference": "TEL-west-7", "summary": "Interface errors rose after a traffic spike."},
    "get_runbook": {"source": "runbook", "reference": "RB-17", "summary": "Validate errors; request approval before traffic shift."},
}


class Request(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None  # noqa: UP007, UP045 - local validation supports Python 3.9
    method: str
    params: dict[str, Any] = {}


@app.get("/health")
async def health():
    return {"status": "healthy", "tools": list(DATA)}


@app.post("/mcp")
async def mcp(request: Request):
    if request.method == "tools/list":
        return {"jsonrpc": "2.0", "id": request.id, "result": {"tools": TOOLS}}
    if request.method == "tools/call":
        name = request.params.get("name", "")
        if name not in DATA:
            return {"jsonrpc": "2.0", "id": request.id, "error": {"code": -32601, "message": "tool_not_found"}}
        return {"jsonrpc": "2.0", "id": request.id, "result": DATA[name]}
    return {"jsonrpc": "2.0", "id": request.id, "error": {"code": -32601, "message": "method_not_found"}}
