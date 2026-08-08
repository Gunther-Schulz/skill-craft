---
name: skill-craft
description: Design, review, or evaluate Claude Code skills and plugins. Use when creating a skill, reviewing or improving one, writing or repairing a description that under- or over-triggers, deciding what a skill enforces versus teaches and which tier consumes it, packaging or releasing a plugin, or when a failure during a skill's use suggests the skill itself needs the fix.
license: MIT
---

# Skill-craft

A skill is a document whose only reader is an AI in mid-execution.
Two questions govern every line of one: does it hold — does the
reader behave differently, reliably, across runs — and what does it
cost — context and attention spent whether or not the line fires.
Design for both at once; every section below is a lever on one or
the other.

**Birth declaration.** Skill-craft is a judgment skill; its intended
consumer is a top-tier session model, and its own prescription
density is calibrated to that. Its teaching content is rich; gates
on itself are near-zero at birth and fire-earned (Skill-craft's own
conduct, fire-born machinery). Mechanical insurance is
tier-insensitive and stays mechanical: the eval runner
(`/eval-skill`), the release and
stale-pin hooks, and the pre-commit self-review dispatch
(`references/self-review.md`). Observations write to
`dev-notes/OBSERVATIONS.md` in the source repo
(github.com/Gunther-Schulz/skill-craft) — a write target during
use, never a load.

## The two parties

Every skill has a writer and a consumer, and the design follows the
consumer. Declare the consumer — the model or tier range that will
execute the skill — in the skill's opening, and let the declaration
set the enforcement density:

- A **top-tier consumer** takes evidence-register principles and
  brief teaching. Gates on its judgment work over-constrain it and
  cost adherence — a strong reader steered too tightly performs
  below its own default.
- A **below-trust-tier consumer** takes the structural instruments:
  blocking gates, load manifests, un-fakeable evidence
  (`references/enforcement.md`).
- The **freedom coupling stays primary at every tier**: a fragile
  or invariant sequence — one that must hold regardless of
  judgment — keeps exact steps and structural enforcement even for
  the top tier. Density calibration governs everything outside
  that class.

An undeclared consumer defaults the density decision to the
writer's habits; the observed failure shape is a corpus written
blocking-gates-everywhere for a reader trusted with judgment.
Re-review density whenever the declared consumer changes
(Lifecycle, the era re-grade).

The economics below apply at every tier — what a skill costs does
not depend on who consumes it.

## What a skill costs

**The two loads.** Every document and pointer spends one of two
budgets. *Context load*: always-loaded material — a description, an
instruction-file line — paid every turn whether or not it fires.
*Cognitive load*: the human as index — knowing the document exists
and when to reach for it. Cognitive load is not minimized; it is
the price of human agency — spend it where human judgment matters,
remove it where it does not.

**Context pointers.** A pointer is in-context text naming
out-of-context material and encoding the condition for reaching
it — a skill description, a reference-file mention in a body. The
pointer's wording, not its target, decides whether the material is
reached: a must-have target behind a weak pointer is a variance
bug. Sharpen the wording first; inline the material only if
sharpening fails. Pointer form: front-load the word that does the
triggering; one trigger per genuinely distinct branch — synonyms
renaming one branch are one branch written twice; cut identity the
body already carries. An always-loaded pointer earns harder pruning
than any body.

**Invocation choice.** A model-invoked skill keeps its description
in the model's listing — permanent context load buying agent
discovery and reach from other skills. A user-invoked skill
(`disable-model-invocation: true`) pays zero context load, and its
description leaves the listing. Measured cost (router simulation,
3 trials × 4 name-carrying queries, 2026-08-06): with the
description listed, prose invocations ("run X", the bare name)
resolved 12/12; delisted, 0/12 — routers read the unknown name as
noise, and one routed the named request to a content-matching
competitor skill. Delisting is therefore safe only for skills
invoked by slash command (harness-resolved, no routing step); prose
invocation rides on the listing. Re-measure before flipping any
prose-invoked skill.

**The information hierarchy.** Two content types — steps (ordered
actions) and reference (rules and facts consulted on demand) — sit
on a ladder ranked by how immediately the consumer needs them:
in-file step, in-file reference, disclosed reference (a separate
file behind a pointer). Progressive disclosure is the move down the
ladder, and its test is branching: inline what every branch of the
skill's use needs; disclose what only some branches reach. Push too
little down and the top bloats; push too much and needed material
hides. Co-location is the within-file companion: a concept's
definition, rules, and caveats sit under one heading — scattering
fragments one meaning across many places, where duplication repeats
it; both are failures. No numeric word budget replaces this ladder:
the description is paid every turn, the body at invocation, a
reference when its branch fires — size each by what it costs where
it sits.

**Term selection recruits priors.** A word meant to steer thinking
is chosen for the priors it recruits: a term the domain's canonical
literature converged on — defined and re-used across a large
consistent body of pretrained text — carries a distributed
definition the skill gets free, repeated as a token, never
re-explained (observed: a 22-line skill's round format transferred
on mere contact, carried by one such term). Selection criterion:
the term the domain's canonical literature converged on — one a
practitioner recognizes without the skill's help — never the
operator's incidental phrasing
(echoing it mints a private dialect that recruits nothing; when the
operator's wording differs, use the canonical term and surface the
substitution), and a coinage only where nothing canonical exists —
a coined word pays in definition tokens what a pretrained term
gives free. Verification is the cold probe: ask a fresh context,
with no skill text loaded, what behavior the candidate term
implies; a term that reproduces the intended behavior from the word
alone recruits — one that draws a blank or a different behavior
does not. Coined tokens stay correct for machine-read vocabulary —
enum values, parser markers, status tags — where priors would
import unwanted meaning; words meant to steer thinking prefer
priors. Two consistency rules ride along: one term per referent
across the corpus (drift is grep-checkable — a referent named
differently in different files picks one canonical term, applied
uniformly), and terms scope-neutral within the skill's declared
scope (paradigm-neutral for a coding skill).

**The no-op test.** Every sentence must change the declared
consumer's behavior versus its default. The test is model-relative,
not reader-relative: two people disagreeing about a no-op disagree
about the default, and the question is settled by running the
document against the consumer — not by debate. A failing sentence
is deleted whole, not trimmed. The test grades leading words too: a
word too weak to beat the default is a no-op, and the fix is a
stronger word, not more words.

**Pruning.**

- One meaning, one home — a single source of truth per behavior, so
  changing it is a one-place edit. A leading word repeats a *token*
  on purpose; duplication repeats the *meaning*, costs maintenance,
  and inflates the meaning's apparent rank on the ladder.
- The environment is a source of truth (hypothesis, validate by
  use): a document restating `--help` output, config values, or
  directory layout is a cache, earning its load only where the
  lookup is expensive. Cache the
  unwritten convention, the reason behind a choice, the gotcha no
  config confesses; leave one-command lookups to the environment,
  where they cannot go stale.
- Relevance decays: a line loses it by never bearing on the task or
  by the world changing under it. Without a pruning discipline the
  default fate is sediment — stale layers that settle because
  adding feels safe and removing feels risky.

## The two registers

Steering text renders in one of two registers, and the choice
follows the consumer declaration and the mechanism split:

- The **directive register** commands the action ("always freeze
  fixtures") — for dispatchable sequence, gate text, and briefs to
  cheaper-tier consumers, where compliance outranks judgment.
- The **evidence register** states the observed fact and lets
  judgment weigh it ("live-anchored counts decay; frozen fixtures
  hold") — for judgment steering of top-tier consumers, where a
  command gets blindly obeyed out of scope or rationalized away in
  scope.

A rule that must hold regardless of judgment belongs in neither
register — it belongs in a mechanism (Enforcement). Register
follows the rule's action; its trigger is a separate axis: a
judgment rule whose firing moment is a recognizable event (a
hand-off, an approval, a start of work) under-binds in pure
evidence register — execution momentum carries past the moment and
the weighing never happens. Anchor the trigger at its named moment
(a convention or a gate); the action's register stays evidence.

**Positive rendering** (hypothesis, validate by use): where a rule
is directive, state the target behavior rather than the
prohibition — a ban drags the banned behavior into context and
half-reads as an instruction to do it. A guardrail that cannot be
phrased positively pairs the prohibition with its positive target.
Exempt: evidence-register failure-shape statements — an
anti-pattern's named shape IS the rule; those stay negative by
design.

**Imperative form.** Write skill content verb-first, not second
person ("Read the configuration file," not "You should read the
configuration file"). Mood is second-person-scoped, not a register
constraint — evidence-register statements are declarative by
design. The frontmatter description carries trigger phrases
stating what the skill does and when to use it, never second
person; second person remains correct inside user-facing output
templates and quoted speech.

## Steps and completion criteria

Every step ends on a completion criterion — the condition telling
the consumer the work is done (hypothesis, validate by use):

- **Clarity**: a vague bound ("understanding reached") invites
  premature completion — attention slips to *being done*, pulled by
  the visible later steps. Sharpen the bound first; split the
  sequence only when the bound is irreducibly fuzzy AND the rush is
  observed — and hiding later steps works only across a real
  context boundary (a subagent dispatch); an inline call leaves
  them in context and clears nothing.
- **Demand**: "every modified X accounted for" forces legwork where
  "produce a list" does not — and demand is not step-bound: "every
  rule applied" binds a body of flat reference the same way.

The strongest criteria are both checkable and exhaustive.

## Output discipline

A skill acts on findings actionable within its scope in the same
invocation, deferring only what needs out-of-scope structural
work — reporting-without-acting converts an enforcement mechanism
into a note-taker the operator must re-process. A decision surfaced
to the operator carries the skill's recommendation beside the
question, never a naked menu.

## Enforcement

The consumer does not self-enforce: a prose instruction it could
skip, it eventually skips — silently, on the success path, where
nothing catches it. Where a rule must hold, the check's evidence is
an **un-fakeable artifact** — one that cannot be produced without
doing the work the check represents. An enumeration with results
requires the checking; "checked all edge cases" is satisfiable
whether or not the work happened. N/A escapes inherit the
principle: a skip condition must be mechanically readable from
observable state (the diff, the document, the manifest), or the
escape is a fakeable claim wearing a scope note.

A decision or load-bearing rule left naked fails latently — the
consumer acts confidently and inconsistently, and the error
surfaces downstream. Mitigations in preference order:
(1) mechanical criteria computed from observable evidence (counts,
presence checks, cross-references); (2) structural enforcement — a
gate whose evidence is un-fakeable, judgment staying inside;
(3) a fail-loud downstream check, documented as the weakest option.

The instrument forms — blocking logic, the load gate,
dispatch-order encoding, phase-boundary commitment gates, handoff
information flow, the guard lifecycle for shipped hooks — are the
below-trust-tier and must-hold toolbox:
`references/enforcement.md`. Applying them to a top-tier consumer's
judgment work is the register error named above.

## Architecture

**Operational vs maintenance files.** Operational files load during
skill use: `SKILL.md` (entry; its description is the always-loaded
pointer) and `references/` (disclosed). Maintenance files never
do — the improvement journal (OBSERVATIONS.md), plans, roadmaps
live at source-repo level, outside the plugin payload, and are
never loaded by operational files. They are legitimate *write
targets*: "write the observation to OBSERVATIONS.md" names a
destination, not a read dependency. This keeps the journal out of
the method while the evolution cycle runs during use.

**Reference files are skill-local.** A SKILL.md loads files from
its own skill directory; a plugin-root `references/` is not a
supported home. Content shared across skills prefers one skill
(an entry skill plus sub-files) over duplicated copies — copies
drift. A model-invoked all-reference skill is another valid home:
other skills can invoke it. Reference needed by two *user-invoked*
skills can live in neither — no description, no reach; push it to a
plain file outside the skill system that any document can point at.

**Scope precedes default; the default owns its sentence.** Skill
text is absorbed in reading order by a reader acting on what it has
read so far: a strong default whose carve-out sits downstream leaks
— the scope cue lands at or before the default. Below the ordering
level, salience: a load-bearing default buried mid-sentence in a
packed enumeration parses but does not fire at its decision moment.
Give it its own sentence at the seam it governs; added rationale
only grows what it competes with.

## Lifecycle

A skill is written once and corrected forever. Use reveals a gap;
the gap becomes an observation (written to the journal — a one-time
mistake is not worth recording unless it names a class); an
observation that names a pattern becomes a change. A skill whose
work involves judgment, or that carries capability patches, keeps
an improvement journal; a corpus without correction machinery rots,
and machinery without restraint bloats.

**Two paths for every rule.** Path 1: an incident happened, and the
observation grounds the rule. Path 2: no incident — the rule is a
hypothesis, valid only when explicitly marked as one and validated
by use (techniques: `references/writing-by-skill-type.md`). The
invalid third thing is an unmarked guess presented as grounded.

**Durability classes.** Classify operational content by why it
exists. *Enforcement structure* (gates, un-fakeable artifacts,
boundaries) is durable — fakeability does not shrink as models
improve. *Capability patches* (teaching, checklists, blind-spot
lenses compensating a current weakness) depreciate: record
provenance in the journal at minting, log each firing there (a
dated line naming what the patch caught), and treat a patch with no
firing since the last consolidation as a cut candidate. *Bindings*
(paths, commands, tool facts) hold while the environment holds —
staleness-checked, not fire-checked.

**The era re-grade.** The no-op test is model-relative, so its
verdicts expire with the model era: when the consuming model moves
a tier or a generation, re-grade the corpus. Re-run the no-op test
over teaching content (Tier 2 of `references/evaluation.md` is the
instrument — settled by running, not debate); re-register surviving
directive-register patches against the register criterion (one that
now steers judgment re-renders in the evidence register; one that
needs no prose retires or precipitates into a hook or check);
staleness-check bindings. A corpus that never depreciates its
content is betting its reader never improves; the bet has lost
every time so far.

**Amendment discipline.** Prefer revising existing rules over
adding: (1) an existing rule covers the failure — revise in place;
(2) existing content becomes redundant or mergeable — reduce or
merge; (3) an existing rule's scope absorbs it — widen to the
underlying principle (a trigger too narrow abstracts upward; it
never grows an "…or X, or Y" list, whose next unlisted variant
slips through); (4) only then add. The corpus declares its
**governed set** — the files a concept may live in; absent a
declaration, the set is every operational file. Every addition or
repair is preceded by a search over that set for the concept, the
scan (command + hits) recorded as the edit's placement basis —
repairs get the same rigor as additions precisely because they feel
local. On amendment, audit each home the concept lives in for stale
or now-redundant restatement.

**Iterative narrowing.** Before any addition, classify the failure
it answers: *gap* (nothing covers it — add the minimum novel
content), *unloaded* (covered, never loaded — fix the pointer or
the load, not the content), *loaded-but-inert* (fix the trigger or
the register, not the content). Then enumerate what existing rules
already cover, subtract it, and re-apply — a single pass misses
sub-parts. Complete when further narrowing would lose content
nothing existing covers.

**Abstraction and context-independence.** State each rule at the
skill's declared scope: a domain skill is correctly domain-bound;
only a domain-general skill must hold across unrelated domains
(the test set lives in `references/review-checklist.md`,
Abstraction). Separately, the rule must behave correctly for a user
whose global configuration is empty — inline what it needs from
ambient context or make the dependency explicit and optional. A
rule can be fully abstract in wording and still assume conventions
that exist only in the author's environment.

**Rendering from a source.** Where a skill derives from a spec or
parent methodology, every load-bearing clause of the source
survives the render, and structurally-enforced source mechanisms
render as structural mechanisms — verified by clause-level diff run
by a context that did not write the render; the renderer is blind
to its own flattening (`references/anti-patterns.md`, Unverified
render). Edits to a render route through the source first.
Skill-craft itself is written direct — single home, no render
chain.

**Consolidation is done** when two consecutive review cycles
surface only wording fixes and no structural reorganization;
further passes return diminishing returns until a structural
finding appears.

## Evaluation

Build the evaluation before the procedure text: assemble the
triggering query set and name the skill's behaviour-delta
signature, then write the minimum text that passes them
(`references/evaluation.md`, Tiers 1–3; runner: `/eval-skill`).
Inspection is not measurement — a skill can read clean and still
under-trigger or sit inert.

## Reviewing a skill

After creating or modifying any skill, work through the review
questions (`references/review-checklist.md`), findings stated per
item — file:line for failures; the deepening rule rides with them.
The medium question (review-checklist.md, Enforcement item) — is
any of this text machine-read semantics belonging in a
mechanism? — is owed again whenever a section has grown since
its last review, repair laps included: momentum re-grades
correctness and never the medium (hypothesis, validate by use).

## Skill-craft's own conduct

- **Governed set**: `SKILL.md` + `references/*.md`, declared in the
  source repo's CLAUDE.md. Additions and repairs carry the
  search-before-add scan over that set as placement basis
  (Amendment discipline).
- **Self-review**: every change to those files dispatches one
  fresh-context self-review before commit
  (`references/self-review.md`); commit only after every finding
  has a recorded disposition.
- **Fire-born machinery**: no new gate, mandate, or checklist on
  skill-craft itself without one real incident as provenance —
  amendment over addition; the mint and each subsequent firing are
  logged in the journal; a mechanism with no firing since the last
  review is a cut candidate.
- **Reflexivity**: a gap noticed in this guidance during any use,
  design, or review is surfaced — the gap, the evidence, the
  proposed change — and the operator decides. Write the
  observation; propose, don't silently patch.
- **Packaging and release**: mechanics in
  `references/plugin-engineering.md`; releases run
  `/release-plugin`. Platform conventions (frontmatter schema,
  hooks syntax, agent definitions) belong to the official
  plugin-dev plugin (`plugin-dev@claude-plugins-official`) —
  skill-craft is the design methodology, not the platform contract.
