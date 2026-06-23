# `risk.yaml` — schema

The **risk model** as data (roadmap 4.1 / 4.4; RFC-0001 §7). A change's risk is a function of its
**security surface** (which sensitive paths it touches), its **size**, and its **blast radius**
(how many areas it spans). At or above the **mandatory-gate level** the `security-auditor` gate is
required — a threshold that may be stricter **per domain** (OQ2). The scorer is
[`../../../tools/risk_score.py`](../../../tools/risk_score.py); it generalizes the `reviewer` +
`security-auditor` roles into a standing audit.

`eados_lint` (`os-spec-completeness`) requires the instance to define every top-level key below.

## Required structure

```yaml
version:              # integer schema version
security_globs:       # path globs whose change raises the security-surface factor
size_buckets:         # lines-changed thresholds, { M: <int>, L: <int> }
levels:               # ordered risk levels, lowest -> highest
mandatory_gate_level: # at/above this level the security-auditor gate is REQUIRED (default)
domain_overrides:     # per-domain { mandatory_gate_level } overrides (OQ2)
```

## Item shapes & scoring

The scorer combines weighted factors into points, then buckets points into a `levels` entry:

- **security surface** (`+3`) — any changed path matches a `security_globs` entry (e.g. `.github/**`
  = CI/supply-chain, `tools/**` = the renderer/write-guards per ADR-0007, `**/auth/**`, secrets).
- **size** — `+2` when lines changed ≥ `size_buckets.L`, `+1` when ≥ `size_buckets.M`.
- **blast radius** (`+1`) — the change spans ≥ 3 distinct top-level areas.

Points → level: `0` low · `1–2` medium · `3–4` high · `5+` critical (capped to `levels`).
`requires_security_gate` is true when the level ≥ the effective `mandatory_gate_level` (the domain
override if present, else the default).

## Invariants

- `mandatory_gate_level` and every `domain_overrides[*].mandatory_gate_level` is a value in `levels`.
- The scorer is **deterministic** — same inputs, same score (no model/LLM in the loop).
