# Enforcement toolbox

**Load when:** the skill under design declares a below-trust-tier
consumer; or contains a sequence that must hold regardless of
judgment (the freedom coupling); or spans phases, dispatches, or
handoffs whose state another party reads.

One principle instruments every entry (SKILL.md, Enforcement): the
check's evidence is an artifact that cannot be produced without
doing the work the check represents. On a top-tier consumer's
judgment work these instruments over-constrain — the register
error; on a must-hold sequence they are correct at every tier.

## Blocking logic

Binary checks with un-fakeable evidence:

```
- [ ] [Check]?
  - NO → CANNOT proceed. [Alternative].
  - YES → Evidence: [HOW verified]
```

For workflow sequence that must hold. The evidence slot states how,
not that — "checked" is a claim; the enumeration of what was
checked, with results, is the artifact.

## The load gate

A below-trust-tier consumer reads a prose pointer ("for X, see Y")
as informational, skips the load, and substitutes pattern memory —
output looks compliant and diverges from the current reference
silently (Soft load pointers, `anti-patterns.md`). Where reference
files are load-bearing for correct execution, gate their loading
once, at activation:

```
- [ ] All load-bearing references loaded this session?
  - NO → CANNOT proceed. Load each now.
  - YES → Evidence: [files + sections read]
```

Genuinely-optional references stay on demand (the disclosure
ladder). For a top-tier consumer, a sharp pointer at point of use
replaces the gate; the gate re-enters only on fire evidence — a
recorded incident of the pointer being skipped.

## Forcing functions and dispatch order

FIRST / BEFORE / THEN express order; they do not enforce it. The
hazard is dispatch-specific: where ordered steps are independently
dispatchable (separate subagents, parallel tool calls, async jobs),
prose order is silently violable — success-path artifacts are
identical whether sequenced or parallel, so nothing catches the
reorder. Steps a single context runs in line are exempt. When a
dispatchable step B conditionally depends on step A's result,
encode the dependency: B cannot be constructed without A's result
as its input, and B's artifact cites that result — the violation
becomes unconstructable, or readable off the artifact.

## Observable checkpoints

Verify actions taken, not internal states. "Considered the
alternatives" is unfalsifiable; the enumeration of alternatives
with the reason each was rejected is the artifact.

## N/A escapes

A skip condition ("N/A if X") is itself mechanically verifiable
from observable state — the diff, the document, the manifest. A
judgment-shaped escape ("if small enough," "if prior coverage
applies") is a fakeable claim wearing a scope note; it surfaces as
the Skip-rationalization anti-pattern (`anti-patterns.md`).

## Commitment consistency across phase boundaries

Where one phase produces output another phase reads as a
commitment — a recommendation, a decision, approved text, a locked
design — gate each boundary where the commitment could be silently
revised. Two valid paths through: faithful execution of the
commitment, or explicit surface of the change ("Switching from X to
Y because Z — confirm?") with a response required before
proceeding. Silent revision between phases is the fakeability
failure applied to handoffs, whichever artifact carries the
commitment.

## Information flow in orchestrated workflows

At every handoff between skills or agents, data is lost unless
verified. Per handoff point: the receiver gets everything it needs;
data passes inline or by explicit path; formats match (schema and
field names); prompt compression preserves what downstream
consumers read; retries re-provide the original context, not just
the failure details; state that must survive compaction goes to
disk.
