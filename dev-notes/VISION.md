# Skill Craft — Vision

The philosophical foundation `PROCEDURE.md` renders into method.
Maintenance file: never loaded at skill-use time. Its purpose is to be
the source every load-bearing checkpoint traces back to — so the
procedure can be re-derived from it and audited against it (the
"Procedure drift" Fix, `references/anti-patterns.md`).

## The problem

A skill is a rule-corpus whose only reader is an AI in mid-execution,
and that AI does not self-enforce. A prose instruction it could skip,
it eventually skips — silently, on the success path, where nothing
catches it. The whole problem of skill design is making a skill the
model *reliably follows*, across many invocations and across the AI
failure modes catalogued in `anti-patterns.md` — not writing a manual
that reads well.

## Thesis: enforcement rests on un-fakeable artifacts

A rule holds only when adherence produces an artifact that could not be
produced without doing the work the rule represents — an enumeration
that required searching, a gate whose evidence cites an external fact.
A bare claim ("checked all cases") is satisfiable whether or not the
work happened, so it enforces nothing. Evidence-bearing is a gradient:
strongest when it points at external, re-checkable truth; weakest when
it is only a claim about the run's own state. **Phase boundaries are
themselves enforcement points**: where one phase produces a commitment
another phase reads, the boundary needs a gate — silent revision
between phases is the same fakeability shape applied to handoffs.
Every technique in the procedure is an application of this one
principle. *This is the spine; everything below serves it.*

## Enforcement is proportional, not maximal

Strength is matched to the work, not applied everywhere. A
deterministic/workflow step — a sequence or gate that must hold — takes
structural enforcement (blocking logic, un-fakeable evidence). A
judgment step takes evidence-backed principles, because a gate on
judgment work over-constrains it and the validator register leaks into
skills that should reason. The common authoring error is the wrong
register, not the wrong rule. Proportionality also binds the framework
to itself: a skill must resist its own bloat — refine by cut, edit for
Pareto improvement — as hard as it closes gaps.

## A skill is an actor, not a reporter

A skill acts on findings actionable within its scope in the same
invocation, rather than handing them back for the operator to track.
Questions surfaced to the operator carry the skill's recommendation —
never a naked menu. Reporting-without-acting is its own discipline
failure: it converts the skill from an enforcement mechanism into a
note-taker the operator must re-process.

## Skills are living rule-corpora

A skill is written once but corrected forever. Use reveals a gap; the
gap becomes an observation; the observation, when it names a pattern,
becomes a procedure change — grounded in the incident, not guessed. The
corpus must carry the machinery of its own correction (evolution) and
the awareness to notice when its own guidance is what needs updating
(reflexivity). Change without this machinery rots; machinery without
restraint bloats.

## Content depreciates against a moving reader

The AI a skill steers is not fixed: consumers improve, and content
written for one tier ages against the next. What a skill *enforces or
structures* is durable — enforcement rests on fakeability, and
fakeability does not shrink with capability. What a skill *teaches or
compensates* is a loan against a current weakness: it depreciates as
the weakness closes, and holding it past that point costs adherence
(a stronger reader steered too tightly performs below its default).
So every piece of operational content carries an implied lifetime and
a review trigger — retirement when its weakness closes, re-rendering
into the judgment register when its step stops being compliance work,
staleness-checking when it binds an environment. A corpus that never
depreciates its content is betting its reader never improves; the bet
has lost every time so far.

## What follows: the five layers

The method organizes as five layers, in rising order of where skills
actually live or die:

1. **Plugin structure** — mechanical plumbing. Get it right once.
2. **Protocol conventions** — how to write text the AI follows: the
   un-fakeable artifact, gates vs principles.
3. **Skill architecture** — organizing knowledge across files so the
   skill stays followable as it grows.
4. **Skill evolution** — the correction machinery.
5. **Skill reflexivity** — noticing that the guidance itself must change.

Most authors get layer 1 right and stop. Layers 3–5 decide whether a
skill survives contact with time.

## What skill-craft is not

Not mechanics — frontmatter format, hooks syntax, packaging, directory
scaffolding. Those are the platform's contract, delegated to the
official `plugin-dev` plugin. skill-craft is the *design methodology*:
what to build, how to structure it, and how to make the AI follow it.
It governs domain-general skill design and must reach across unrelated
domains — which is why its own procedure runs longer than an ordinary
skill's, and why the test on it is per-checkpoint compression, never a
line count.

## The derivation contract

`PROCEDURE.md` is this vision rendered into operational checkpoints.
Every load-bearing checkpoint should trace to a principle here; one
that doesn't is either accreted detail to move to `references/`, or a
sign the vision is incomplete. Re-derive the procedure from this file
periodically; where a section no longer reads like the vision, the
section drifted — not the vision.
