import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .guardrails import NemoGuardrailClient
from .profile import AgentReliabilityProfile
from .service import IncidentRequest, ReliabilityService, provider_from_env

PROFILE_PATH = os.getenv("RELIABILITY_PROFILE", "config/reliability-profile.yaml")
profile = AgentReliabilityProfile.load(PROFILE_PATH)
guardrail_endpoint = os.getenv("GUARDRAILS_ENDPOINT", "")
guardrail_client = NemoGuardrailClient(guardrail_endpoint) if guardrail_endpoint else None
service = ReliabilityService(profile, provider_from_env(profile), os.getenv("MCP_URL", ""), guardrail_client)

app = FastAPI(title="When Agents Fail", version="0.1.1")


@app.get("/", response_class=HTMLResponse)
async def workspace():
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agent Reliability Advisor</title><style>
:root{color-scheme:dark;font-family:"Red Hat Text",system-ui,sans-serif;background:#151515;color:#fff}body{margin:0;background:#151515}main{max-width:920px;margin:auto;padding:40px 24px}.eyebrow{color:#73bcf7;font-weight:700;letter-spacing:.08em;text-transform:uppercase}h1{font-size:2.2rem;margin:.3rem 0}.lead{color:#c7c7c7;max-width:760px}.panel{margin-top:28px;padding:24px;background:#212121;border:1px solid #3c3f42;border-radius:12px}.journey{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:24px 0}.journey div{padding:12px;background:#292929;border-bottom:3px solid #73bcf7;font-size:.9rem}.summary{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:18px}.fact{background:#151515;padding:12px;border:1px solid #3c3f42;border-radius:6px}.fact span{display:block;color:#8a8d90;font-size:.8rem}.fact strong{display:block;margin-top:4px;overflow-wrap:anywhere}.hidden{display:none}label{display:block;font-weight:700;margin:16px 0 8px}textarea,select{width:100%;box-sizing:border-box;background:#151515;color:#fff;border:1px solid #6a6e73;border-radius:6px;padding:12px}textarea{min-height:110px;resize:vertical}button{margin-top:18px;background:#ee0000;color:#fff;border:0;border-radius:6px;padding:12px 20px;font-weight:700;cursor:pointer}button:disabled{opacity:.55}pre{white-space:pre-wrap;overflow:auto;background:#0f0f0f;border-radius:6px;padding:16px;min-height:80px}.status{color:#8a8d90;font-size:.9rem}@media(max-width:700px){.journey,.summary{grid-template-columns:1fr 1fr}}
</style></head><body><main><div class="eyebrow">Intel × Red Hat AI Launchpad · 301 Engineer</div><h1>Agent Reliability Advisor</h1><p class="lead">Follow one NOC incident from healthy recommendation through three controlled failures and qualification. Recommendations remain read-only and require human approval.</p><div class="journey"><div><strong>1 · Healthy</strong><br>Ground in evidence</div><div><strong>2 · Abstain</strong><br>Contain unsafe input</div><div><strong>3 · Deny</strong><br>Enforce authority</div><div><strong>4 · Degrade</strong><br>Fail without fabrication</div></div><section class="panel"><label for="query">NOC request</label><textarea id="query">Diagnose NOC-1042 and recommend the safest next step</textarea><label for="scenario">Reliability scenario</label><select id="scenario"><option value="none">Healthy evidence-backed request</option><option value="prompt_injection">Prompt injection</option><option value="unauthorized_tool">Unauthorized tool request</option><option value="inference_timeout">Inference disruption</option></select><button id="run">Run reliability check</button><p id="status" class="status">Start with the healthy request, then compare each failure against it.</p><div id="summary" class="summary hidden" aria-live="polite"></div><details><summary>Structured decision evidence</summary><pre id="result">Results will appear here.</pre></details></section></main><script>
const button=document.querySelector('#run'),status=document.querySelector('#status'),result=document.querySelector('#result'),summary=document.querySelector('#summary');function fact(label,value){const node=document.createElement('div');node.className='fact';const l=document.createElement('span');l.textContent=label;const v=document.createElement('strong');v.textContent=value;node.append(l,v);return node}button.addEventListener('click',async()=>{button.disabled=true;status.textContent='Running…';result.textContent='';summary.replaceChildren();summary.classList.add('hidden');try{const response=await fetch('./api/v1/advise',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({query:document.querySelector('#query').value,failure:document.querySelector('#scenario').value})});const body=await response.json();if(!response.ok)throw new Error(body.detail||`HTTP ${response.status}`);summary.append(fact('Outcome',body.outcome),fact('Model',body.model_status),fact('Tools executed',body.executed_tools.join(', ')||'none'),fact('Evidence records',String(body.evidence.length)),fact('Human approval',String(body.human_approval_required)),fact('Trace ID',body.trace_id));summary.classList.remove('hidden');result.textContent=JSON.stringify(body,null,2);status.textContent=`Outcome: ${body.outcome} · ${body.elapsed_ms} ms · Compare this state with the guide.`;}catch(error){status.textContent='Request failed';result.textContent=String(error);}finally{button.disabled=false;}});
</script></body></html>"""


@app.get("/health")
async def health():
    return {"status": "healthy", "profile": profile.name, "failure_injection": profile.lab_failure_injection}


@app.post("/api/v1/advise")
async def advise(request: IncidentRequest):
    return await service.advise(request)
