#!/usr/bin/env python3
"""Differential test: the hand-rolled manifest loader must agree with a real YAML parser.

EAAO renders with a dependency-free loader (render.load_yaml) so the everyday path needs no
third-party deps. This test pins that loader to PyYAML on the documented supported subset, so a
future regression (the kind ADR-0006/0008 were written about) fails loudly instead of silently
corrupting a generated repo. PyYAML is a CI-only dependency; absent it, the test skips (exit 0).

    python .eaao-core/tools/tests/test_loader.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
from render import load_yaml  # noqa: E402  (the loader under test)

# Each case is idiomatic manifest YAML; load_yaml must equal yaml.safe_load on all of them.
# The previously-silent corruptions (quote escaping, block chomping) are first-class cases.
CASES = [
    # --- the regressions C2 fixes ---
    ("single-quote escaping",      "tagline: 'it''s a developer''s friend'"),
    ("double-quote escaping",      r'objective: "Parse \"key: value\" pairs"'),
    ("double-quote newline+tab",   r'msg: "line1\nline2\tend"'),
    ("block clip |",               "note: |\n  a\n  b\n"),
    ("block strip |-",             "note: |-\n  a\n  b\n"),
    # `|+` keep-chomping is intentionally out of the guaranteed subset (see render.py header).
    # --- core subset that must keep agreeing ---
    ("plain string",               "name: pbr-cpp-memory-pool"),
    ("string with colon value",    "url: http://example.com:8080/path"),
    ("comma-bearing plain scalar", "tier1: Linux x86_64, Windows x86_64, macOS arm64"),
    ("int",                        "coverage_target: 80"),
    ("bool true/false",            "bench: true\nthreading: false"),
    ("null forms",                 "a: null\nb: ~\nc:"),
    ("quoted empty",               'secondary_lang: ""'),
    ("at-sign quoted",             'assignee: "@me"'),
    ("flow list",                  "scopes: [api, build, tests, docs, ci]"),
    ("flow map in seq",            "matrix:\n  - { os: ubuntu-24.04, toolchain: gcc, preset: debug }\n"),
    ("block seq same indent",      "scopes:\n- api\n- build\n"),
    ("block seq deeper indent",    "scopes:\n  - api\n  - build\n"),
    ("nested mapping",             "language:\n  lang: cpp\n  group_path: it/d4np\n"),
    ("block-style map items",      "matrix:\n  - os: ubuntu-24.04\n    toolchain: gcc\n"),
    ("hash inside quotes",         'hint: "#include <memory_pool.h>"'),
]


def main():
    try:
        import yaml
    except ImportError:
        print("test-loader: SKIP — PyYAML not installed (pip install pyyaml to enforce).")
        return 0

    failures = []
    for label, text in CASES:
        try:
            mine = load_yaml(text)
        except Exception as exc:  # noqa: BLE001 — any crash is a failure
            mine = f"<EXC {exc!r}>"
        ref = yaml.safe_load(text)
        if mine != ref:
            failures.append(f"{label}: load_yaml={mine!r} != pyyaml={ref!r}")

    # End-to-end: the shipped reference manifest must parse identically with both.
    ref_path = os.path.join(ROOT, "orchestrator", "examples", "reference.yaml")
    with open(ref_path, encoding="utf-8") as fh:
        raw = fh.read()
    if load_yaml(raw) != yaml.safe_load(raw):
        failures.append("orchestrator/examples/reference.yaml: load_yaml != pyyaml (deep)")

    if failures:
        print("test-loader: FAIL\n")
        for f in failures:
            print(f"  {f}")
        print(f"\n{len(failures)} loader-fidelity divergence(s).")
        return 1
    print(f"test-loader: OK — loader agrees with PyYAML on {len(CASES)} cases + reference.yaml.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
