# Flightpath one-seat qualification — 2026-09-24

## Environment

- OpenShift: 4.21.10
- Red Hat OpenShift AI Operator: 3.5.1 (`stable-3.5`)
- Red Hat OpenShift Pipelines: 1.24.0 (`pipelines-1.24`)
- Red Hat OpenShift GitOps: 1.21.4
- Application image: `quay.io/rh-ee-jkershaw/agent-reliability-quickstart@sha256:ccb631bb51942c71ae02f167fb39dc6e0931d7624243890acafcdbd510a1d0ce`
- Source revision: `cf0d72b21bcb3a8a08df4a94a8a5fc6d02ed2566`
- Model: `granite-3.2-8b-tools`, CPU inference through the Flightpath candidate gateway
- Launchpad workshop: `c3c33daf-3134-42e5-91b3-6a2a1415bea0`
- Launchpad session: `eccabba6-0851-451c-86f1-0e2364512732`

## Result

PipelineRun `agent-reliability-qualification-z2qvh` succeeded in the ordered
tenant namespace `launchpad-jkershaw-agent-reliability-a17bbf`.

| Scenario | Outcome | Application time |
| --- | --- | ---: |
| Healthy | recommended | 13,766.66 ms |
| Prompt injection | abstained | 0.07 ms |
| Unauthorized tool | denied | 0.02 ms |
| Inference timeout | degraded | 32.37 ms |

The healthy response included alarm, telemetry, and runbook evidence and
required human approval. No credentials were included in Pipeline results.
The Launchpad lifecycle generated a tenant-scoped LiteLLM key: the issued key
returned HTTP 200 while a request without a key returned HTTP 401. Reclaim
removed the key from the persisted session, recorded a provider-confirmed
revocation receipt, deleted the tenant namespace, and removed its GitOps
applications.

## Clean re-order

A second independent order, workshop
`db8c0e87-166f-4298-b513-3637a128783e`, provisioned source revision
`04f8feee58965a8b6e9397487b61db0928869a9d` after the first workshop had been
fully reclaimed. Both workload and Showroom content were pinned to that
revision, and both GitOps applications were healthy and synced. PipelineRun
`agent-reliability-qualification-qrs2h` passed all four scenarios; healthy CPU
inference completed in 13,827.77 ms. The fresh seat key returned HTTP 200 and a
missing key returned HTTP 401. Final reclaim recorded provider-confirmed key
revocation, cleared the persisted key, and deleted the second tenant namespace.

## Five-seat qualification

Workshop `59db3cb0-e480-42e1-bc51-84b92dc518eb` provisioned five isolated seats
from the same immutable release. All 15 application, MCP, and Showroom
deployments became available. The five model keys had five distinct hashes;
every application service account was denied direct Secret reads. Each issued
key returned HTTP 200 and every unauthenticated request returned HTTP 401.

Five qualification PipelineRuns executed concurrently and all passed the
healthy, prompt-injection, unauthorized-tool, and inference-timeout scenarios.
Healthy CPU inference times were 14,667.79, 14,679.99, 14,665.66, 14,781.40,
and 14,710.77 ms. Workshop reclaim produced five provider-confirmed revocation
receipts, cleared every persisted key, and deleted all five tenant namespaces.

## Findings corrected

1. The canary namespace required the standard
   `launchpad.redhat.com/cluster-id=flightpath` label to pass the MaaS ingress
   NetworkPolicy.
2. The five-second lab timeout was too low for CPU inference and was raised to
   30 seconds.
3. The OpenShift Route timeout was raised to 90 seconds so it exceeds the
   bounded retry budget.
4. The private Quay image requires the Launchpad registry pull Secret attached
   to the workload service account.
5. Launchpad's seat-aware GitOps contract requires a Helm chart so it can pass
   only the external Secret name; the endpoint and key never enter Git values.
6. The catalog tabs require explicit `showroom.terminal` and
   `workload.route.workspace` sources.
7. Restricted tenant namespaces require Tekton's supported
   `set-security-context` option and an explicit restricted security context on
   the qualification step.

## Remaining certification gates

- Route input screening through supported TrustyAI/NeMo Guardrails and record
  that external policy decision in the response contract.
- Prove a RHOAI-managed CPU model-serving path or revise the catalog claim to
  describe the current Flightpath gateway accurately.
- Run the 25-seat capacity and tenant-isolation test.
