# Roadmap — EADOS

The **single source of truth** for EADOS's own delivery plan, from start to finish.
[RFC-0001](0001-eados-delivery-os.md) ratifies the design and points here for the schedule.

- **Living & checkbox-driven.** When an item completes in a PR, flip its checkbox
  (`- [ ]` → `- [x]`) **in the same PR**. New work goes at the bottom of its milestone with a
  fresh `<milestone>.<task>` number; never renumber.
- **Versioning:** pre-1.0, milestone-driven (`AGENTS.md` §6).
- **Invariant:** the factory keeps working unchanged throughout; every phase is opt-in, so a
  user who only wants `scaffold` (today's generation) sees no behavior change.
- **Foundation:** [RFC-0001](0001-eados-delivery-os.md) + the machine-readable specs under
  [`orchestrator/os/`](../../orchestrator/os/README.md).

## Status

| Item | State |
|------|-------|
| Rename EAAO → EADOS | ✅ merged (#33) |
| Design package — RFC-0001 + OS specs + diagrams | ✅ merged (#35) |
| **M1 — Foundation** | ✅ **done** — M1-A..E merged (#37–#41) |
| **M2 — design phase + roles** | ✅ **done** — M2-A..E merged (#42–#46) |
| **M3 — plan phase + traceability** | ✅ **done** — M3-A..C merged (#47–#49) |
| **M4 — audit phase + risk** | ✅ **done** — M4-A..C merged (#50–#52) |
| **M5 — refactor (brownfield)** | ✅ **done** — M5-A..D merged (#53–#56) |
| **v2.0.0 release** | ✅ tagged on #70's merge — GitHub Release drafted, awaiting human publish |
| **M6 — hardening & UX** | 🚧 in progress — 6.1–6.5 + 6.9 done (#63, #64, #65, #66, #68, #76); 6.6–6.8 planned (#67, #69, #72) |

Legend: ⏳ not started · 🚧 in progress · ✅ done.

---

## Milestone 1 — Foundation: domain axis, persistent manifest, role authority, `/eados init`

**Goal.** Lay the data foundation the whole pipeline reads from, and the entry command — without
changing how generation behaves today.

- [x] 1.1 Add the **domain/target axis** as data: `orchestrator/domains/_schema.md` +
      `_template.yaml`, and seeds `software.yaml`, `game.yaml`, `mobile.yaml` (each declaring its
      roles, artifacts — GDD vs PRD, NFR axes — RAM/GPU/framerate for `game`, and milestone
      vocabulary — Alpha/Beta/RC vs SemVer).
- [x] 1.2 `eados_lint`: a **`domain-completeness`** gate (every `domains/<d>.yaml` defines every
      schema key), mirroring `profile-completeness`.
- [x] 1.3 Interview: new **`Q0.4 — development target`** loads the domain profile; the manifest
      gains a `domain` field.
- [x] 1.4 Promote the manifest to a **persistent, reference-based `delivery_state`** block
      (current phase, checkpoints, cross-link ids) with a `schema_version` (**resolves OQ1**).
- [x] 1.5 Wire the **authority block** to the existing roles (persona in `agent/*.md` ↔ authority
      in `authority.yaml`), making the persona≠authority separation real.
- [x] 1.6 Ship the **`/eados init`** command surface (entry skill) + a thin state-driven
      phase-runner skeleton that reads `workflow.yaml` and reports the legal next transitions.

**Acceptance gate.** All lints green (incl. `domain-completeness`); render-smoke unchanged; a
chosen domain selects roles/artifacts/NFRs/milestone-vocabulary purely as data.
**Depends on:** RFC-0001, `orchestrator/os/` specs.

---

## Milestone 2 — `design` phase (RFC) + Product/Delivery roles + workflow checker + authority gate

**Goal.** Make the first governance phase real: author/import RFCs under a review protocol, with
the new org-chart roles and the deterministic engine that gates phase transitions.

- [x] 2.1 Add personas `agent/{product-manager,tech-lead,producer}.md` + the **domain-overlay**
      pattern (`agent/domains/<domain>/<role>.md`, e.g. the `game` `product-manager` = Game
      Designer); recursive `agent-registry` + `authority-personas` lints. **OQ4 resolved:** one
      authority role + a domain-specialized persona overlay (not two role IDs).
- [x] 2.2 RFC template + the **RFC-review protocol** under `orchestrator/os/rfc/` (schema +
      config + template + protocol), and `tools/rfc_check.py` enforcing the **`rfc-approved`** gate
      (required sections + a `tech-lead` approval record).
- [x] 2.3 The **deterministic workflow checker**: `phase_runner.py` returns the legal transitions
      and (new `--propose <to>`) validates a proposed transition and **emits the checkpoint** to
      write — read-only; the agent writes it, the human confirms H-gates.
- [x] 2.4 The **authority gate** — `tools/authority_check.py <role> <paths>` enforces the
      `authority.yaml` ownership map: a path the acting role may not write (outside its
      `owns`/`may_draft`) is rejected. Agent-invoked (CI can't know the actor's role), tested.
- [x] 2.5 Ship the **`/eados design`** command surface (`commands/design.md` — authority-check →
      author the RFC from the template → review → `rfc_check` → `phase_runner --propose plan`).

**Acceptance gate.** A sample RFC passes the review gate; an out-of-authority edit is rejected by
the authority gate; the checker computes the correct legal transitions for a given state.
**Depends on:** M1.

---

## Milestone 3 — `plan` phase: roadmap from RFCs + the traceability graph

**Goal.** Co-create the roadmap from RFCs through a real negotiation, and build the lineage graph
that makes delivery auditable.

- [x] 3.1 The **roadmap-negotiation protocol** under `orchestrator/os/plan/` (schema + `plan.yaml`
      config + `negotiation-protocol.md`): PM proposes → `tech-lead` sizes (T-shirt) → `producer`
      reconciles capacity, anchored to artifacts (no "multi-agent theatre").
- [x] 3.2 Ship the **`/eados plan`** command surface (`commands/plan.md` — negotiate via `plan.yaml`
      → write `ROADMAP.md` → `traceability.py` (`roadmap-covers-rfcs`) → `--propose scaffold`).
- [x] 3.3 The **traceability-graph builder** — `tools/traceability.py` builds the design-time
      `RFC → milestone` edges from the roadmap (the Git-side `PR → commit → release` edges land in
      M4, derived from the `git`-spec cross-links).
- [x] 3.4 The **`roadmap-covers-rfcs`** gate — `traceability.py` fails when an RFC is addressed by
      no milestone (every RFC maps to ≥1 milestone; generalizes the spec-coverage-map). Wired into
      `workflow.yaml`.

**Acceptance gate.** Every RFC maps to ≥1 milestone; the graph builds from a sample project's
cross-links.
**Depends on:** M2.

---

## Milestone 4 — `audit` phase: risk scoring + enforced `traceability-lint`

**Goal.** Stand up continuous audit with a real risk model, and turn the traceability graph into
a blocking gate.

- [x] 4.1 A **risk model** — `tools/risk_score.py` + the `risk` OS spec: score = f(security surface
      × change size × blast radius), generalizing the `reviewer` + `security-auditor` roles.
- [x] 4.2 Ship the **`/eados audit`** command surface (`commands/audit.md` — `traceability-lint` +
      `risk_score` → the `security-auditor` gate above threshold → a risk register).
- [x] 4.3 The **`traceability-lint`** gate — `traceability.py --links` extends the graph to the
      Git-side edges (`milestone → PR → commit → release`) and fails on a dangling edge (an RFC with
      no PR, a PR missing its RFC/milestone, a release not tracing to a PR + commit).
- [x] 4.4 Risk-threshold → **mandatory `security-auditor` gate** at/above the level; the threshold
      is **per-domain configurable** in `risk.yaml` (**OQ2 resolved**: a global default + domain override).

**Acceptance gate.** A seeded dangling edge fails `traceability-lint`; a change above the risk
threshold forces the security gate.
**Depends on:** M3.

---

## Milestone 5 — `refactor` (brownfield) — last, sandboxed

**Goal.** Bring an existing repository up to the standard via incremental, gated migrations —
the highest-risk phase (it edits real user code), so it is sequenced last and write-contained.

- [x] 5.1 **Brownfield reader** — `tools/brownfield.py` (READ-ONLY) maps an existing repo against
      the EADOS standard (agent contract, docs system, CI, source tree) and reports the gaps to migrate.
- [x] 5.2 **Migration planner** — `tools/migration_planner.py` (READ-ONLY) orders the brownfield
      gaps into incremental steps (one logical change each), lowest-risk / most-foundational first.
- [x] 5.3 A **write-contained sandbox** — `tools/sandbox.py` (defense-in-depth, on the renderer
      write-guard principle of [ADR-0007](../adr/0007-renderer-write-guards-and-validation-independence.md)):
      a write may only land inside the target repo (traversal/absolute/symlink/`.git`/clobber refused).
- [x] 5.4 Ship the **`/eados refactor`** command surface (`commands/refactor.md` — brownfield read
      → plan → sandboxed, gated, **additive** migration PRs, one logical change each).

**Acceptance gate.** A fixture repo is migrated via gated PRs; no write escapes the sandbox; each
PR passes the standard's gates.
**Depends on:** M4.

---

## Milestone 6 — hardening & UX (post-v2.0.0)

**Goal.** Close the automation/completeness gaps (G2–G4) and feature suggestions (F1–F4) surfaced
by the v2.0.0 enterprise review, plus the one cross-spec scope deferred from #62 — **without
changing the shipped pipeline's behavior**. Each item is one logical change (one PR), tracked as a
GitHub issue under the `M6 — hardening & UX` milestone (#6).

- [x] 6.1 (G4, #65) **End-to-end phase smoke test** — a fixture that runs a complete *phase flow*
      (`design → plan → audit`) over the real tool CLIs to catch tool-integration bugs the per-tool
      unit tests miss: each gate passes on a coherent fixture and fails on a broken one, and
      `phase_runner --propose` matches every transition declared in `workflow.yaml`
      (`tools/tests/test_phase_smoke.py`).
- [x] 6.2 (F3, #68) **Risk-model weights as data** — the factor weights, blast-radius threshold, and
      points→level cutoffs move from `risk_score.py` into `risk.yaml`, each **per-domain overridable**
      like `mandatory_gate_level`; the scorer reads them via `resolve(cfg, domain)` with built-in
      fallbacks (back-compat, default scores unchanged). Full "knowledge as data"; `risk/_schema.md` updated.
- [x] 6.3 (G2, #63) **Single-artifact render for `refactor`** — `tools/render_artifact.py` renders
      one template with the manifest context (the same gates as a full render) and places it via
      `sandbox.safe_write`; the "render the missing artifact → sandbox" step in `refactor.md` now
      invokes it (no longer manual).
- [x] 6.4 (F1, #66) **`/eados status` (doctor)** — a read-only `tools/doctor.py` (+ the
      `commands/status.md` surface) reports current phase, legal transitions (+ gates/human-gating),
      refs, and traceability coverage at a glance — composing `phase_runner` + `traceability`; exits
      non-zero on an actionable problem (undeclared phase, uncovered RFC, dangling edge).
- [x] 6.5 (G3, #64) **Thin CLI phase orchestrator** — `tools/eados.py <phase> <manifest>` runs a
      phase's deterministic outgoing gates (data-driven from `workflow.yaml`), marking render-time /
      human gates `[manual]`, then reports the legal next moves; `eados.py status` is the doctor. The
      executable spine beneath the markdown `/eados <phase>` procedures.
- [ ] 6.6 (F2, #67) **Auto-derive traceability links from PR bodies** (via `gh`) — replace the
      hand-written `links.yaml`, feeding `traceability-lint` real `PR → commit → release` edges.
- [ ] 6.7 (F4, #69) **Version-lockstep dogfooding** — apply the generated repos' `version-lockstep`
      gate to EADOS's own README release badge (the factory held to the bar it imposes downstream).
- [ ] 6.8 (#72) **Cross-spec gate → cross-cutting gates** — extend `cross-spec-consistency` to
      validate cross-cutting (non-phase) gate references too; `git.yaml`'s `traceability-lint` was
      intentionally left out of the phase-gate registry check in #62.
- [x] 6.9 (#76) **Auto-sync shared action pins into templates** — `tools/sync_action_pins.py`
      (`--check` / `--fix`) rewrites the rendered workflow templates' action pins to the factory CI's,
      so a Dependabot `github-actions` bump needs no manual companion edit to pass the `action-pins`
      lockstep gate (ADR-0009) — and the `dependabot-pin-sync` workflow (`workflow_run`, not
      `pull_request_target`; ADR-0013) applies it automatically on a Dependabot PR (true zero-touch).

**Acceptance gate.** Each item lands as a gated PR with tests; no regression to the v2.0.0 pipeline;
any new data/spec is `_schema`-validated and lint-gated (no special-casing in code — the
anti-fragmentation invariant below).
**Depends on:** v2.0.0 (post-release); incremental — items are independent.

---

## Cross-cutting invariants (every PR, every milestone)

These are **not tasks to complete** but **invariants upheld in every PR** — held across M1–M5 and
the v2.0.0 release, and binding on all future work (M6 included). They are deliberately not checkboxes.

- **English on disk; agent drafts / human merges & publishes; Conventional Commits; one logical
  change per PR; one PR at a time.**
- **Each new spec / role / domain ships `_schema`-validated and lint-gated** — never a special case
  in code (anti-fragmentation), enforced by `eados_lint`'s `os-spec-completeness`,
  `domain-completeness`, `authority-personas`, and `agent-registry` gates.
- **Each milestone keeps RFC-0001, this roadmap, the affected specs, and the `CHANGELOG` in sync in
  the same PR.**

## Open questions (each resolved within its milestone)

| OQ | Question | Resolved in |
|----|----------|-------------|
| OQ1 | Manifest schema-versioning mechanics | ✅ M1-B (item 1.4) — embedded `schema_version` |
| OQ4 | product-manager vs game-designer role shape | ✅ M2-A (item 2.1) — one authority role + domain persona overlay |
| OQ2 | Risk-score thresholds (per-domain?) | ✅ M4-A (item 4.4) — global default + per-domain override in risk.yaml |
| OQ3 | Committed, CI-generated SVG vs Mermaid-only | ✅ Resolved — Mermaid-only (no Node toolchain; `.mmd` committed, SVG on demand) |
