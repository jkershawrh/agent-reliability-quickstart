# When Agents Fail — Reliable Agentic AI on OpenShift

A 75-minute Red Hat and Intel quickstart-to-lab showing how a NOC incident
advisor fails safely on Red Hat OpenShift with CPU inference on Intel Xeon.

The project implements a portable OpenAI-compatible inference adapter,
MCP-compatible tool policy, evidence validation, bounded retry/degraded mode,
structured decision metadata, GitOps manifests, an OpenShift Pipeline
qualification suite, and six Showroom-ready Antora modules.

## Secure defaults

- Failure injection is disabled in `config/reliability-profile.yaml`.
- The agent is read-only and always requires human approval.
- Model credentials come from the `model-connection` Secret and are never
  rendered into Showroom content or API output.
- The default service account has no resource-mutation RBAC.
- The local guardrail is deterministic developer scaffolding. Flightpath
  certification must validate the same contract through supported OpenShift AI
  TrustyAI/NeMo Guardrails.

## Local validation

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
make test
make run
```

The application uses deterministic demo evidence when `MCP_URL` is empty and
deterministic demo inference when `MODEL_ENDPOINT` is empty. This allows the
reliability controls to be tested without pretending that local mode validates
the Flightpath model or Operators.

## OpenShift deployment

Create a `model-connection` Secret with `endpoint`, `model`, and tenant-scoped
`api-key` entries, then apply `deploy/base` for safe mode or `deploy/lab` for
the controlled failure exercises. Cluster-scoped Operator lifecycle remains a
Launchpad platform responsibility.

## Attribution

The portable agent protocol and quickstart structure are informed by the
existing `rh-ai-quickstart/multi-agent-quickstart` pattern. This repository is
an original reliability-focused implementation and contains no copied RHDP
catalog or provisioning assets.

Licensed under the MIT License.

