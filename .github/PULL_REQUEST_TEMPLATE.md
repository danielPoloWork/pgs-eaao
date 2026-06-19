## Summary

One or two sentences: what changes and why it matters.

## Motivation

Link to the ADR, issue, or audit finding that prompted this work. Non-trivial design
decisions need an ADR under [`.eaao-core/docs/adr/`](../.eaao-core/docs/adr/).

## Changes

- bulleted list of meaningful changes (not a file list)

## Verification

- [ ] `python .eaao-core/tools/eaao_lint.py` passes (placeholder / profile / playbook /
      i18n-freshness integrity)
- [ ] Render-smoke green: `python .eaao-core/tools/render.py .eaao-core/orchestrator/examples/reference.yaml --out /tmp/r` and the generated `consistency_lint.py` passes
- [ ] Tooling tests pass (`tools/tests/test_*.py`) where touched
- [ ] `python -m py_compile` clean on any changed tool

## Documentation Impact

- [ ] `README.md` updated (if the maintainer-facing surface changed)
- [ ] ADR added/updated (if a non-trivial design decision was made)
- [ ] Translations refreshed + `docs/i18n/translation-status.md` bumped (if an English source with translations changed)
- [ ] `CHANGELOG.md` `[Unreleased]` updated
- [ ] PR metadata set — assignee + one type label
