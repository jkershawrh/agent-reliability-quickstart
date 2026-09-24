# OpenShift AI integration

The application consumes the Flightpath tenant-scoped, OpenAI-compatible model
gateway through the `model-connection` Secret. The shared CPU model must be
managed at cluster scope using a Red Hat OpenShift AI release supported on the
installed OpenShift version. Learner namespaces never receive the gateway
master key.

TrustyAI/NeMo Guardrails is the supported external guardrail target. The local
detector keeps local development deterministic; certification must test the
supported guardrail route and record its policy decision in the same response
metadata contract.

No cluster-scoped Operator installation is included in this repository.
Launchpad platform onboarding owns prerequisite validation and installation.

