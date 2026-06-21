# RFC review protocol

How the `design` phase produces and gates an RFC. Machine-readable config:
[`rfc.yaml`](rfc.yaml); skeleton: [`template.md`](template.md); checker:
[`../../../tools/rfc_check.py`](../../../tools/rfc_check.py). Mirrors the delivery-roles guide §2.

## Roles (authority is data — `../authority/authority.yaml`)

| Step | Who | Output |
|------|-----|--------|
| **Author** | a `tech-lead` (or `product-manager` for a product-facing RFC) | the RFC, from [`template.md`](template.md) |
| **Review** | `reviewer` peers + the `enterprise-architect` (when the change is cross-cutting / touches infra) | **structured findings** (not prose) the author resolves |
| **Approve** | the `tech-lead` (RFC-level) | the **Approval record** in the RFC |

The `reviewer` comments and the architect weighs cross-domain impact, but **only the
`approver_role` approves** — the persona ≠ authority separation made concrete.

## The flow

1. **Draft** — the author writes the RFC (Context, Decision, Alternatives, Consequences) and
   opens it for review. Status: *Draft → In review*.
2. **Review** — reviewers return structured findings; the author addresses each. Anchored to the
   document, never theatre: every comment is a concrete, resolvable item.
3. **Approve** — when findings are resolved, the approver adds the **Approval record**:
   ```
   approved-by: tech-lead (YYYY-MM-DD)
   ```
   Status: *Accepted*.
4. **Gate** — `rfc-approved` is verified mechanically by `rfc_check.py`: the RFC has every
   `required_section` and a well-formed approval by the `approver_role`. Only then is
   `design → plan` legal (the human still confirms the human-gated transition).

## Escalation

A reviewer/approver disagreement follows the authority `escalation` ladder
(`reviewer → tech-lead → enterprise-architect → human-owner`). The human owner is always the
terminal decider (`AGENTS.md` §6).

## Boundary

The agent **drafts** the RFC and **proposes** the transition `rfc_check` reports as legal; a human
approves the RFC (the approval encodes a human decision) and confirms the phase move. No RFC
self-approves.
