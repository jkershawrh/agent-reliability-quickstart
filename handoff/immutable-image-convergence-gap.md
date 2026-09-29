# Immutable-image convergence gap

No `demo-story.redhat-intel.com/launchpad-handoff/v1` manifest is emitted for
this repository yet.

The existing Launchpad qualification report is authoritative for the workload
release it names: source revision
`66638c95db0f8a56f80646086e1b639ce4625d1e`, image
`quay.io/rh-ee-jkershaw/agent-reliability-quickstart@sha256:7aff969774fa4b3efac77de4525a046a9c36ce8609de77af20f1077ad17a79d1`,
and successful qualification through 25 seats. That external certification is
recorded without conferring factory authority in
`evidence/external-launchpad-certification.json` (SHA-256
`dde6a4d308d516a6d7a6acca804fcb9e73f9b6a91cdebd4268f17ee85d9a1762`).

The canonical handoff contract also requires a content-addressed presentation
artifact. The qualified Containerfile packages the workload API and MCP
implementation only; the Showroom learner content remains source-owned and is
not included in that image. Reusing the workload image as a presentation image
would therefore be inaccurate.

There is also a release-identity mismatch to resolve before a future handoff:
the qualification report names digest `7aff9697…`, while the current chart
and base manifests pin digest `604331d4…`. This report does not infer that the
latter digest inherited the former digest's qualification.

Convergence requires an authoritative immutable presentation artifact (or a
new combined artifact that actually serves the presentation), its verification
receipt, and an explicit reconciliation of the qualified workload digest.
Launchpad catalog state and the existing qualification record are unchanged.
