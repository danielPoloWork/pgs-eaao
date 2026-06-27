# `git.yaml` — schema

The **Git/PR/CI/release policy** as data: branch naming, commit convention, the PR rules
(including the mandatory PR↔RFC↔milestone cross-links that feed the traceability graph), and
the release flow (with the explicit **merge ≠ deploy** boundary). This encodes the rules
`AGENTS.md` §6 states in prose, so the workflow gates can enforce them mechanically.

`eados_lint` (`os-spec-completeness`) requires the instance to define every top-level key
below.

## Required structure

```yaml
version:            # integer schema version
branch_naming:      # pattern + the allowed type vocabulary
commit:             # convention, scopes, one-change-per-PR / one-PR-at-a-time
pr:                 # who drafts/opens/merges, metadata, the required cross-links
release:            # SemVer flow, tag flow, the merge!=deploy boundary, delegation flag
traceability:       # the artifact lineage the graph + lint (M3/M4) are built from
```

## Item shapes (runtime-enforced, M3/M4)

- **`branch_naming`** — `{ pattern, types[] }`. `types` is the Conventional-Commit type set.
- **`commit`** — `{ convention, scopes[], one_logical_change_per_pr, one_pr_at_a_time }`.
- **`pr`** — `{ draft_by, opened_by, merged_by, merge_method, assignee, one_type_label,
  required_crosslinks[], template, review_gate }`. `required_crosslinks` (e.g. `[rfc, milestone]`)
  are the references a PR body must carry; the traceability lint fails on a missing edge.
  `review_gate` names the cross-cutting inbound-review gate (`contribution-review`) that
  `/eados review` runs on a PR — a recommendation, never a merge (M8).
- **`release`** — `{ scheme, tag_flow, merge_is_not_deploy, publish_by, delegation_flag }`.
  `merge_is_not_deploy: true` models `merged → tagged/released → deployed` as distinct,
  separately-gated states. `delegation_flag` records whether the owner delegated the publish
  step to the agent (default `false`; the human publishes).
- **`traceability`** — `{ graph, gate }`. `graph` is the lineage string the lint walks.

## Invariants

- `pr.merged_by` and `release.publish_by` are `human` unless `delegation_flag: true`
  (`AGENTS.md` §6 — the agent never merges to the default branch or publishes a release on its
  own authority).
- `pr.required_crosslinks` are the edges the traceability graph (M3/M4) depends on; dropping one
  breaks end-to-end auditability.
