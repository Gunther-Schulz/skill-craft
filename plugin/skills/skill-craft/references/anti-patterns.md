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
- **WHY-explanation prose padding the rule** — rationale text the AI
  can infer from anchored cross-references (`§X.Y`, `file.md`), or
  restating-with-different-emphasis filler. Skills target AI
  consumption; human-style explanation is bloat when the anchor
  carries the meaning.

**Fix:** Periodically re-derive the procedure from the vision. For each
checkpoint, ask: can I state this in 3-5 sentences that a sculptor would
recognize? If not, the checkpoint has accumulated implementation detail
that belongs in `references/`. Move specialized guidance to reference
files. The procedure should fit on a screen.

**AI-tightness check** (per-edit): a new clause whose word-count is
dominated by explanation rather than rule is malformed. Cross-references
substitute for explanation; the AI follows the anchor when context is
needed. Rule-words first, anchors second, explanation only when no
anchor exists.

**Positive-form-first for definitional rules** (per-edit): a rule
defining what a thing IS leads with the positive shape ("X is A + B");
negative form follows only as discriminator. **Classification test:**
when a parent rule (a discipline's lead, an enclosing definition)
already states the positive shape, this rule is a **discriminator** —
keep it negative; otherwise, lead with the positive shape. **Default
to discriminator when ambiguous** — under-stating is recoverable;
restating inflates. Standalone-all-negative AND discriminator-with-
positive-lead are both malformed.

**Form choice for non-definitional rules** (per-edit): positive-form-
first above scopes to definitional rules. Other rule classes pick
form by what makes the rule fire clearly against its target failure:
- **Mechanical rules** (backed by un-fakeable artifact): positive
  default — the artifact is observable; "produce X" is more
  checkable than "don't fake X."
- **Anti-patterns** (named failure shapes the AI defaults to):
  negative — the named shape IS the rule; pattern-match against
  the shape. This is why this file is negative-form throughout.
- **Judgment rules with multiple correct paths**: negative refusal
  of the wrong behavior, leaving room for legitimate variations.
  Positive form here over-constrains.

Form is secondary to the mechanical-vs-judgment axis (PROCEDURE.md
"Judgment calls as design risk"). Mechanical rules preferred
regardless of form; if a rule must be judgment-shaped, form follows
what surfaces the target failure most clearly.

**Edit-as-Pareto-improvement** (per-edit): a rule edit must show
either fewer words OR more coverage (ideally both). Pure addition
without coverage gain is the bloat path. Before commit, name what
the edit removed or consolidated; if nothing, the addition is
suspect.

## Rule elaboration creep

A load-bearing rule grows beyond principle + test + fix. Each
addition is locally justified but aggregate creates narrowing
bias and conflict risk. ("Procedure drift" at rule level;
"Checklist as ceiling" applied to rule text rather than
execution.)

**Symptoms:**
- Body exceeds principle + test + fix
- Examples enumerated within the rule
- Sub-shapes elaborate the same principle
- Motivational prose appears alongside the test

**Fix:** Compress to principle + test + fix. Drop enumeration,
sub-categorization, motivational framing.

## Additive reflex

When working on a rule corpus, AI tendency is to propose additions
even when restraint or subtraction is correct. The failure surfaces
at the AI's proposal moment; cumulative effect is bloat (parallels
"Procedure drift" at corpus accretion).

**Symptoms:**
- Proposed responses to bloat are themselves rule-additions
- Multi-option menus when "do nothing" is the right option
- Refactoring that grows total content
- Rule-additions to police rule-additions

**Fix:** apply "Edit-as-Pareto-improvement" (above). Default
disposition on ambiguous rule-need: do nothing.

## Naked judgment in rule statements

A load-bearing rule's test rests on the AI's own judgment rather
than on an observable property. The AI pattern-completes the
missing criterion and answers consistently-wrong; the error
surfaces downstream.

**Symptoms:**
- The rule has no explicit criterion for what constitutes correct
  application
- The decision affects control flow (path taken, skip taken,
  category assigned)
- The rule directs the AI to apply "judgment" without naming the
  observable criterion

**Fix:** Apply one of three mitigations — mechanical criteria,
structural enforcement, or safety net — per "Judgment calls as
design risk" (PROCEDURE.md Layer 2). Never leave the test naked.

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

A skill points at load-bearing reference files with prose
("for X, see Y") instead of an imperative load gate. The AI reads
it as informational, skips the load, substitutes pattern-memory;
output looks spec-compliant but diverges from current references
silently.

**Symptoms:**
- Reference named in prose without an observable load step
- No loaded-references manifest at skill activation
- Skipping the reference would produce wrong output yet loading
  is not gated

**Fix:** Convert load-bearing reference loads to a blocking gate
at skill activation requiring a loaded-references manifest as
evidence. Discriminator: load-bearing = skipping produces wrong
output; genuinely-optional = skill works correctly when not loaded
(genuinely-optional may remain on-demand per Layer 3). See
"Blocking logic" (PROCEDURE.md Layer 2).

## Unverified render from source

A skill rendered from a source spec by paraphrase silently flattens
structural rules to prose ("must" → "should") and drops load-bearing
clauses. The renderer is blind to its own flattening — re-reading
the render reads as faithful.

**Symptoms:**
- Skill text was written by paraphrasing a source spec
- No clause-level diff against the source by a separate context
- Enforcement language is softer than the source
- Load-bearing clauses in the source have no corresponding text in
  the skill

**Fix:** A fresh subagent (not the renderer) diffs clause-by-clause
against the source: every load-bearing clause appears in the
render; structural mechanisms render as structural, not flattened
to prose. See "Rendering from a source" (PROCEDURE.md Layer 2).
