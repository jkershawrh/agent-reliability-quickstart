# Build a Reliable Agentic AI Workflow on OpenShift

## Overview

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

## Table of contents

- Architecture and product roles
- Requirements
- Deploy
- Repository structure
- Validation and certification
- References

## Architecture and product roles

OpenShift supplies isolation and identity; OpenShift AI supplies model serving
and supported guardrails; OpenShift Pipelines proves behavior; OpenShift GitOps
restores the known-good state; Intel Xeon supplies CPU inference capacity.

## Requirements

- OpenShift 4.21-compatible cluster and `oc` access
- Supported OpenShift AI, OpenShift Pipelines, and OpenShift GitOps Operators
- Tenant-scoped access to the Flightpath model gateway
- Python 3.9+ for local control testing

## Deploy

Use `oc apply -k deploy/base` after Launchpad creates the tenant-scoped
`model-connection` Secret. The lab overlay is deliberately separate and is
only used in controlled learner namespaces.

## Repository structure

- `src/`: API, MCP service, policy, guardrails, and inference adapter
- `config/`: safe and lab-only reliability profiles
- `deploy/`: OpenShift, GitOps, Pipelines, and OpenShift AI integration assets
- `modules/`: Showroom-ready learner content
- `tests/`: contract, safety, publication, and certification definitions

## Validation and certification

`make precommit` is the local gate. Live model, guardrail, image, lifecycle,
multi-tenant, and 25-seat evidence are required before Launchpad activation.

## References

- Red Hat OpenShift AI supported configurations
- Red Hat OpenShift AI TrustyAI and NeMo Guardrails documentation
- Model Context Protocol and OpenAI-compatible chat-completion interfaces

## Tags

`openshift` `openshift-ai` `pipelines` `gitops` `intel-xeon` `mcp` `agentic-ai`
