# EADOS — machine-readable OS specs

The four data artifacts that turn EADOS's delivery governance from prose conventions into
**declarative, gate-enforced contracts**. Each spec is *data*, validated by
[`eados_lint`](../../tools/eados_lint.py) (the `os-spec-completeness` check) and elaborated in
[`docs/rfc/0001-eados-delivery-os.md`](../../docs/rfc/0001-eados-delivery-os.md).

The design principle is the same one the language profiles already follow: **knowledge is
data, not code**. Adding a workflow, a role, or a gate is editing a YAML file the lint
validates against a schema — never a special case in a tool.

| Spec | What it governs | Schema + instance |
|------|------------------|-------------------|
| **workflow** | The phase state machine: states, gated transitions, the gate registry, per-domain overlays | [`workflow/_schema.md`](workflow/_schema.md) · [`workflow/workflow.yaml`](workflow/workflow.yaml) |
| **authority** | Roles (separate from persona), the path→role ownership map, the escalation ladder | [`authority/_schema.md`](authority/_schema.md) · [`authority/authority.yaml`](authority/authority.yaml) |
| **git** | Branch/commit/PR/release policy and the PR↔RFC↔milestone cross-link requirement | [`git/_schema.md`](git/_schema.md) · [`git/git.yaml`](git/git.yaml) |

The fourth artifact — the **traceability graph** (requirement → RFC → milestone → PR → commit
→ release) and its lint — is *described* here and in the RFC but is **built in M3/M4**; it is
derived from the cross-links the `git` spec mandates, not stored as a separate file.

> **Status:** these are the **reference instances** that encode the design (RFC-0001). Their
> runtime wiring lands across milestones M2–M4 (see RFC §12). A reference to a role persona or
> a gate runner that does not exist yet is intentional — its milestone adds it. Each instance
> validates today: it parses and defines every key its schema declares.

## Invariants (all instances)

- **English on disk.** Every value is English (`AGENTS.md` §2).
- **Human holds the terminal gate.** Any `human_gate: true` transition and any
  `*_by: human` action is never crossed by an agent (`AGENTS.md` §6).
- **Versioned.** Every instance carries a top-level `version:` so the schema can evolve with
  backward compatibility (the persistent manifest references a spec version).
