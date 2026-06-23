#!/usr/bin/env python3
"""EADOS risk score — the audit phase's deterministic risk model (roadmap 4.1 / 4.4).

A change's risk is a function of its **security surface** (sensitive paths touched), its **size**
(lines changed), and its **blast radius** (distinct areas). At/above the (per-domain) mandatory-gate
level, the `security-auditor` gate is REQUIRED. Config is data
(`orchestrator/os/risk/risk.yaml`); the weights are here. No model in the loop — same inputs, same
score. Dependency-free (stdlib + the sibling renderer's YAML loader).

    python .eados-core/tools/risk_score.py <path> [<path> ...] [--lines N] [--domain D]
    git diff --cached --name-only | xargs python .eados-core/tools/risk_score.py --lines 250
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # .eados-core/
sys.path.insert(0, HERE)
import render  # noqa: E402  — the hand-rolled, dependency-free YAML loader

RISK_SPEC = os.path.join(ROOT, "orchestrator", "os", "risk", "risk.yaml")
DEFAULT_LEVELS = ["low", "medium", "high", "critical"]


def load_risk(path=RISK_SPEC):
    with open(path, encoding="utf-8") as handle:
        return render.load_yaml(handle.read())


def _glob_re(glob):
    """`**` matches across directories; `*` within a segment; everything else literal."""
    out, i = [], 0
    while i < len(glob):
        if glob[i:i + 2] == "**":
            out.append(".*")
            i += 2
        elif glob[i] == "*":
            out.append("[^/]*")
            i += 1
        else:
            out.append(re.escape(glob[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def _matches_any(path, globs):
    return any(_glob_re(g).match(path) for g in globs or [])


def score(paths, lines, cfg):
    """Return (level, factors) for a change touching `paths` with `lines` changed."""
    paths = [p.replace("\\", "/") for p in paths]
    levels = cfg.get("levels") or DEFAULT_LEVELS
    buckets = cfg.get("size_buckets") or {}
    points, factors = 0, []

    if any(_matches_any(p, cfg.get("security_globs")) for p in paths):
        points += 3
        factors.append("security-surface")

    big, med = int(buckets.get("L", 400)), int(buckets.get("M", 100))
    if lines >= big:
        points += 2
        factors.append("large-change")
    elif lines >= med:
        points += 1
        factors.append("medium-change")

    areas = {p.split("/", 1)[0] for p in paths if p}
    if len(areas) >= 3:
        points += 1
        factors.append("wide-blast-radius")

    idx = 0 if points == 0 else 1 if points <= 2 else 2 if points <= 4 else 3
    return levels[min(idx, len(levels) - 1)], factors


def requires_security_gate(level, cfg, domain=None):
    """True when `level` is at/above the effective mandatory-gate level (the domain override if
    present, else the default)."""
    levels = cfg.get("levels") or DEFAULT_LEVELS
    threshold = cfg.get("mandatory_gate_level", "high")
    override = (cfg.get("domain_overrides") or {}).get(domain or "", {})
    if isinstance(override, dict) and override.get("mandatory_gate_level"):
        threshold = override["mandatory_gate_level"]
    return levels.index(level) >= levels.index(threshold)


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="EADOS risk score for a change.")
    ap.add_argument("paths", nargs="+", help="the paths the change touches")
    ap.add_argument("--lines", type=int, default=0, help="lines changed (default 0)")
    ap.add_argument("--domain", default=None, help="the project domain (per-domain threshold)")
    args = ap.parse_args(argv)
    cfg = load_risk()
    level, factors = score(args.paths, args.lines, cfg)
    gate = requires_security_gate(level, cfg, args.domain)
    print(f"risk: {level}  (factors: {', '.join(factors) or 'none'})")
    dom = f" [domain={args.domain}]" if args.domain else ""
    print(f"security-auditor gate: {'REQUIRED' if gate else 'optional'}{dom}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
