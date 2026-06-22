#!/usr/bin/env python3
"""Tests for risk_score — the deterministic risk model: security surface, size, blast radius, and
the per-domain mandatory-gate threshold (OQ2). Dependency-free.

    python .eados-core/tools/tests/test_risk_score.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS)
import risk_score as rs  # noqa: E402  (the module under test)


def check(label, cond, failures):
    if not cond:
        failures.append(label)


def main():
    failures = []
    cfg = rs.load_risk()

    # --- level by factor ---
    lvl, _ = rs.score(["docs/journal/2026-06.md"], 10, cfg)
    check("a small docs change is low", lvl == "low", failures)

    lvl, fac = rs.score([".github/workflows/ci.yml"], 20, cfg)
    check("a CI change is high (security surface)", lvl == "high", failures)
    check("security-surface factor is reported", "security-surface" in fac, failures)

    lvl, _ = rs.score(["tools/render.py"], 500, cfg)
    check("a large tools change is critical", lvl == "critical", failures)

    lvl, _ = rs.score(["src/a.py", "lib/b.py", "app/c.py"], 50, cfg)
    check("a wide non-security change is medium", lvl == "medium", failures)

    # --- glob matcher: security globs ---
    check("**/auth/** matches nested auth code",
          rs._matches_any("src/main/auth/login.py", cfg["security_globs"]), failures)
    check("a plain source file is not security surface",
          not rs._matches_any("src/main/util.py", cfg["security_globs"]), failures)

    # --- mandatory gate: default vs per-domain (OQ2) ---
    check("high requires the gate by default",
          rs.requires_security_gate("high", cfg, None), failures)
    check("medium does not require the gate by default",
          not rs.requires_security_gate("medium", cfg, None), failures)
    check("medium DOES require the gate for the mobile domain",
          rs.requires_security_gate("medium", cfg, "mobile"), failures)
    check("low never requires the gate",
          not rs.requires_security_gate("low", cfg, "mobile"), failures)

    if failures:
        print("test-risk-score: FAIL\n")
        for f in failures:
            print(f"  {f}")
        print(f"\n{len(failures)} expectation(s) failed.")
        return 1
    print("test-risk-score: OK -- security surface, size, blast radius, and per-domain gate hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
