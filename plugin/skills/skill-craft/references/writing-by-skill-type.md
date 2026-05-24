# Writing skill procedures by type

**Load when:** Designing a new skill — to determine the appropriate
procedure shape for the skill's type. Not needed for reviewing or
iterating existing skills.

---

Not all skills are the same type. The approach to writing
PROCEDURE.md depends on what kind of skill it is.

## Skill types

**Rule-based skills** — checklists, audits, validation procedures.
The procedure is a set of rules that prevent specific failures.

**Workflow skills** — orchestrate a multi-phase process. The
procedure is a flow with phases, gates, and routing.

**Domain knowledge skills** — encode expertise for a specific
domain. The procedure is "when encountering X, do Y because that's
how this domain works."

**Judgment skills** — require assessment, not execution.
Architecture audits, reflective reviews, design critiques. The
procedure defines what to examine and what constitutes a finding,
but the analysis requires understanding, not step-following.

**Tooling skills** — thin wrappers around a specific workflow or
tool. The procedure is a sequence of steps.

An audit fits whichever type matches its checks: mechanical checks
that need no understanding make it rule-based; checks that require
assessment make it a judgment skill.

## Writing rule-based procedures

Two paths, depending on whether real incidents exist.

**Path 1: Phenomenon-driven (you have incidents).** A failure
happened. The observation exists or is obvious.

1. Document the observation (what happened, abstracted)
2. Derive the rule from the observation (what would prevent it)
3. The observation grounds the rule — the reason for its existence
   is traceable

This is how most effective rule-based skills are built. The
observation comes first, the rule follows.

**Path 2: Blank-slate (no incidents yet).** You're writing rules
for a new capability. No failures to learn from. Each technique
below is a way to find or hold the right abstraction level — broad
enough to apply across variants, specific enough to discriminate.
Wrong abstraction is the common root of every failure mode these
techniques address.

- **Phenomenon identification.** Before drafting any rule, describe
  what actually goes wrong (or could go wrong) and why. A rule must
  address the root cause, not just one scenario.

- **Proxy detection.** For each element of a rule, ask: does this
  represent the actual condition, or an approximation? "Be careful"
  is a proxy for a specific action. Replace proxies with the
  precise condition.

- **Bidirectional trigger check.** Every rule has two failure
  modes: too narrow (misses cases the principle should catch) and
  too fuzzy (covers cases it shouldn't, or fails to discriminate).
  Refining toward one risks the other. List at least two cases
  where the rule WOULD fire and at least two where it WOULDN'T.
  For each, decide whether the firing/non-firing matches the
  intended principle. Misses → too narrow; spurious fires → too
  fuzzy.

- **Widen by principle, not enumeration.** When a trigger is too
  narrow, abstract upward to the underlying principle that catches
  all variants — including ones not enumerated — and restate the
  rule at that level. A rule that grows by appending "...or X, or
  Y, or Z" is brittle: the next failure shape not in the list
  slips through. The fix is upward (abstract to the principle),
  not outward (list more cases). Applies equally when refining an
  existing rule based on a new incident: a Path 1 observation that
  exposes a gap should produce a sharper principle, not a longer
  list.

Rules from Path 2 are hypotheses. Validate by use, refine through
Path 1.

## Writing workflow procedures

Define phases, gates between phases, and what triggers transitions.
The key decisions are: what must be true to advance? What signals
completion? What happens when the user interrupts?

Workflow procedures benefit from menus (PROCEDURE.md Layer 2) more
than any other type. The menu IS the flow control — it shows the
user where they are and what they can do next.

**Decision logic within workflow phases.** When a workflow phase
produces design decisions that contain decision logic
(classification, matching, filtering, scoring, routing), apply
Path 2 techniques to that logic: phenomenon identification, proxy
detection, and non-firing case enumeration. A workflow skill's
design phase proposing a heuristic is creating an internal rule —
validate it as one, not just as a workflow step. This is a
specific case of the Layer 2 principle "Judgment calls as design
risk" — classification inside a workflow phase is that same
decision at finer grain.

## Writing judgment procedures

Judgment skills assess rather than execute. The procedure defines
what to examine and what constitutes a finding, but cannot be
reduced to a checklist that produces correct results when followed
mechanically.

**Principles with evidence requirements, not blocking checkpoints.**
A judgment skill states: "two passes minimum" (principle) and
"each finding must have: code location, impact, classification"
(evidence requirement). Not: "- [ ] Two passes completed? NO →
CANNOT proceed" (blocking checkpoint). The distinction matters: a
blocking checkpoint can be satisfied mechanically without
understanding. A principle with evidence requirements forces the
output to demonstrate the principle was applied.

The test: "can this check be satisfied mechanically without
understanding?" If yes, it belongs in a workflow skill. If no, it
belongs in a judgment skill.

**Layers, not steps.** Judgment procedures examine the same system
from multiple angles (e.g., structural shape, boundary agreements,
error paths). Each layer produces different findings. Unlike
workflow phases, layers don't gate each other — findings from any
layer can inform analysis in other layers.

**Deepening is mandatory.** Every finding predicts adjacent
issues. A judgment procedure must instruct: trace each finding's
implications. A swallowed error in one function predicts swallowed
errors in similar functions. A missing abstraction in one area
predicts missing abstractions in adjacent areas. Without
deepening, the skill produces a checklist of surface findings
instead of structural insight.

**The output demonstrates the analysis.** For each finding:
specific location, impact if unfixed, classification (severity).
The findings themselves are the evidence that the judgment was
applied. A judgment skill that says "looks good" without findings
is a protocol violation.

## Writing domain knowledge procedures

Encode the expertise as concrete rules with context. Not "be aware
of CRS issues" but "BEFORE any geometry operation, verify source
and target CRS match. If they don't, reproject explicitly."

Domain procedures are the most likely to need progressive
disclosure — the full expertise is too large to load at once. Core
rules in PROCEDURE.md, detailed reference material in
`references/`.

## Writing tooling procedures

Keep them minimal. State the steps, the expected inputs, the
expected outputs. Tooling skills rarely need observations or
evolution — they either work or they don't. If the tool changes,
update the steps.
