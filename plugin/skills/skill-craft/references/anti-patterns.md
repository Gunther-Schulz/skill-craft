# Anti-Patterns

**Load when:** Reviewing a skill for common design mistakes.

**Reader model.** A skill file's only reader is the AI in mid-execution.
Every anti-pattern below is a failure mode where content ends up in a
skill file but does not serve that reader. The fix is to move the
content to a maintenance file (OBSERVATIONS.md, commit messages,
README.md, VISION.md) or delete it.

---

## Monolithic SKILL.md

Everything in one file. Works for trivial skills. Fails when the skill
grows because the AI loads the entire file at invocation, wasting context
on guidance that isn't needed yet.

**Fix:** Extract reference material to `references/` subdirectory. Keep
SKILL.md focused on trigger conditions, what to load, and the core method.

## Procedure with project-specific examples

The procedure contains real filenames, service names, or code patterns
from a specific project. It only makes sense in that project. Porting it
to another codebase requires rewriting the examples.

**Fix:** Procedure is abstract. Observations contain the real incidents.

## Checklist as ceiling

The procedure has a checklist of N items. The AI performs all N,
reports findings, and stops — neither tracing each finding's
implications nor looking past the N categories. Issues outside the
checklist, and adjacent issues a finding predicts, go unfound.

**Fix:** The checklist seeds the investigation, it does not bound it.
Trace each finding's implications — follow each as a lead until it
stops producing new findings — and look beyond the N categories.

## Skill that never evolves

The skill was written once and never updated. Failures during use are
worked around rather than incorporated as observations or procedure
changes.

**Fix:** Establish the improvement cycle (layer 4). Every failure is a
candidate observation. Every observation is a candidate procedure change.

## Procedure drift through incremental patches

The opposite of "never evolves." Each observation adds a paragraph to the
procedure. Individually correct. In aggregate, the procedure bloats beyond
what the AI can hold in attention and drifts from the founding vision. The
document becomes a compliance checklist instead of the lean set of
principles it started as.

**Symptoms:**
- Procedure exceeds 200 lines
- Specialized guidance (data flow tracing, verification states) sits
  inline alongside core principles
- Tone becomes adversarial ("this is not optional," "CANNOT proceed,"
  "do not generate") — the procedure is arguing with the AI's tendencies
  instead of stating principles
- Multiple paragraphs say the same thing with different emphasis
- A VISION.md exists but reading the procedure doesn't feel like the vision

**Fix:** Periodically re-derive the procedure from the vision. For each
checkpoint, ask: can I state this in 3-5 sentences that a sculptor would
recognize? If not, the checkpoint has accumulated implementation detail
that belongs in `references/`. Move specialized guidance to reference
files. The procedure should fit on a screen.

## Naked judgment call

The procedure asks the AI to decide something without providing
mechanical criteria or structural enforcement. Reads reasonable —
"assess severity", "identify critical items", "classify as trivial",
"determine if qualifies" — but none of those verbs have a computation
behind them. The AI answers confidently and consistently-wrong because
there is nothing to correct against.

**Symptoms:**
- Evaluative verbs (assess, classify, identify, determine, qualify)
  appear in the procedure without a defined computation
- The decision affects control flow: which path taken, whether to
  skip, which category a finding goes in
- The same input produces different classifications in different runs
- Errors in the decision are caught downstream (during review or after
  shipping), not at the decision point
- Procedure uses phrases like "use judgment", "as appropriate",
  "when warranted" — these are proxies for a specific rule the author
  didn't write down

**Fix:** Name the decision explicitly, then apply one of the three
mitigations — mechanical criteria, structural enforcement, or a safety
net — per "Judgment calls as design risk" (PROCEDURE.md Layer 2).
Never leave the decision naked.

## Information loss at skill boundaries

Orchestrated workflows (A invokes B, B invokes C) lose data at every
handoff. Skill A's output is compressed into skill B's prompt, dropping
fields that skill C needs later. Or a retry invocation includes only the
failure details, not the original design context. Or counters tracked in
conversation are lost when context compacts.

**Symptoms:**
- Downstream skill re-discovers what upstream already found
- Retry produces different (often worse) results than original
- Session recovery loses progress or quality signals
- Reviewer re-verifies what executor already proved

**Fix:** For each handoff point, audit: does the receiver get everything
it needs? Is the data passed explicitly (in prompt or on disk), or does
it rely on conversation context that can be compacted? See "Information
flow in orchestrated workflows" in the main procedure.
