# Anti-Patterns

**Load when:** Reviewing a skill for common design mistakes.

**Reader model.** A skill file's only reader is the AI in mid-execution.
Anti-patterns below are skill-design failure modes — content that
doesn't serve that reader, rule shapes that don't behave as written,
or structures that break the AI's loading or execution flow. Fixes
vary by shape: relocate content to a maintenance file (OBSERVATIONS.md,
commit messages, README.md, VISION.md), reshape the rule (anchor to
observable criteria), or restructure the skill (split files, change
loading boundary).

---

## Monolithic SKILL.md

Everything in one file. Works for trivial skills. Fails when the skill
grows because the AI loads the entire file at invocation, wasting context
on guidance that isn't needed yet.

**Fix:** Extract reference material to `references/` subdirectory. Keep
SKILL.md focused on trigger conditions, what to load, and the core method.

## Procedure with project-specific examples

The procedure contains concrete names, examples, or patterns from a
specific project. It only makes sense in that project. Porting it to
another project requires rewriting the examples.

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

## Naked judgment in rule statements

A load-bearing rule asks the AI to do something, judge something,
or check something — but the test rests on the AI's own judgment
rather than on an observable property. The AI reads the rule,
pattern-completes the missing criterion from whatever the
conversational context suggests, and answers confidently and
consistently-wrong because there is nothing to correct against.
Errors are caught downstream (during review or after shipping),
not at the decision point.

Two failure shapes share this root — same problem, different parts
of speech:

**Shape 1: Evaluative verbs.** The rule uses an evaluative verb
without a defined computation. Reads reasonable — "assess
severity," "identify critical items," "classify as trivial,"
"determine if qualifies" — but none have a computation behind them.

**Shape 2: Judgment-coded nouns and adjectives.** The rule uses a
term whose meaning rests on the AI's own judgment. Three
sub-shapes (illustrative, not exhaustive — the test is the
principle below, not the example term):

- **Moralistic** — terms implying moral or normative judgment
  without anchored criteria. *Example shape:* "proper-X", "right-X",
  "appropriate-X."
- **Vague positive valence** — descriptors carrying approval
  without specifying the property approved. *Example shape:*
  "good-X", "clean-X", "natural-X", "elegant-X."
- **AI-judgment-coded** — terms whose meaning requires the AI to
  assess its own state or context. *Example shape:* "best by your
  judgment", "as appropriate", "when warranted", "use judgment."

**The test, not the term-match.** Any term or verb in a load-bearing
rule that requires AI judgment rather than observable
property-check falls under this anti-pattern, whether or not the
specific word matches an example above. The principle is *no
anchored criterion*; the examples illustrate but do not exhaust.

**Symptoms:**
- A verb, term, or phrase in a load-bearing rule has no explicit
  criterion for what makes something instance-of-X
- The decision affects control flow: which path taken, whether to
  skip, which category a finding goes in
- The same input produces different classifications in different
  runs
- Errors in the decision are caught downstream (during review or
  after shipping), not at the decision point
- The rule uses phrases like "use judgment", "as appropriate",
  "when warranted" — proxies for a specific rule the author didn't
  write down
- Reasonable readers could interpret the term or verb differently
- The term encodes approval/disapproval without grounding
- Replacement candidates exist that describe properties or
  processes observably

**Fix:** Name the test explicitly, then apply one of the three
mitigations — mechanical criteria, structural enforcement, or a
safety net — per "Judgment calls as design risk" (PROCEDURE.md
Layer 2). Where a property is meant (e.g., thorough,
scope-bounded), name the property. Where a process is meant
(e.g., verified, search-established), name the process. Where a
comparison is meant (e.g., lowest-cost), name what's being
compared and against what. Never leave the test naked.

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

## Soft load pointers

A skill lists reference files as dependencies and points at them
with prose ("for full checklists, load X", "for detailed rules,
see Y"). The AI reads the prose pointer as informational ("there is
a reference doc") rather than imperative ("execute a Read now"),
proceeds without loading, and substitutes pattern-memory of past
sessions for the actual file content. Output looks spec-compliant
because the AI reproduces the expected shape from memory; it
diverges from the current reference files silently.

**Symptoms:**
- Reference file is named in prose ("see X for details", "consult
  Y", "load Z if needed") without an observable load step
- No loaded-references manifest at skill activation enumerating
  what was actually read
- Skill output matches the reference's shape but is not traceable
  to specific reference content
- Re-runs of the same skill produce inconsistent output as
  pattern-memory drifts
- Reference files are load-bearing (skipping them produces wrong
  output) but loading is not gated

**Fix:** Convert load-bearing reference loads to a blocking gate
at skill activation — one consolidated step requiring a
loaded-references manifest (files + sections read) as evidence
before the skill body executes. Discriminator: a reference is
**load-bearing** if skipping it produces wrong output;
**genuinely-optional** if the skill works correctly when it is not
loaded. Load-bearing references must be
gated; genuinely-optional ones may remain on-demand (progressive
disclosure, Layer 3). See "Blocking logic" (PROCEDURE.md Layer 2)
— reference loading is structurally the same shape as a workflow
gate.

## Unverified render from source

A skill is rendered from a source spec (framework, standard, parent
methodology) by paraphrase. Paraphrase silently flattens — "must"
becomes "should," structural rules become soft principles,
load-bearing clauses drop. The renderer's own review misses this
because the drafting context is blind to its own flattening: it
reads its output as faithful to what it intended, not as a diff
against the source. The rendered skill ships with structural
enforcement degraded to advisory prose, and the first real run
exposes the gap.

**Symptoms:**
- Skill text was written by paraphrasing a source spec or parent
  document
- No clause-level diff against the source was performed by a
  separate context
- The skill's enforcement language is softer than the source
  ("must" → "should", "CANNOT proceed" → "consider whether")
- Structural mechanisms in the source (gates, mandates, blocking
  logic) render as prose principles in the skill
- Load-bearing clauses in the source have no corresponding text
  in the skill
- Verification artifact (if any) references re-reading the render,
  not a clause-by-clause comparison against the source

**Fix:** Render verification is a separate-context job. The
context that produced the render never verifies it — paraphrase
blindness means the renderer reads its own output as faithful. A
fresh subagent (or another party) diffs clause-by-clause: every
load-bearing clause of the source must appear in the render;
structural mechanisms must render as structural, not flattened to
prose. See "Rendering from a source" (PROCEDURE.md Layer 2).
