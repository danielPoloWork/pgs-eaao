# `workflow.yaml` — schema

The project **state machine**: the phases (states), the legal transitions between them, the
registry of gates a transition must clear, and the per-domain overlays that adapt the machine
to a target (software / game / mobile). The orchestrator is **state-driven**: a thin
deterministic checker reads the persistent manifest's current state plus this spec and computes
which transitions are *legal now*; the agent **proposes** a transition, the gates validate it
mechanically, and a human confirms every `human_gate: true` step. No transition is automatic.

`eados_lint` (`os-spec-completeness`) requires the instance to define every top-level key
below. The item shapes (documented here) are enforced at runtime by the workflow checker built
in M2; the lint guarantees the file parses and is structurally present.

## Required structure

```yaml
version:            # integer schema version (manifest pins the version it was written against)
states:             # the phases, in canonical order
transitions:        # legal, gated moves between states; never automatic
gates:              # the gate registry — lint/test/security/build/human checks, uniform shape
domain_overlays:    # per-domain adaptations (insert/remove states, add gates, reorder)
```

## Item shapes (runtime-enforced, M2)

- **`states[]`** — `{ id, role, produces[] }`. `id` is the phase name; `role` is the owning
  role from [`authority.yaml`](../authority/authority.yaml); `produces` lists the artifact
  kinds the phase writes.
- **`transitions[]`** — `{ from, to, entry_gates[], human_gate }`. `entry_gates` are gate
  ids that must pass before the move; `human_gate: true` requires explicit human confirmation.
- **`gates[]`** — `{ id, kind, runs, blocking, required_for[] }`. `kind ∈
  {lint, test, security, build, human, manual}`; `runs` is the command or `human:<who>` /
  `manual:<description>`; `blocking: true` means a red gate halts the transition; `required_for`
  lists the transition `to`-states that depend on it.
- **`domain_overlays`** — a mapping `domain → { insert_states[], add_gates[], … }`. Absent
  keys mean "inherit the base machine unchanged".

## Invariants

- Every `transitions[].from`/`to` is a declared `states[].id`.
- Every `transitions[].entry_gates[]` and `gates[].required_for[]` references a declared id.
- `scaffold` is the only state that renders the repository (today's factory); it reads the
  manifest like every other phase and writes files — it never calls another phase directly,
  so generation stays decoupled from governance (they share state via the manifest only).
