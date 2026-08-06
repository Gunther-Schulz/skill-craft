# Writing skill procedures by type

**Load when:** designing a new skill — to determine the procedure
shape for the skill's type, and for the full Path 2 techniques.

---

Not all skills are the same type. The shape of the method text
depends on what kind of skill it is.

## Skill types

**Rule-based skills** — checklists, audits, validation procedures.
The method is a set of rules preventing specific failures.

**Workflow skills** — orchestrate a multi-phase process. The method
is a flow with phases, gates, and routing.

**Domain knowledge skills** — encode expertise for a specific
domain: "when encountering X, do Y — that is how this domain
works."

**Judgment skills** — assess rather than execute: audits,
reflective reviews, design critiques. The method defines what to
examine and what constitutes a finding; the analysis requires
understanding, not step-following.

**Tooling skills** — thin wrappers around a workflow or tool. The
method is a sequence of steps.

An audit fits whichever type matches its checks: mechanical checks
make it rule-based; checks requiring assessment make it a judgment
skill.

## Writing rule-based procedures

Two paths, by whether real incidents exist (SKILL.md, Two paths for
every rule).

**Path 1: phenomenon-driven (incidents exist).** Document the
observation (what happened, abstracted); derive the rule from it
(what would prevent it); the observation grounds the rule — its
reason for existing stays traceable.

**Path 2: blank-slate (no incidents yet).** The rules are
hypotheses — mark them as such and validate by use. Each technique
below finds or holds the right abstraction level, the common root
of the failure modes it addresses:

- **Phenomenon identification.** Before drafting a rule, describe
  what actually goes wrong (or could) and why. The rule addresses
  the root cause, not one scenario.
- **Proxy detection.** For each element of a rule: does it state
  the actual condition or an approximation? "Be careful" proxies a
  specific action — replace the proxy with the precise condition.
- **Bidirectional trigger check.** Every rule fails two ways: too
  narrow (misses cases the principle covers) and too fuzzy (fires
  where it shouldn't). List at least two cases where the rule WOULD
  fire and two where it WOULDN'T; per case, decide whether the
  outcome matches the intent. Misses → too narrow; spurious fires →
  too fuzzy.
- **Widen by principle, not enumeration.** A trigger too narrow
  abstracts upward to the principle that catches unenumerated
  variants — a rule growing by "…or X, or Y, or Z" is brittle; the
  next shape not in the list slips through. Applies equally when a
  Path 1 incident exposes a gap in an existing rule: sharpen the
  principle, don't lengthen the list.

## Writing workflow procedures

Define phases, gates between them, and what triggers transitions:
what must be true to advance, what signals completion, what happens
on interrupt. Workflow procedures benefit from explicit
choice-surfacing at phase boundaries more than any other type — the
surfaced choice IS the flow control.

**Decision logic within workflow phases.** A workflow phase whose
output contains decision logic (classification, matching,
filtering, scoring, routing) is minting an internal rule — validate
it with the Path 2 techniques above, not just as a workflow step.
This is the naked-judgment mitigation (SKILL.md, Enforcement) at
finer grain.

## Writing judgment procedures

Judgment skills assess. The method defines what to examine and what
constitutes a finding; it cannot reduce to a checklist that is
correct when followed mechanically.

**Principles with evidence requirements, not blocking checkpoints.**
State the principle ("two passes minimum") and the evidence
requirement ("each finding carries location, impact,
classification") — not a gate ("- [ ] Two passes completed? NO →
CANNOT proceed"). A gate can be satisfied mechanically without
understanding; an evidence requirement forces the output to
demonstrate the principle was applied. The test: can the check be
satisfied mechanically without understanding? If yes, it belongs in
a workflow skill.

**Layers, not steps.** Judgment procedures examine one system from
multiple angles (structural shape, boundary agreements, error
paths); layers do not gate each other — findings from any layer
inform the others.

**Deepening is mandatory.** Every finding predicts adjacent issues:
a swallowed error in one function predicts swallowed errors in its
siblings. Instruct: trace each finding's implications. Without
deepening the output is surface findings, not structural insight.

**The output demonstrates the analysis.** Per finding: location,
impact if unfixed, classification. The findings are the evidence
the judgment happened; "looks good" without findings is a protocol
violation.

## Writing domain knowledge procedures

Encode expertise as concrete rules with context — not "be aware of
CRS issues" but "BEFORE any geometry operation, verify source and
target CRS match; if they don't, reproject explicitly." Domain
procedures need the disclosure ladder most: core rules in the body,
detail in `references/`.

## Writing tooling procedures

Keep them minimal: steps, expected inputs, expected outputs.
Tooling skills rarely need journals — they work or they don't; when
the tool changes, update the steps.

**Skills that bundle scripts.** A shipped script is part of the
skill's reliability surface:

- **Solve, don't punt.** The script handles its own error
  conditions — recover, or exit with a precise actionable message —
  never failing into the consumer's lap with a bare error.
- **No unexplained constants.** Every magic value (timeout, retry
  count, threshold) carries the reason for its value at point of
  use.
- **Plan → validate → execute** for fragile or batch operations:
  emit a plan artifact, validate it with a script, then act — the
  un-fakeable artifact applied to scripts; the validated plan
  proves the operation was checked before it ran.
- **State execute-vs-read intent.** Say whether the consumer runs
  the script (most cases — cheaper, deterministic) or reads it as
  reference (when the logic itself is the guidance); ambiguous
  intent wastes a load or a run.
