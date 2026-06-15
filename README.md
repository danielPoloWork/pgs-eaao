# Enterprise Agentic Architecture Orchestrator (EAAO)

> A language-agnostic meta-project that reproduces the **enterprise agent system** of
> `pbr-cpp-memory-pool` for *any* new project, in *any* language, with *any* toolchain —
> by interviewing the maintainer, recording the answers in a single manifest, and
> rendering a complete, governed repository from parameterized templates.

EAAO is not the product. EAAO is the **factory** that stamps out products that all
share the same technical-enterprise structure, the same GitHub workflow, the same
quality gates, and the same AI-agent contract — regardless of programming language,
framework, or tooling.

It exists to answer one question:

> *"We built `pbr-cpp-memory-pool` to an enterprise bar — agents, ADRs, CI matrix,
> consistency lint, SemVer governance. How do we get the **same** rigor on the next
> project, which is in Rust / Python / TypeScript / Go / Java / …?"*

The answer: point the **Enterprise Project Architect** agent at EAAO, run the
**intake interview**, and let it generate the new repository.

---

## What you get out of it

Running the orchestrator against a fresh project idea produces a new repository that
already contains, on day zero:

| Concern | Reproduced artifact |
|---|---|
| **Agent contract** | `AGENTS.md` (source of truth) + `CLAUDE.md` / `GEMINI.md` adapters, with the senior-architect persona bound to *the new project's* language and stack |
| **Source layout** | Maven-style cross-language tree `src/{main,test,bench}/<lang>/<group-path>/<project>/` — identical shape, language-appropriate segment |
| **Git governance** | Conventional Commits, branch-naming, one-item-per-PR / one-PR-at-a-time, the agent-vs-human boundary, the PR template + PR-metadata policy |
| **Documentation system** | ADRs (+ template + index), design-patterns catalogue (+ the 8-category taxonomy), spec template, session journal, bug ledger, changelog split, releases |
| **Quality gates** | A GitHub Actions CI workflow wired to the chosen toolchain's build / test / format / lint / sanitize commands, plus the agent-runnable `consistency_lint.py` |
| **Versioning** | SemVer policy, milestone-driven release flow, post-release maintenance / hotfix / deprecation / security protocol |

Every one of these is a **parameterized copy** of what already works in
`pbr-cpp-memory-pool`. The genericity lives in three places:

1. **Language profiles** (`orchestrator/profiles/*.yaml`) encode the per-language
   toolchain knowledge (build tool, test framework, formatter, linter, sanitizers,
   CI matrix, source-file extension, namespace style, version-constant location).
2. **The project manifest** (`orchestrator/project.yaml`) captures the maintainer's
   answers — one source of truth for every placeholder.
3. **The templates** (`templates/**`) are the `pbr` artifacts with the
   project-specific facts replaced by `{{PLACEHOLDERS}}`.

---

## How it works (the pipeline)

```text
                 ┌─────────────────────────────────────────────────────────┐
                 │  Enterprise Project Architect agent (agent/...)         │
                 │  persona: senior architect, 20+ yrs, enterprise bar     │
                 └─────────────────────────────────────────────────────────┘
                                          │
   1. INTERVIEW            ───────────────┼───────────────  orchestrator/interview.md
      Ask the maintainer about language(s), frameworks, tools,                 +
      governance, and the project spec (with follow-up questions).   orchestrator/questionnaire.yaml
                                          │
   2. RESOLVE PROFILE      ───────────────┼───────────────  orchestrator/profiles/<lang>.yaml
      Load the toolchain profile(s) for the chosen language(s);
      the profile fills the toolchain-shaped placeholders.
                                          │
   3. WRITE MANIFEST       ───────────────┼───────────────  orchestrator/project.yaml
      Merge answers + profile into one parameter manifest.
                                          │
   4. RENDER              ────────────────┼───────────────  templates/**  →  <new-repo>/**
      Substitute {{PLACEHOLDERS}}, lay down the source tree,
      seed ADR-0001/0002, the roadmap's Milestone 1, the spec.
                                          │
   5. VERIFY              ────────────────┼───────────────  templates/tools/consistency_lint.py
      Run the consistency lint; initialize git; draft the first PR.
                                          ▼
                            A new, governed, enterprise-grade repository
```

The full, ordered procedure is the **generation playbook**:
[`orchestrator/generate.md`](orchestrator/generate.md).

---

## Repository layout

```text
enterprise-architecture-agentic-orchestrator/
├── README.md                       # this file
├── AGENTS.md                       # agent contract for EAAO itself (+ the meta-architect persona)
├── CLAUDE.md / GEMINI.md           # tool adapters → defer to AGENTS.md
├── LICENSE
├── agent/
│   └── enterprise-architect.md     # the reusable "senior project architect" subagent definition
├── orchestrator/                   # the engine
│   ├── README.md                   # how to drive the orchestration
│   ├── interview.md                # the master Q&A protocol the architect runs
│   ├── questionnaire.yaml          # machine-readable question bank
│   ├── generate.md                 # the step-by-step generation playbook
│   ├── placeholders.md             # the canonical placeholder dictionary
│   ├── project.yaml.template       # the project manifest skeleton (copied to project.yaml per run)
│   └── profiles/                   # per-language toolchain knowledge
│       ├── _schema.md              # what every profile must define
│       ├── cpp.yaml  python.yaml  typescript.yaml
│       ├── java.yaml  go.yaml      rust.yaml
├── templates/                      # the parameterized enterprise scaffolding
│   ├── AGENTS.md.tmpl  CLAUDE.md.tmpl  GEMINI.md.tmpl
│   ├── README.md.tmpl  ROADMAP.md.tmpl  CHANGELOG.md.tmpl  SECURITY.md.tmpl  gitignore.tmpl
│   ├── docs/**                     # adr/, patterns/, specs/, bugs/, journal/, workflow/
│   ├── .github/**                  # PULL_REQUEST_TEMPLATE.md, workflows/ci.yml
│   └── tools/consistency_lint.py   # generic, profile-driven congruence checker
└── docs/
    └── adr/                        # ADRs governing EAAO's own design decisions
```

---

## Quickstart

You drive EAAO conversationally through the Enterprise Project Architect agent.

1. **Open this repo with your AI coding agent** (Claude Code, Gemini, Codex). It reads
   `AGENTS.md` and adopts the meta-architect persona.
2. **Say what you want to build.** e.g. *"New project: a Rust token-bucket rate limiter,
   library, GitHub owner `acme`, default branch `main`."*
3. **Answer the interview.** The architect walks
   [`orchestrator/interview.md`](orchestrator/interview.md) — language(s), frameworks,
   tools, governance, and the functional spec — asking only the questions whose answers
   it cannot safely default.
4. **Review the manifest.** The architect writes `orchestrator/project.yaml` and shows it
   to you for confirmation before generating anything.
5. **Generate.** The architect follows [`orchestrator/generate.md`](orchestrator/generate.md)
   to render the new repository, runs the consistency lint, and drafts the bootstrap PR.

You never have to remember the enterprise rules — they are encoded in the templates and
enforced by the lint. You only make the project-specific decisions.

---

## Design principles (why it is shaped this way)

- **One source of truth per fact.** A project fact (name, language, owner, namespace)
  is captured once in `project.yaml` and flows to every artifact via placeholders.
  This is the same anti-drift discipline the generated `consistency_lint.py` enforces.
- **Language knowledge is data, not code.** Adding support for a new language means
  adding one `profiles/<lang>.yaml` — not editing templates. The templates only know
  about *roles* (build tool, test runner, formatter), never specific tools.
- **The generated repo governs itself.** EAAO's job ends at generation. The new repo
  ships with its own `AGENTS.md`, CI, and lint, so it is self-sufficient and is *not*
  coupled back to EAAO.
- **English on disk, any language in chat.** Like the reference project, every
  generated artifact is English; the interview itself may be conducted in the
  maintainer's language.
- **Human owns the irreversible steps.** The agent drafts branches, commits, and PRs;
  the human opens, reviews, and merges. EAAO reproduces that boundary verbatim.

---

## Provenance

EAAO is reverse-engineered from `pbr-cpp-memory-pool` — every rule, template, and gate
here has a concrete origin in that project's `AGENTS.md`, `docs/`, `.github/`, and
`tools/consistency_lint.py`. See [`docs/adr/`](docs/adr/) for the decisions that shaped
the generalization.
