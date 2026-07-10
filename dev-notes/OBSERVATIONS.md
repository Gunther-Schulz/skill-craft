# Observations

Documented patterns of how skill design fails and what produces better results.
Each observation is grounded in real incidents. Read at skill invocation to
calibrate judgment.

---

## 1. Procedure contaminated with project-specific content

A skill's procedure contained real filenames and service names from the project
where it was developed. When applied to a different project, the examples were
confusing — they referenced components that didn't exist. The procedure's
abstract guidance was correct, but the embedded examples made it feel inapplicable.

The fix was separating observations (real incidents, abstracted) from procedure
(abstract method). The procedure works anywhere. The observations provide
grounding without contaminating the method.

---

## 2. Checklist as ceiling

A skill with 6 structural checks found issues in all 6 categories. Issues
outside those categories were not found — not because they were checked and
cleared, but because they were never looked for. The checklist became the scope
of the work rather than the minimum.

The fix was adding a deepening step: after each phase, take each finding and
trace its implications. The checklist seeds the investigation; findings expand
it beyond the checklist categories.

---

## 3. Findings recorded but not followed

A skill found "data layer has too many responsibilities" and "a subsystem lacks
a formal interface." Both correct. But the implications were never traced:
where are the contracts for that subsystem defined today? Are there other
subsystems with the same problem? Three adjacent issues were discoverable from
the first two findings but never found.

The fix: each finding is a lead. Follow it until it stops producing new
findings. Then move to the next checklist item.

---

## 4. Progressive disclosure ignored

A skill loaded a 500-line reference file at invocation. Most of the content
was irrelevant to the current task. The AI's context was consumed by guidance
it never used, reducing its effectiveness on the actual work.

The fix: reference files load on demand (the SKILL.md says "for X details, see
references/Y.md"). The main skill stays focused. Detail loads when needed.

---

## 5. Skill written once, never updated

A skill was designed, tested once, and deployed. Over months of use, multiple
workarounds accumulated — users learned to compensate for the skill's gaps
rather than updating the skill. The skill's observations file was empty.

The fix: establish the improvement cycle. Every failure during use is a
candidate observation. Every observation is a candidate procedure change.
A skill without observations is a skill that hasn't been used enough or
hasn't been maintained.

---

## 6. Reflexivity gap

While using one skill, a failure revealed a gap in a different skill's
guidance. The gap was noticed, discussed, and fixed — but only because the
user happened to connect the two. The skill itself didn't surface the
connection.

The fix: skills should notice when their own guidance (or the guidance of
the skill-craft guide itself) is incomplete or contradicted by experience.
Not automatic changes — suggestions with reasoning, for the user to decide.

---

## 7. Abstraction level not self-verified during skill updates

When adding a checkpoint to another skill (Clippy's investigate-design),
the initial proposal was domain-specific: "test for substring collisions,
boundary conditions in string matching." A human had to challenge: "is
this sufficiently abstract for any project?" The revised version — "test
inputs at decision boundaries for any decision logic" — was correct and
project-agnostic, but the AI didn't self-check the abstraction level.

Skill-craft's procedure says procedures must be "project-agnostic to work
in any codebase." But there's no checkpoint that fires during skill
updates asking "is this proposed rule/checkpoint abstract enough?" The
principle exists (Layer 3: procedure from observations separation) but
there's no forcing function that prevents domain-specific checkpoints
from slipping into another skill's procedure.

The fix: when proposing changes to any skill's procedure or reference
files, self-check abstraction before presenting: "Would this checkpoint
make sense in a codebase that has nothing to do with the current project?
If the examples are domain-specific, abstract them." This is a reflexivity
improvement — skill-craft applying its own principles to itself.

*Observed: 8 April 2026. Discovered while updating Clippy investigate-design
during agentplane project work.*

---

## 8. Workflow skills create internal rules that need rule-based validation

A workflow skill (Clippy investigate-design) proposed heuristic matching
logic during its design phase. The workflow procedure defined phases,
gates, and transitions — but the heuristic within one phase was not
validated with Path 2 techniques (non-firing case enumeration). The
"Writing workflow procedures" section and "Writing rule-based procedures"
section were separate categories with no connection.

The fix: added a bridge paragraph to "Writing workflow procedures" —
when a workflow phase produces decision logic, apply Path 2 techniques
to that logic. A heuristic proposed inside a workflow phase is an
internal rule.

*Observed: 8 April 2026. Same incident as observation 7.*

---

## 9. Self-reported completion passes observable checkpoint but is unfalsifiable

A blocking check asked "verified all assumptions?" The AI answered yes
with evidence "all verified." This passed the observable checkpoint test
(it's an action, not a feeling). But the evidence was unfalsifiable —
there was no way to tell if "all" actually meant all, or just the ones
the AI thought of. The missing edge case was discovered post-implementation.

The fix: added self-reported completion as a third category in Layer 2's
observable checkpoints. Evidence must enumerate what was checked, not
just claim completeness. "Checked these 3 cases: [list]" is observable.
"Checked all cases" is not.

*Observed: 8 April 2026. Clippy readiness check reported [READY] but
keyword matching edge cases were not enumerated.*

---

## 10. Guide existed but wasn't followed during creation

A skill about plugin design included a reference document covering the
two-layer marketplace/plugin structure. When the skill's own repo was
created, it used a flat structure (plugin.json at root, no marketplace.json)
and failed to install. The knowledge was in the guide — it just wasn't
applied to the guide's own packaging.

The fix: added a "New plugin setup" checklist to the reference — the minimum
steps from empty repo to installable plugin. Having the knowledge documented
is not enough; a concrete setup sequence prevents the most common first-time
mistake.

---

## 11. Judgment call left naked in skill flow

A workflow skill (Clippy autopilot) applied the same per-unit ceremony
— investigate subagent, executor subagent, reviewer subagent, checkpoint
file — to every unit regardless of complexity. Observed session: 4 units,
2 trivial (4-6 lines of line-replacement, log-swallow fixes), 2 nontrivial
(70-line new function with parameter threading, 400-line test suite).
Trivial units absorbed the same cost as nontrivial ones. The user flagged
the disproportion.

The underlying issue was not ceremony size. It was that "is this unit
trivial or nontrivial?" was a decision point in the skill's flow with no
mechanical criteria behind it. Any resolution at runtime would have been
AI judgment — inconsistent across runs, and potentially missing adjacent
bugs. In this session, unit-001 was a 4-line fix sitting next to a
related bug (a ghost-doc race) that the full investigation caught.
Self-classification as "trivial" would have skipped the investigation
that found it.

This generalizes beyond workflow skills. Any skill with a control-flow
decision point — fast path vs normal, include vs skip, defer vs act,
what severity, which category — that lacks mechanical criteria leaves a
naked judgment call in the flow. Observation 9 addressed the VERIFICATION
analog (self-reported completion with unfalsifiable evidence). This is
the DECISION analog: don't let the AI decide, give it criteria.

The fix: added a named "Judgment calls as design risk" principle at the
start of Layer 2, before forcing functions. Added a "Naked judgment call"
anti-pattern to references/anti-patterns.md. Extended the existing
"Decision logic within workflow phases" paragraph (itself grounded in
observation 8) to reference the new principle as the general case.

On post-edit review (user-prompted), the review caught project-specific
contamination ("fast-path", "contracts_produced") and restatement fluff
in the first drafts. This revealed that skill-craft's own "run the
review checklist" rule was stated as a standalone section but not
structurally bound into any workflow — the review happened because the
user asked for it, not because the skill enforced it. Two further fixes
followed: Fix A bound the review checklist into "After creating or
modifying a skill" as a required pre-commit step with blocking logic;
Fix B added a "Domain-independence check" in Layer 2 that fires at
write time, as an earlier net than the Layer 5 abstraction check. The
meta-lesson: a rule stated in isolation is not an enforced rule — it
is a hope.

*Observed: 12 April 2026. Clippy autopilot session implementing a
harness resume bug fix. Unit-001 (4-line checkpoint.py fix) and unit-002
(6-line silent-swallow fix) each triggered the full per-unit protocol
including a per-unit re-investigation cycle that duplicated evidence
already present in the parent tracker.*

---

## 12. Mental model drift — skill files drafted as documentation

An AI implementing a skill-craft-governed change drafted 6 files of
procedure and reference content. The drafts passed the mandatory
post-edit review checklist on density — by the same AI that wrote them.
A human reader then pointed at one closing paragraph and asked whether
it was aligned. It wasn't — it was pure documentation (cross-reference
to another skill, restated imported principle, motivational framing).
Scanning the rest of the implementation revealed the same pattern
everywhere: Purpose sections explaining why files existed, Rationale
paragraphs explaining why thresholds were chosen, Failure-mode
paragraphs narrating what each step prevented, Summary sections
restating content already present above. Roughly half of the content
by line was documentation for a human reader who does not exist during
skill execution.

The rule "Every sentence must change behavior" covers this in theory.
In practice, the drafter rationalized each documentation category
individually (this is context, this is provenance for future
maintainers, this is a cross-reference that helps the reader) and the
fluff list was read as exceptions to justify rather than as patterns
to delete. The underlying rule that catches all categories at once is
the reader model: the only reader of a skill file is the AI in
mid-execution, and documentation belongs in files that are not loaded
during execution.

This is the second self-review failure in the same session. The first
caught project-specific contamination (observation 11, Fix A) because
contamination is mechanical — a wrong field name is easy to audit
against "is this generic?" The second missed documentation drift
because drift looks "reasonable" to the drafter and each paragraph has
a defensible-sounding justification. Self-review by the drafting
context is strong against mechanical violations and weak against
register drift. A separate review context (subagent or human) catches
both.

The fix: add the reader model to Layer 2's density guidance as an
explicit paragraph before "Every sentence must change behavior", and
add a matching preamble to `references/anti-patterns.md` so a reviewer
loading anti-patterns starts with the same lens. With the reader model
stated up front, a drafter auditing their own work can ask one
question — "does this sentence serve the executing AI?" — instead of
enumerating the fluff list category by category and rationalizing past
each. The test is faster, harder to rationalize past, and catches
documentation drift at the time of writing rather than at the time of
review.

*Observed: 12 April 2026. Clippy plugin, PR 2 of the fast-path
classification implementation. The drafting AI could not see the
register drift on self-review; a human reader caught it. Same session
as observation 11.*

---

## 13. Seeded observations — a skill can be born with a notebook

The evolution model in PROCEDURE.md (Layer 4) describes observations
as reactive: a failure happens during skill use, the failure is
abstracted into an observation, the observation informs procedure
refinement. "Use skill → notice failure → abstract → observe →
refine → use again."

This misses a legitimate mode: a skill can be born with observations
already in place, seeded from the work that produced the skill. When
a practitioner recognizes a pattern that worked in real experience
and crystallizes it into a new skill, the evidence motivating the
skill's procedure is already on hand. Discarding it and waiting for
the skill's first invocation-failure to re-derive the same evidence
wastes what the practitioner knows.

The pattern was observed when designing a skill called `titrate`
(empirical iteration for non-deterministic systems). The skill's
OBSERVATIONS.md launched with seven observations extracted from a
multi-day iteration session that produced the titration pattern —
not from the skill's own use, but from the work that motivated the
skill. The seeded observations grounded the procedure's checkpoints
from invocation zero instead of leaving the skill's first several
uses to rediscover them.

Constraints for valid seeding:
- Observations must still be abstracted — no project-specific
  filenames or domain examples in the procedure itself, and
  observations themselves should use generalized language where
  possible (while retaining the incident as grounding).
- Seeded observations must correspond to actual incidents, not
  hypothetical ones. A seeded observation "invented" to justify a
  checkpoint is a fabricated ground — it lies.
- The seeded observations should be marked as such (an explicit
  note that they came from the founding work), so the first
  non-seeded observation is distinguishable.

The fix to skill-craft: Layer 4's evolution cycle should explicitly
acknowledge seeding as a legitimate mode. The current flow reads as
the only valid path; it is one of two.

*Observed: 21 April 2026. During the design of the `titrate` skill.
The practitioner asked for observations to be seeded from the
originating LLM-pipeline iteration session; the resulting
OBSERVATIONS.md had seven entries before the skill was ever invoked.
The framing suggested an amendment to skill-craft's own guidance
rather than a private choice inside titrate.*

---

## 14. Plugin reinstall friction during heavy iteration

When a plugin's skills are under active development with many edits per
session, the standard install/uninstall cycle becomes a friction point.
Every cache refresh requires either bumping the version in plugin.json
(making the git history noisy with version-only commits) or running
uninstall+install (round-trip through the marketplace clone, multiple
seconds per cycle).

The marketplace+cache architecture is designed for distribution, not
for the plugin author's dev loop. The cache is a real copy of the
plugin folder under
`~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`, and
Claude Code reads from it directly.

The fix is to replace the cache copy with a symlink to the source
plugin folder for the duration of active development:

```
rm -rf ~/.claude/plugins/cache/<mp>/<plugin>/<version>
ln -s /path/to/repo/plugin \
      ~/.claude/plugins/cache/<mp>/<plugin>/<version>
```

After this, edits to the source plugin folder are visible to Claude
Code on `/reload-plugins` alone — no version bump, no reinstall. The
standard flow returns whenever the user runs `claude plugin uninstall`
or bumps the version (the cache path includes the version).

This is a development-time optimization, not a distribution mechanism.
End users still install normally via the marketplace.

The fix to skill-craft: `references/plugin-engineering.md` should
document the symlink technique under "Local development" as an option
alongside the standard reinstall workflow, with a small idempotent
shell template authors can drop into their plugin repos.

*Observed: 28 April 2026. During scaffolding of the `pbs-bureau`
plugin. Iterating on a master orchestrator skill required many small
edits per session; the bump-and-reinstall cycle became visible
friction. A `dev-link.sh` was added to the plugin repo that creates
the cache symlink, reading name/version from manifests for safety.
After symlinking, `/reload-plugins` alone picks up edits.*

---

## 15. Silent revision of standing commitments across cycles

A coding-clippy session showed AI recommendations drift between cycles
without explicit surface. Cycles 3-5 of an investigation consistently
recommended Option G-1. At "i" entry (implementation activation), the
AI silently switched to "Option B alone" — a narrower alternative not
surfaced as a recommendation in any prior cycle. The switch happened
with internally-plausible reasoning ("more surgical") but no flag that
the AI was changing its own prior standing recommendation. The
operator pressed "i" expecting G-1 and got B.

This is the same shape as Path 2 technique "Refine by removal;
transcribe verbatim or surface every change" — the silent-augmentation
discipline applied to skill-text porting — but extended to a different
artifact: the AI's own prior recommendation, not operator-approved
text. The general pattern: AI commitments persist across cycles, files,
and phases. Any change requires explicit surface. Silent revision is a
discipline violation regardless of which artifact carries the
commitment.

The fix in this incident landed as a structural gate in the consumer
skill (coding-clippy's composer "i" routing checks the implementation
plan against the standing recommendation; silent swap blocked). The
broader skill-craft implication: skills that produce recommendations
or stated positions across cycles need an explicit "no silent
revision" check at every phase boundary where the position could be
redrawn.

**Promoted to procedure rule in v1.0.4** — added as a Layer 2 principle
"Commitment consistency across phase boundaries". The Path 2 technique
"Refine by removal; transcribe verbatim or surface every change"
remains the author-side discipline (writing rule text); the new Layer 2
principle is the runtime-side discipline (skills producing commitments
across phases).

*Observed: 17 May 2026, beat-the-books project, Clippy investigation
of a txn-poison fix. Mitigation landed in coding-clippy v0.5.2.*

---

## 16. Rule proposals over-broad without operator pushback

During a Clippy roadmap update, an "output discipline vs digestibility
tension" entry was drafted as a broad framework with three resolution
patterns including a generic operator-override shortcut. Two rounds of
operator pushback narrowed it: first round revealed the underlying
incident was rule-violation (AI shortcut existing strict rules), not
rule-gap; second round revealed 5 existing Clippy rules already
covered most of the surface-vs-internal boundary the framework was
trying to design. Final framing: 3 narrow clarifications plus an
explicit withdrawal of the operator-override as a generic shortcut
shape.

Without the pushback, the broad framework would have shipped. The AI
applied the amendment discipline 4-step ("check if existing rules
cover it") once, classified the incident as rule-gap, and stopped.
The single pass missed sub-parts of the proposal that further
enumeration would have shown were already covered.

This reveals a gap in how the amendment discipline is APPLIED, not in
its content. The 4-step gives the static framework. What was missing
is iteration — re-applying the 4-step to each narrowing as new
existing-rule overlap surfaces. Without iteration, the AI ships the
first-pass framing even when most of it overlaps with existing rules.

The fix is a new Layer 4 sub-section ("Iterative narrowing of rule
proposals") with explicit steps for re-examining incident
classification, enumerating existing rules, subtracting overlap, and
re-applying iteratively until the proposal cannot be narrowed further
without losing content no existing rule covers. Composes with the
existing amendment discipline rather than replacing it.

*Observed: 17 May 2026, coding-clippy roadmap update session. P11
"output discipline" entry narrowed from broad framework to 3 specific
edge cases over two operator-pushback rounds. Iterative narrowing
rule landed in skill-craft v1.0.5.*

---

## 17. Soft "load X" pointers treated as informational, not imperative

A skill listed reference files as dependencies and instructed loading
them via prose pointers scattered through the skill body ("for full
checklists, load X", "for detailed rules, see Y"). Measurement found
~0% of load-bearing reference files were actually loaded at skill
activation — the AI read the prose pointers as informational ("there
is a reference doc") rather than imperative ("execute a Read now"),
proceeded without loading, and substituted pattern-memory of past
sessions for the actual file content. Output looked spec-compliant
because the AI reproduced the expected shape from memory; it diverged
from the current reference files silently.

The root cause is format. Prose imperatives produce no observable
artifact — the AI can skip the load and the output looks identical.
This is the same failure shape Observation 9 identified for
self-reported completion: a claim with no verifiable evidence behind
it. Blocking logic already solves it for workflow steps; reference
loading is structurally the same — a step that, skipped, is always
wrong, with no visible failure.

The fix extends "Blocking logic" (Layer 2) to cover reference
loading: one consolidated load gate at skill activation requiring a
loaded-references manifest (files + sections read) as evidence,
rather than N soft pointers through the body. It also qualifies
"Progressive disclosure" (Layer 3) — progressive disclosure correctly
keeps genuinely-optional references on-demand, but load-bearing
references must be gated, not pointed at.

*Observed: 20 May 2026, coding-clippy spec-load investigation.
Measured ~0% activation-load rate for verification-layer reference
files (roadmap P21). Fix landed in skill-craft v1.0.6 as a Layer 2
sub-section. Path 2 — promotes to Path 1 when the consuming plugin's
load rate measurably improves after gating ships.*

---

## 18. Skill behavior depends on ambient user context

A skill's portability rules — domain-independence, language
agnosticism, the Layer 5 abstraction check — all verify the skill's
rule CONTENT is abstract. None verifies the skill's runtime BEHAVIOR
is independent of the user's ambient environment: global instruction
files, tool settings, prior-session memory. A skill can pass every
content-abstraction check yet still assume context that exists only
for the user who built it. "Follow the user's testing conventions"
is domain-neutral in wording but assumes such conventions exist
somewhere ambient — the content-abstraction checks green-light it.

A skill installed by any user must behave correctly regardless of
what global instructions, settings, or memory that user has.
Context-independence is a distinct portability axis from content
abstraction.

The fix is a sibling rule in Layer 2 alongside domain-independence:
a context-independence check at write time.

*Observed: 20 May 2026, coding-clippy session. A consuming plugin
maintained a standing rule that it must "perform correctly without
assuming any particular global CLAUDE.md exists." The principle
generalizes to any skill — landed in skill-craft v1.0.7 as a Layer 2
sibling to domain-independence.*

---

## 19. "Rule-violation" conflates two failure classes with different fixes

The iterative-narrowing rule (Observation 16, Layer 4) distinguishes
rule-violation (an existing rule would have prevented the failure if
followed) from rule-gap (no existing rule covers it). Applied to real
failure diagnosis, the two-way split proved too coarse —
"rule-violation" hides two distinct classes:

- The rule existed but was never loaded into context — the AI could
  not follow a rule it never read. Fix: the loading mechanism (a load
  gate — Observation 17).
- The rule existed, was loaded, and still didn't fire. Two sub-cases:
  the trigger or articulation was too weak (fix: sharpen it), or the
  rule was clear and unambiguous but skippable because nothing
  structurally enforced it (fix: convert the prose imperative to a
  blocking gate or verifiable-artifact requirement). A clear rule
  that is simply not done is the second sub-case — an enforcement
  problem, not a wording problem.

Both produce an identical observable failure, but the fixes are
unrelated — a loading gate does nothing for a loaded-but-inert rule,
and a trigger refinement does nothing for an unloaded one. Collapsing
them into one "rule-violation → add enforcement" bucket sends the
wrong fix.

The fix extends iterative-narrowing step 1 from a two-way to a
three-way distinction: rule-gap / unloaded / loaded-but-inert, with
step 4 split accordingly.

*Observed: 20 May 2026, coding-clippy session. Operator caveat that
observed plugin failures could trace to rules never loaded rather
than rules missing. Extension landed in skill-craft v1.0.7. Refined
v1.0.10: loaded-but-inert split into two sub-cases (weak articulation
vs clear-but-unenforced) after an incident where a clearly-worded
"mandatory minimum" rule was simply never run — an enforcement gap,
not a wording gap.*

---

## 20. Skill-craft's own guidance assumed skill-craft's context

An audit of PROCEDURE.md — prompted by a v1.0.8 fix where one rule
assumed a grounding incident always exists — found the same shape in
several other places. Skill-craft's guidance carried assumptions valid
only for skill-craft itself, not for the general skill-builder the
guidance is written to serve:

- The Layer 5 reflexivity rule said "if the experience reveals that
  the skill-craft guidance itself is incomplete" — written from
  skill-craft's self-improvement viewpoint, though Layer 5 is meant to
  teach any skill-builder to make their own skill reflexive.
- An example path in the post-edit procedure hardcoded the
  maintainer's home directory.
- Skill-craft's own OBSERVATIONS.md sat inside the plugin payload
  (`plugin/skills/skill-craft/`), so the distributable carried
  skill-craft's development journal — including project names from the
  maintainer's own work.
- Separately, "When an observation becomes a procedure change" stated
  that procedure changes without grounding observations "are guesses,"
  contradicting Path 2, which legitimizes blank-slate rules as
  hypotheses.

The unifying pattern: skill-craft is both a methodology and a skill
that applies the methodology to itself. Without care the two roles
blur — self-improvement machinery and project-specific content leak
into the distributable teaching. The fix keeps the distributable (the
plugin payload) purely the methodology, and keeps skill-craft's own
maintenance artifacts at the source-repo level.

*Observed: 20 May 2026, coding-clippy session, audit of skill-craft
PROCEDURE.md. Fixes landed in v1.0.9: maintenance files moved outside
the plugin payload; Layer 5 phrasing made generic; hardcoded path
genericized; observation-vs-Path-2 contradiction resolved; a placement
rule added to the Category 2 taxonomy.*

---

## 21. The un-fakeable-artifact principle is stated twice, never named

Layer 2 states one principle in two places without consolidating it.
"Observable checkpoints" says self-reported completion is fragile —
"the enumeration is observable; the claim of completeness is not."
"Structural enforcement" says blocking logic needs enumerated
evidence — "the enumeration is verifiable; a claim of completeness is
not." It is one principle stated twice: a mechanism's check must rest
on an artifact that cannot be produced without doing the work the
mechanism represents. Diffused across two entries and never named, it
is harder to invoke as one thing and easier to half-apply.

Suggested, not yet applied — for the maintainer to decide:
consolidate the two into one named principle, the
*un-fakeable-artifact principle* — a mechanism's output must be an
artifact that cannot be produced without doing the work it
represents; a form check ("N items present," "a sample exists") is
satisfiable whether or not the work happened. A named principle is
easier to reference — from the per-type guidance and from reviews —
than the diffused version.

*Observed: 21 May 2026, coding-clippy session. The Clippy spec names
this crisply as "the un-fakeable-artifact rule"; a cross-level review
of skill-craft against the spec surfaced that skill-craft holds the
same principle, diffused. Actioned 2026-05-21 in the skill-craft
review (Layer 2 pass): the principle is now named in `PROCEDURE.md`
Layer 2 — "The un-fakeable-artifact principle" — and the two diffused
statements reference it.*

---

## 22. Abstraction guidance conflated within-domain abstraction with cross-domain universality

skill-craft's review checklist (item 5, abstraction) and the Layer 5
abstraction check were applied to a skill — Clippy — that is
deliberately the *coding instance* of a domain-general framework (the
Anneal framework). The checks read as demanding cross-domain
universality: the Layer 5 exclusion tests ask whether a change
"applies to diverse problem domains" and "works across diverse
languages and runtimes," and the Layer 2 domain-independence check
said to "enumerate at least two domains outside the current project
... if it only works in one domain, it is contaminated." Clippy is
correctly coding-specific — it uses "codebase," "file," "symbol,"
"grep." Read literally, the tests flag those as contamination.

The guidance was internally inconsistent. Layer 2's terminology
agnosticism already accepted domain-specific skills — "for a coding
skill that means paradigm-neutral terms" — while the domain-
independence check and the Layer 5 abstraction check demanded
cross-domain reach. A skill can legitimately be domain-specific: most
skills are (a coding skill, a GIS skill), and a skill that
instantiates a domain-general framework for one domain is bound to
that domain by design. What every skill must avoid is contamination
by one *project's* specifics and one *paradigm's* variant terms — not
domain-specificity itself.

The fix: abstraction is judged against the skill's intended **scope**.
A domain-specific skill is abstract within its domain and
domain-specific overall — correct. Only a domain-general methodology
skill (skill-craft, a framework) must reach across domains. The Layer
2 domain-independence check, the Layer 3 procedure/observations
separation, the Layer 5 abstraction check, and review-checklist item
5 were reworded to make the scope explicit.

*Observed: 2026-05-21, coding-clippy. Surfaced in the skill-craft
review of the rewritten Clippy plugin — Clippy being the coding
instance of the Anneal framework. Fix landed in skill-craft
v1.0.12.*

---

## 23. Layer 1 had no guidance for multi-skill plugins or shared content

A plugin was built as five skills that shared a set of reference
files, placed in a `references/` directory at the plugin root. The
Claude Code plugin documentation documents skill reference files as
**skill-local** — referenced from a `SKILL.md` relative to its own
skill directory — and the plugin root has a fixed set of recognized
component directories (`skills/`, `commands/`, `agents/`, `hooks/`); a
plugin-root `references/` is not one of them and is not a supported
home for shared content. The layout was off-pattern and the
cross-directory reference from each skill to the shared files was
fragile. It forced a restructure: the five skills collapsed into one,
the others becoming sub-files and the references skill-local.

Layer 1 showed only a single-skill directory diagram and said nothing
about plugins with multiple skills or about shared reference content.
The off-pattern layout passed every existing check because no check
addressed it.

The fix: a Layer 1 paragraph on multiple skills and shared content —
reference files are skill-local; the plugin root has no `references/`
component; when several skills would share reference material the
structural choice is one skill (orchestrator plus sub-files) versus
duplicated per-skill copies, and one skill is preferred when the
material is load-bearing for all of them. The exact path mechanics for
bundled-file references belong to the official `plugin-dev` plugin and
the Claude Code docs — skill-craft owns the architecture lesson, not
the volatile mechanics.

*Observed: 2026-05-21, coding-clippy. Discovered during the
skill-craft review and a Claude Code plugin-docs check while
rewriting the Clippy plugin. Fix landed in skill-craft v1.0.12.*

---

## 24. A framework rule lost its structural enforcement in the rendering to an instance

The Clippy plugin is rendered from the anneal-framework spec. A
load-bearing behavioral rule — the AI self-resolves design decisions
and does not pose them to the operator as choices (framework
`core.md` §1) — was rendered into the plugin's investigate-design
phase file as "self-resolve and record," dropping the "does not pose
as choices" clause and the rule's structural framing. The first
empirical run posed three design decisions to the operator as
questions.

Two skill-craft failures compounded:

- **The rendering was an unverified lossy paraphrase.** A load-bearing
  clause silently dropped; what survived flattened from a structural
  rule to a soft principle. Nothing verified the rendered text against
  the source — and the renderer's own review missed it, because the
  drafting context is blind to its own flattening (observation 12).
- **The structural-enforcement mandate did not fire.** "Judgment
  calls as design risk" (Layer 2) was framed around classification
  decision-points; a standing behavioral rule phrased as a positive
  instruction did not trip its trigger, so the renderer treated
  "self-resolve" as a principle to state, not a rule to enforce.

The fix to skill-craft: a new Layer 2 sub-section, "Rendering from a
source" — render faithfully, structural-as-structural, verified by a
clause-diff against the source — plus a matching review-checklist
item. And "Judgment calls as design risk" widened: its trigger now
covers any load-bearing rule, not classification decision-points
alone. The framework-side root causes (the un-fakeable-artifact rule
generalized to behavioral rules, the design-decision definition, the
closed cycle-boundary output, the prescription-discipline split)
landed in the anneal-framework spec.

*Observed: 2026-05-21, coding-clippy. The first empirical run of the
rewritten Clippy plugin. Fixes landed in skill-craft v1.0.13.*

---

## 25. Subagent-introduced speculative-cruft — caught by CI tier, not by lens set

A coding-clippy unit-14 implement-phase subagent (U5) imported
`ProviderMarketData` from `services.market_broker` as part of typing
context for its per-position max_bet work, but the final code path only
used the sibling type `AggregatedMarket`. The unused import survived
the implement-phase self-check (the Coupled-change / Branch-coverage /
Failure-path lenses don't inspect imports) and was caught by the
verify-phase mechanical CI check (`ruff check --select F821,F401,F811`).

The failure shape: **speculative-cruft** — symbols introduced from the
subagent's reasoning context during exploration but not load-bearing
in the final code. Distinct from semantic gaps (which the lens set
catches); fundamentally lint-tier mechanical-tool territory.

Considered a framework rule: extend the implement-phase self-check to
require running the project's CI-tier gate on the diff before commit,
shifting the catch from verify (cost: 1 commit + delta verify pass,
~5 min) to pre-commit (cost: ~30 sec gate run per unit). The proposal
was drafted and shipped to `core.md` §4.2 + clippy + daneel implement
renders. A bildhauer pass on the shipped artifact surfaced thin Pareto
justification at n=1:

- Verify-phase already catches this — practice 8's "operator catch
  remains" disposition covers failure shapes not tractable for upfront
  codification.
- "Extends verify" framing was the Pareto-justification, but on
  inspection the extension was duplication-shifted-earlier rather than
  coverage-gained.
- Instance-binding brittleness: the rule needs each project to have a
  recognizable CI gate, which becomes naked-judgment for projects
  without one.

The shipped edits were reverted. Verify-phase backstop remains the
design intent. The observation is preserved here so that if
speculative-cruft incidents recur and the verify-catch cost
accumulates, the framework rule earns its place at n≥2.

*Observed: 2026-05-26, coding-clippy unit-14 verify-phase pass 2
surfaced single F401 (commit c6346b33 closed it). Codification
considered, drafted, shipped, then reverted after operator-triggered
bildhauer pass exposed thin Pareto justification. No fix shipped to
spec; pattern documented here for future-incidence escalation.*

---

## 26. Soft-load-pointer false-positive: provenance citation read as a load-bearing pointer

During an instance-plugin render review (anneal-dev, a framework instance), a
fresh skill-craft review subagent raised a **blocking** finding: a phase file
"defines its verification battery in an unloaded file" because the clause cited
`bindings.md` and `bindings.md` was in no load gate — i.e. the Soft-load-pointer
anti-pattern (#17). On independent re-derivation against the artifact, the battery
was rendered **inline** in the loaded phase file; the `(bindings.md …)` was a
**provenance citation** (source-attribution for content that is present), not a
pointer to content that must be loaded. The reviewer conflated the two; the
"blocking" was a false positive.

The gap: the Soft-load-pointer anti-pattern keys on "reference named in prose
without an observable load step" — but that description matches BOTH (a) a
load-bearing pointer (content lives in the named file and must be loaded → a real
soft-load-pointer) AND (b) a provenance citation (content is rendered inline; the
named file is cited for source-attribution / re-render fidelity → not a
soft-load-pointer). The true discriminator is **whether the load-bearing content
is present in a loaded file**, not whether a file is named in prose.

Proposed change (operator decides; not made): add a discriminator to the
Soft-load-pointer anti-pattern — a citation is a soft-load-pointer only if the
load-bearing content is NOT present in a loaded file; a citation that attributes
the source/provenance of content rendered inline is not one. Test: would the AI
behave wrong WITHOUT loading the named file? If the content is inline, no. The
discriminator doubles as a reviewer guard against this false-positive.

*Observed: 2026-06-02, anneal-dev step-5 render skill-craft review (subagent
a26608dcf75a31ff6) flagged blocking B1; re-derived against verify.md:57-82 /
implement.md:108-161 (battery + isolation rendered inline) as a
provenance-citation false-positive. Relates to #17 (Soft "load X" pointers).*

---

## 27. Measurement vetoed an inspection-favored description change

The Anthropic-manual audit and a first read of a triggering eval flagged
skill-craft's own `description` as under-triggering: it claimed "plugin
structure" — territory delegated to plugin-dev — and lost a plugin-architecture
query ("structure a new plugin that bundles three skills sharing reference
docs") to `plugin-dev:plugin-structure`. Inspection-logic prescribed a rewrite:
drop the delegated overclaim, foreground the differentiator ("make a skill the
model reliably follows").

Measuring the candidate before shipping it (Tier 1, `references/evaluation.md`)
reversed the conclusion. Across three blind router trials the new description
changed zero routing outcomes: still 5/5 fires on unambiguous skill queries,
0/4 false-fires on near-misses, and the plugin query still routed to
`plugin-dev:plugin-structure` — because its literal verb ("structure a new
plugin") is plugin-dev's, and it is a genuine compose/boundary case
(skill-craft's own SKILL.md says "use both" for plugin building), not a
triggering defect. The proposed fix was outcome-neutral and its premise — "that
query is a skill-craft miss" — was wrong.

Lesson: a description that reads like an overclaim is not necessarily
mis-triggering — only measurement settles it. Tier-1 evaluation earns its place
by vetoing plausible inspection-favored changes, not only by catching gaps. The
disciplined output was a change NOT made: keep the working description;
reclassify the boundary query rather than broaden the description to win it
(Additive-reflex, `anti-patterns.md`). The current description triggers cleanly
(5/5 unambiguous, 0/4 false).

*Observed: 2026-06-05, skill-craft self-audit against Anthropic Agent-Skills
best-practices; baseline + retest each 3 blind router subagents over a 10-query
set (6 should-trigger, 4 near-miss). First live use of `references/evaluation.md`
Tier 1. Caveat: simulated routers, n=3, indicative not production-harness.*

---

## 28. First end-to-end /eval-skill Tier 2 run — runner mechanics validated; signature spec too narrow to measure skill-craft's actual value (the test was a softball)

The new `/eval-skill` runner (v1.0.63) was first applied end-to-end to
skill-craft itself in Review mode. Signature spec named four observable
elements: (a) 13-item review-checklist citation by canonical name;
(b) file:line citation per finding; (c) per-item pass/fail verdict;
(d) anti-pattern names from `anti-patterns.md`. Task: review a
contrived `csv-utils` SKILL.md with five planted defects pulled from
`anti-patterns.md` (vague description, soft-load-pointer, naked
judgment, project-specific contamination, second-person prose).
WITH-skill and WITHOUT-skill subagents dispatched in parallel.

Surface result: all four signature elements present in WITH, absent
in WITHOUT (structural delta was sharp: 13-item checklist vs 5
ad-hoc sections; ~20 line cites vs 2; per-item verdict vs narrative).
Catch rate: WITH 5/5; WITHOUT 4/5. WITHOUT missed the imperative-form
/ second-person violation.

**The result is largely an artifact of test design, not a fair
measure of skill-craft's value.** Three honest limits:

1. The five planted defects came from skill-craft's OWN
   `anti-patterns.md` catalogue, so a bare model with general
   skill-design training pattern-matches most of them without
   needing the framework loaded. WITHOUT scored 4/5 on defects
   skill-craft itself helped popularise.
2. Single-shot review never fired skill-craft's load-bearing
   machinery — self-review subagent mandate, evolution cycle,
   amendment discipline, rendering-from-source check. None have
   a chance to differentiate on one ad-hoc review.
3. Signature was structural (checklist + cites + named patterns) —
   the shallowest layer of value. The deeper value lives in (a) the
   meta-machinery above and (b) named-rule catches with no
   plain-English shorthand (imperative-form, scope-precedes-default,
   naked-judgment-in-rule-statements), most untriggerable in a
   single review.

Where skill-craft's value measurably showed this session — *outside*
this controlled experiment, in live editing of skill-craft itself —
the mandated fresh-context self-review subagent caught: a
second-person violation in `evaluation.md` (imperative-form rule); a
wrong `OBSERVATIONS.md` path in `eval-skill.md` (boundary rule;
**blocking**); a soft-load-pointer in `eval-skill.md` Step 1
(`anti-patterns.md`; **blocking**); a stale `(c)` reference after the
N2 fix collapsed Step 2 to (a)/(b) (cross-file consistency). Each was
a named-rule catch the authoring context demonstrably missed — they
came in as either blocking or notable on the authoring AI's own
draft. Those catches are skill-craft's real signature, firing in
the workflow the framework was designed for (multi-pass
canonical-file editing with mandated review), not in a single-shot
review of a contrived input.

Lesson: the experiment validated runner **mechanics** (Skill-tool
invocation, parallel dispatch, evidence-cited surfacing, CWD
fallback — all worked first-try) but **under-measured value**.
Single-shot catch-rate on contrived defects is a lower bound, not a
fair measure. A test that would match operator empirical experience
needs: real skills not contrived ones; signatures that capture
meta-machinery (self-review catches across an editing session,
evolution-cycle outputs, amendment-discipline application);
multi-pass edit sequences not single reviews.

*Observed: 2026-06-05, /eval-skill skill-craft (v1.0.63, first
end-to-end real-input run). Limits flagged post-hoc when operator
pushed back — catch-rate delta read smaller than empirical experience
predicts; the right read is that the experiment was the wrong
measure, not that the framework's value is thin. Contrived input +
signature spec + per-element citation table saved at
`~/.claude/skill-evals/skill-craft/2026-06-05/`.*

---

## 29. Extraction axis is management-vs-core, not length — and it is already latent in VISION's derivation contract

During Phase-3 PROCEDURE.md slimming, an extraction-inventory subagent
classified two checkpoints as EXTRACT-to-references: the **Abstraction
check** (7-test domain-independence) and the **Forcing-functions
dispatch hazard** (temporal keywords express order but do not enforce
it on independently-dispatchable steps). The operator overrode both —
they are **core design method** and stay inline. The subagent had
sorted by length / "specialized-detail / checklist-shape," and under
that lens a 7-test checklist reads as boilerplate and a dispatch
hazard reads as niche orchestration detail.

The correct axis is **management/operational scaffolding vs core design
method**:

- **Management (extractable):** plumbing (directory layout), release /
  activation ops, the *machinery* of running a review (the five
  checks, recovery path, citation format). These trace only to the
  mechanics-delegation boundary — "what skill-craft is not."
- **Core (stays inline regardless of length or checklist-shape):** the
  abstraction check (operationalizes domain-independence, a Layer-2
  principle); the dispatch hazard (the un-fakeable-artifact spine
  applied to ordering); the self-review *mandate* + commit gate.

Proof the axis is real, not convenient: the self-review section
bisected cleanly — *mandate* (core) stayed inline; *machinery*
(management) moved to `references/self-review.md`. Same content area,
split exactly on the axis.

Deeper: this axis is not a new criterion — it is **already implied by
VISION's derivation contract**. Core = traces to a core design
principle in VISION; management = traces only to the "what skill-craft
is not" mechanics boundary. The misclassification happened because the
Procedure-drift Fix's "move specialized guidance to references" is
fuzzy enough to override the derivation trace. Implied procedure
change: point the Procedure-drift Fix at the derivation test (does the
checkpoint trace to a VISION design principle? keep inline. Only to
mechanics/ops? move) instead of the fuzzy "specialized" wording.

Process note: the staged, operator-in-the-loop extraction (inventory →
defer uncertain → operator confirms before executing) caught the
misclassification. Auto-executing the inventory would have wrongly
extracted two core checkpoints. The deferral discipline was
load-bearing.

*Observed: 2026-06-05, Phase-3b PROCEDURE.md extraction; inventory
subagent EXTRACT verdicts on Abstraction-check + Forcing-functions
overridden by operator. Implies a procedure change to the
Procedure-drift Fix (`anti-patterns.md`) — surfaced for decision, not
yet made (Layer 5 "How to surface it": propose, operator decides).*

## Durability classes — skills lack a depreciation model (2026-07-10)

A corpus audit of a heavyweight protocol skill (34 runs of its
on-disk trackers) split its content sharply by lifecycle class: the
enforcement primitives (append-only ledger, isolated
verify-by-real-substrate-execution) carried nearly all the durable
value; the mechanical self-attestation machinery yielded ~2.3%
(a re-confirmation ratchet); the accreted blind-spot lenses were
real but patch-shaped — scar tissue from incidents, each needing a
retirement criterion it didn't have. A mid-session model upgrade
(previous tier → newest tier) showed teaching content depreciating
in real time: the newer model self-applied the discipline the skill
existed to force, while the enforcement/persistence value held
(and the same upgraded model still shipped one silent fail-open
miss — enforcement remains load-bearing even at the top tier).

skill-craft had accretion-quality rules (amendment discipline,
additive reflex, Edit-as-Pareto) and bloat rules (procedure drift)
but no durability classification and no retirement mechanism —
nothing says "a patch that never fires is a cut candidate," and
nothing tells a consolidation pass WHICH content class to cut
first.

*Observed: 2026-07-10, protocol-skill tracker-corpus audit +
model-tier comparison (session forensics). Procedure change made
same day: Layer 4 "Durability classes and pruning order"
(v1.0.66).*
