#!/usr/bin/env python3
"""EADOS phase runner — the deterministic, state-driven checker behind `/eados <phase>`.

Given a project manifest, it reads `delivery_state.phase` and the workflow spec
(`orchestrator/os/workflow/workflow.yaml`) and prints the **legal next transitions** — each with
its entry gates and whether it needs human confirmation. It is the thin "engine" the RFC calls
for: a pure function over data. It **never advances state** — it reports what is legal; the agent
proposes a transition, the gates validate it, and the human confirms every human-gated step
(`AGENTS.md` §6).

Dependency-free: the Python standard library plus the sibling renderer's YAML loader.

    python .eados-core/tools/phase_runner.py <manifest>     # report the legal next transitions
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # .eados-core/
sys.path.insert(0, HERE)
import render  # noqa: E402  — the hand-rolled, dependency-free YAML loader (sibling tool)

WORKFLOW = os.path.join(ROOT, "orchestrator", "os", "workflow", "workflow.yaml")


def load_workflow(path=WORKFLOW):
    with open(path, encoding="utf-8") as handle:
        return render.load_yaml(handle.read())


def state_ids(workflow):
    return [s.get("id") for s in (workflow.get("states") or []) if isinstance(s, dict)]


def current_phase(manifest):
    """The manifest's current phase; defaults to `init` when there is no delivery_state yet
    (a legacy / freshly-initialized manifest)."""
    ds = manifest.get("delivery_state") if isinstance(manifest, dict) else None
    return ds.get("phase", "init") if isinstance(ds, dict) else "init"


def legal_transitions(workflow, phase):
    """The transitions whose `from` == phase, in declared order (deterministic)."""
    return [t for t in (workflow.get("transitions") or [])
            if isinstance(t, dict) and t.get("from") == phase]


def report(manifest_path, out=sys.stdout):
    with open(manifest_path, encoding="utf-8") as handle:
        manifest = render.load_yaml(handle.read())
    workflow = load_workflow()
    states = state_ids(workflow)
    phase = current_phase(manifest)
    print(f"current phase: {phase}", file=out)
    if phase not in states:
        print(f"  ERROR: '{phase}' is not a declared workflow state {states}", file=out)
        return 1
    transitions = legal_transitions(workflow, phase)
    if not transitions:
        print("  (terminal phase — no outgoing transitions)", file=out)
        return 0
    print("legal next transitions:", file=out)
    for t in transitions:
        gates = ", ".join(t.get("entry_gates") or []) or "—"
        human = "  [human-gated — the owner confirms]" if t.get("human_gate") else ""
        print(f"  -> {t.get('to')}   (gates: {gates}){human}", file=out)
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: phase_runner.py <manifest>", file=sys.stderr)
        return 2
    return report(argv[0])


if __name__ == "__main__":
    sys.exit(main())
