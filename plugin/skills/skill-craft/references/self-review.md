# Self-review (the pre-commit dispatch)

**Load when:** dispatching the self-review subagent against a
change to skill-craft's operational files, or executing recovery on
its findings.

Every change to skill-craft's operational files (`SKILL.md`,
`references/*.md`) dispatches one fresh-context subagent — one per
change-set, **before commit**. The subagent loads skill-craft,
reads the changed text freshly (working tree, staged diff, or
inline in the brief), and applies the five checks. This is
verification of the session's own edits — distinct from
reflexivity (SKILL.md, own conduct), where a proposed new rule goes
to the operator: here the artifact under review is the session's
own commit, so blocking recovery executes without a round-trip.
Fresh-context vetting is tier-insensitive insurance — it removes
self-blindness, not a capability gap — and stays regardless of the
consuming model.

## The five checks

1. **Rule application** — test the changed text against each rule
   of the canon (SKILL.md sections; the anti-patterns). A violation
   is a blocking finding.
2. **Format consistency** — does the change match adjacent entries'
   form?
3. **Overlap or conflict** — enumerate cross-referenced rules: the
   change's citations, grep-found citations of the change's home,
   and semantic siblings in the same section. Per reference,
   articulate the relationship (parallel / extending / overlapping
   / contradicting). The enumeration with per-reference tests is
   the artifact; a bare "no conflict found" is malformed.
4. **Coverage** — does the change catch what it targets?
5. **Fix substance** — does any Fix prescribe a concrete next
   action?

## Recovery

Findings rank blocking / notable / nit.

- **Blocking** — fix (or revert the change) before commit, no
  operator round-trip.
- **Notable / nit** — surface each finding to the operator with a
  recommendation (fix-shape proposed). The operator decides per
  finding: fix-now, accept-with-rationale, or
  defer-to-observations.

## Discipline-citation in dispositions

Every finding's disposition cites the discipline-test applied plus
the evidence that test requires — never a naked verdict, never an
echo of the reviewer's severity (the appeal-to-existing family,
`anti-patterns.md`). When the finding names a discipline, test
against it; when it is bare, identify the applicable discipline
from the candidate set (Edit-as-Pareto-improvement, Naked judgment,
Skip-rationalization, equivalent canon rules) and cite
which matched and which were ruled out. A
cosmetic-no-discipline-applies exemption lists the candidates
considered with per-member rule-outs. A proposed deviation from a
finding surfaces as its own `operator-decision-required` line — an
explicit flag, not an equal-weight option.

## Commit conventions

Accept-with-rationale adds an `Accepted-finding:` line in the
commit message **body**, citing the finding's file:line and the
operator's reason — commit-body-only, because the audit trail lives
permanently in git history. Defer-to-observations logs to the
OBSERVATIONS.md of the corpus the finding cites. Commit only after
every finding has a recorded disposition; reviewing before commit
keeps bad commits out of the record.
