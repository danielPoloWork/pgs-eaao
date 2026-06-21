# `/eados init` — initialize a governed project

The **entry command** of the pipeline. It frames the project and writes the initial manifest so
every later phase has state to read. Owned by the **enterprise-architect** role.

## Procedure

1. **Frame** — run interview [Phase 0](../interview.md) (Q0.1–Q0.4), **including
   `Q0.4 — development target`** (`software` / `game` / `mobile`), which loads the matching
   [`domains/<domain>.yaml`](../domains/_schema.md).
2. **Write the manifest skeleton** — copy [`project.yaml.template`](../project.yaml.template) to
   `orchestrator/project.yaml` and fill the framing facts: `identity`, the top-level `domain`, the
   `schema_version`, and a `delivery_state` block with `phase: init` (empty `checkpoints` /
   `refs`). Leave the deeper sections (language, toolchain, spec, …) for their phases.
3. **Confirm** — present the skeleton to the maintainer (the cheap checkpoint; `AGENTS.md` §5).
4. **Report the next move** — run the deterministic phase runner:
   ```bash
   python .eados-core/tools/phase_runner.py orchestrator/project.yaml
   ```
   At `phase: init` it reports the one legal transition, `-> design` (gate `manifest-valid`,
   **human-gated**).
5. **Hand off** — the maintainer chooses the next phase:
   - the **delivery pipeline** → `/eados design` (authoring RFCs; lands in M2); or
   - the **classic one-shot path** → finish the full interview (Phases 1–5) and `/eados scaffold`
     ([`generate.md`](../generate.md)) to render the repository as today.

## Boundary

The agent **drafts** the manifest and **proposes** the transition the phase runner reports; the
**human confirms** every human-gated move and owns the irreversible steps. `init` never renders
or commits anything on its own.

## Backward compatibility

`init` is additive. A maintainer who ignores the pipeline and runs the classic interview →
`render.py` flow is unaffected: `delivery_state` is optional and the renderer ignores it.
