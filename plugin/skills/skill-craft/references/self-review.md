# Self-review (Layer 4 mandate machinery)

**Load when:** Dispatching the mandated self-review subagent against
a proposed change to skill-craft canonical files, or executing
recovery on its findings before commit.

This is **Mechanism 2** per `PROCEDURE.md` Layer 4 "Two reflexivity
mechanisms" — that section owns the Mechanism-1-vs-Mechanism-2
definition. Distinct from `review-checklist.md` (see its **Scope**
section for the reciprocal framing): review-checklist is the 13-item
user-facing review applied to any skill; self-review is the
finer-grained, fresh-context gate for every change to skill-craft's
own canonical files.

## The mandate

Every change to skill-craft's canonical files (`PROCEDURE.md`,
`references/*.md`, `SKILL.md`) triggers one self-review — one subagent
for the whole change — **before commit**. The authoring AI dispatches
a fresh-context subagent against the proposed changes (working tree,
staged diff, or inline-described in brief). The subagent loads
skill-craft, reads the changed text freshly, and applies the five
checks below.

## The five checks

1. **Universal rule application** — for each canonical rule in
   skill-craft (Layer 2 principles, Layer 4 disciplines,
   anti-patterns), test the changed text against it. A violation is a
   blocking finding.
2. **Format consistency** — does the change match adjacent entries'
   format?
3. **Overlap or conflict** — enumerate cross-referenced rules (the
   change's citations + grep-found cites of the change's home +
   semantic siblings in the same Layer); for each, test whether
   consequences contradict the cited rule and articulate the
   relationship (parallel / extending / overlapping / contradicting).
   The enumeration + per-reference test is the un-fakeable artifact;
   bare "no conflict found" is malformed.
4. **Coverage** — does the change catch what it targets?
5. **Substance of any Fix prescription** — does it specify a concrete
   next action?

## Recovery path

Findings ranked blocking / notable / nit.

1. **Blocking** — AI fixes (or reverts the change) without operator
   round-trip.
2. **Notable / nit** — AI surfaces each finding to the operator with a
   recommendation (fix-shape proposed). Operator decides per finding:
   fix-now, accept-with-rationale, or defer-to-observations. AI does
   not self-classify or auto-fix.

## Discipline-citation in recommendations

Every reviewer finding's disposition cites a discipline-test applied
+ the evidence the test requires — not naked verdict, not echo of the
subagent's severity (see `anti-patterns.md` Skip-rationalization,
disposition-echo and corpus-appeal variants). The discipline-test
source (closed set):

- **(a)** the Concern-named discipline when the finding cites one —
  from the candidate set: Edit-as-Pareto-improvement / Naked-judgment
  anti-pattern / Skip-rationalization anti-pattern / no-theater /
  equivalent framework practices.
- **(b)** when Concern is bare, the AI scans (a)'s candidate set and
  tests the matching member, citing which matched + which were ruled
  out.
- **(c)** `cosmetic-no-discipline-applies` exemption listing every
  member of (a)'s candidate set considered + the per-member rule-out
  reason.

Classifiable structural-enforcement candidate → ship-now (n=1).
Undefendable alternative per no-theater → cut. A proposed AI
deviation produces an additional `operator-decision-required` line
citing the alternative — the deviation surfaces explicitly, not as an
equal-weight option.

## Accept-with-rationale and defer-to-observations

For accept-with-rationale decisions, AI adds an `Accepted-finding:`
line in the commit message **body** citing the finding's file:line and
the operator's reason; commit-body-only because the audit trail must
live in git history permanently. For defer-to-observations, AI logs
to the relevant `OBSERVATIONS.md` (of the corpus the finding cites).
AI commits only after every finding has a recorded disposition.

## Why before commit, not after

Reviewing before commit keeps git history clean — bad commits never
enter the record.
