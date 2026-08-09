# Anti-patterns

**Load when:** reviewing a skill for known failure shapes, or
drafting content that risks one.

**Reader model.** A skill file's only reader is the AI in
mid-execution. The entries below are skill-design failure shapes —
content that doesn't serve that reader, rule forms that don't
behave as written, or structures that break loading or execution.
Entries stay in negative form by design: the named shape IS the
rule (SKILL.md, The two registers — positive-rendering exemption).

---

## Overweight description

The description restates the body — method summaries, identity
prose, synonym chains — and every word is paid on every turn of
every session (observed fleet-wide: a ~180-word triage description;
a forcing-point summary in the description of a skill invoked only
by name, buying zero triggering).

**Symptoms:** description longer than its trigger branches justify;
identity the body carries restated; synonyms renaming one branch;
method summary in a name-invoked skill's description.

**Fix:** front-load the leading word; one trigger per genuinely
distinct branch; cut identity the body carries (SKILL.md, Context
pointers). Before delisting a prose-invoked skill entirely, weigh
the measured invocation cost (SKILL.md, Invocation choice).

## Monolithic SKILL.md

Everything inline regardless of branch. Works for trivial skills;
fails as the skill grows — attention thins across material only
some branches reach.

**Fix:** the disclosure ladder (SKILL.md, The information
hierarchy): inline what every branch needs, push single-branch
reference behind pointers.

## Procedure with project-specific examples

The method contains concrete names, examples, or patterns from one
project; porting it means rewriting them.

**Fix:** the method stays abstract at the skill's declared scope;
real incidents live in the journal.

## Checklist as ceiling

The skill has a checklist of N items; the consumer performs all N,
reports, and stops — neither tracing findings' implications nor
looking past the N categories.

**Fix:** the checklist seeds the investigation and does not bound
it. Trace each finding as a lead until it stops producing new
findings; look beyond the categories.

## Skill that never evolves

Failures during use are worked around rather than recorded and
incorporated.

**Fix:** the evolution cycle (SKILL.md, Lifecycle): every failure
is a candidate observation, every pattern-naming observation a
candidate change.

## Procedure drift through incremental patches

The opposite failure: each observation adds a paragraph,
individually correct; in aggregate the method bloats past what
attention holds and the register turns adversarial.

**Symptoms:** management scaffolding (release ops, the machinery of
running a check) inline beside the core method; adversarial tone
("this is not optional") — text arguing with the reader's
tendencies instead of stating principles or building mechanisms;
multiple paragraphs restating one point with different emphasis;
WHY-prose padding a rule an anchor already carries.

**Fix:** re-run the no-op test clause by clause against the
declared consumer; move management scaffolding down the disclosure
ladder; re-render adversarial gates into mechanisms (if they must
hold) or the evidence register (if they steer judgment). The
per-edit guard is Edit-as-Pareto-improvement (Additive reflex,
below).

## Rule elaboration creep

A load-bearing rule grows beyond principle + test + fix; each
addition locally justified, the aggregate narrowing and
conflict-prone — Procedure drift at rule grain.

**Symptoms:** body exceeds principle + test + fix; examples
enumerated inside the rule; sub-shapes elaborating the same
principle; motivational prose beside the test.

**Fix:** compress to principle + test + fix; drop enumeration,
sub-categorization, motivation.

## Additive reflex

On a rule corpus, the default proposal is an addition even where
restraint or subtraction is correct; the cumulative effect is
bloat.

**Symptoms:** responses to bloat that are themselves rule-additions;
multi-option menus where "do nothing" is right; refactors that grow
total content; rules policing rule-additions.

**Fix — Edit-as-Pareto-improvement:** a rule edit shows fewer words
OR more coverage, ideally both. Before commit, name what the edit
removed or consolidated; if nothing, the addition is suspect.
Default disposition on ambiguous rule-need: do nothing.

## Skip-rationalization

About to apply a discipline (a review, a check, a gate, a
dispatch), the AI constructs a rationalization for skipping it —
"small change," "prior reviewer covers this," "redundant here."
The discipline gets skipped; the gap surfaces later, often via
operator catch.

**Symptoms:** doubt voiced in prose about whether a discipline
applies; discretion-shaped reasons cited; proceeding without the
discipline; the pattern recurring with fresh escape phrasings.

**Fix:** the rationalization-construction IS the signal — the doubt
is evidence the discipline applies. Apply first, evaluate after.
Mechanical inapplicability conditions (observable from artifact,
diff, or document state) are the only acceptable skip
(`enforcement.md`, N/A escapes).

**The appeal-to-existing family.** Variants sharing one shape: a
disposition justified by appeal to something existing without
independent verification against the applicable discipline.

- *Disposition-echo*: a reviewer's severity is echoed into the
  disposition ("reviewer said observation, so keep-as-is") without
  re-deriving. Test: does the disposition cite a discipline-test
  applied, or only the reviewer's rank?
- *Corpus-appeal*: an existing corpus pattern cited as defense
  ("§X already does Y") without testing the cited pattern against
  current discipline — weakness inherited circularly. Test: does
  the cited pattern itself pass? If not, it is no defense; surface
  the corpus-wide weakness as its own observation.
- *Jurisdiction-appeal*: a real, healthy rule cited whose scope
  governs a different act than the one being decided — drift
  reading as discipline. Test: read the cited rule's own text for
  the act it names; a mismatch is the finding. Name the act first,
  then apply the rule that governs THAT act.

## Naked judgment in rule statements

A load-bearing rule's test rests on the consumer's own judgment
rather than an observable property; the consumer pattern-completes
the missing criterion and answers consistently wrong.

**Symptoms:** no explicit criterion for correct application; the
decision affects control flow; the rule says "apply judgment"
without naming the observable; a common-word qualifier
("sufficient," "minimal," "reasonable") with no operational
definition constraining its reading.

**Fix:** the mitigation ladder (SKILL.md, Enforcement): mechanical
criteria, structural enforcement, or a documented fail-loud net —
never a naked test. For common-word qualifiers, inline an
operational definition or replace with a mechanical criterion.

## Information loss at skill boundaries

Orchestrated workflows (A invokes B, B invokes C) lose data at
every handoff: output compressed into the next prompt drops fields
a later consumer needs; a retry carries only the failure details;
conversation-held state dies at compaction.

**Symptoms:** downstream re-discovers what upstream found; retries
produce worse results than originals; session recovery loses
progress; a reviewer re-verifies what an executor proved.

**Fix:** audit each handoff — receiver gets everything it needs,
explicitly, format-matched, compaction-safe (`enforcement.md`,
Information flow).

## Soft load pointers

A skill points at load-bearing reference files with prose ("for X,
see Y") for a consumer that reads pointers as informational — the
load is skipped, pattern memory substitutes, and output diverges
from the current reference silently.

**Symptoms:** a load-bearing reference named in prose for a
below-trust-tier consumer; no load evidence at activation; skipping
the reference would produce wrong output, yet nothing gates it.

**Fix:** tier-conditional — for a below-trust-tier consumer or a
must-hold procedure, the load gate (`enforcement.md`); for a
top-tier consumer, a sharp pointer at point of use, gated only on
fire evidence. Discriminator: load-bearing = skipping produces
wrong output; genuinely-optional stays on demand at every tier.

## Unverified render from source

A skill rendered from a source spec by paraphrase silently flattens
structural rules to prose ("must" → "should") and drops
load-bearing clauses; the renderer is blind to its own flattening,
so re-reading the render reads as faithful.

**Symptoms:** skill text written by paraphrasing a source; no
clause-level diff by a separate context; enforcement language
softer than the source; source clauses with no corresponding text.

**Fix:** a fresh context (not the renderer) diffs clause-by-clause
against the source: every load-bearing clause present, structural
mechanisms rendered structural (SKILL.md, Rendering from a source).

## Edit-without-spec-origin

A rendered artifact is edited directly, without the source clause
the edit derives from — the artifact gains content the source
doesn't carry, a re-render would lose it, and audit-against-source
has nothing to compare. Distinct from Unverified render: that
questions render fidelity; this has no source clause at all.

**Symptoms:** render edited with no surfaced source clause;
re-render would lose the edit; drift surfaces retroactively at
operator catch.

**Fix:** route the edit through the source first — add the content
to the source, then re-render; every render edit cites the source
clause it derives from.
