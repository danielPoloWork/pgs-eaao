#!/usr/bin/env python3
"""Tests for the EADOS phase runner — the legal-transition checker is correct, pure, and the
workflow spec is internally consistent. Dependency-free (runnable in the self-lint job).

    python .eados-core/tools/tests/test_phase_runner.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS)
import phase_runner as pr  # noqa: E402  (the module under test)


def check(label, cond, failures):
    if not cond:
        failures.append(label)


def main():
    failures = []
    wf = pr.load_workflow()

    # --- current_phase: defaults to init; reads delivery_state when present ---
    check("current_phase default init", pr.current_phase({}) == "init", failures)
    check("current_phase reads delivery_state",
          pr.current_phase({"delivery_state": {"phase": "plan"}}) == "plan", failures)
    check("current_phase tolerates malformed delivery_state",
          pr.current_phase({"delivery_state": "oops"}) == "init", failures)

    # --- legal_transitions: the entry phase ---
    init = pr.legal_transitions(wf, "init")
    check("init -> exactly one transition", len(init) == 1, failures)
    check("init -> design", init and init[0].get("to") == "design", failures)
    check("init -> design is human-gated", init and init[0].get("human_gate") is True, failures)
    check("init -> design gate is manifest-valid",
          init and init[0].get("entry_gates") == ["manifest-valid"], failures)

    # --- plan is a fork: forward to scaffold + resumable back to design ---
    plan = {t.get("to") for t in pr.legal_transitions(wf, "plan")}
    check("plan -> {scaffold, design}", plan == {"scaffold", "design"}, failures)

    # --- scaffold -> audit is automatic (not human-gated; the gates are mechanical) ---
    sc = pr.legal_transitions(wf, "scaffold")
    check("scaffold -> audit, not human-gated",
          sc and sc[0].get("to") == "audit" and not sc[0].get("human_gate"), failures)

    # --- refactor is terminal ---
    check("refactor is terminal", pr.legal_transitions(wf, "refactor") == [], failures)

    # --- an unknown phase yields no transitions (report() flags it; the function is total) ---
    check("unknown phase -> no transitions", pr.legal_transitions(wf, "bogus") == [], failures)

    # --- workflow integrity: every transition endpoint is a declared state ---
    states = set(pr.state_ids(wf))
    for t in wf.get("transitions") or []:
        check(f"transition from '{t.get('from')}' is a declared state",
              t.get("from") in states, failures)
        check(f"transition to '{t.get('to')}' is a declared state",
              t.get("to") in states, failures)

    if failures:
        print("test-phase-runner: FAIL\n")
        for f in failures:
            print(f"  {f}")
        print(f"\n{len(failures)} expectation(s) failed.")
        return 1
    print("test-phase-runner: OK — legal transitions, terminal phase, and workflow integrity hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
