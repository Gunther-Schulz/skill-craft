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

## Durability at review time + the OBSERVATIONS.md presupposition (2026-07-13)

The durability classes (v1.0.66) were wired only into consolidation
and authoring; a plain review run never asked the existence/expiry
question — a skill made entirely of dead capability patches would
pass all 13 items, because every item audits the quality of what is
there, none whether it should exist. External corroboration: a
practitioner workflow (video, 2026-07) that keeps near-zero skills,
each carrying an explicit deletion condition ("delete once better
models come out"), all bindings to external capability, none
teaching content. Procedure change same day: review-checklist gains
a 14th item, Durability (v1.0.67).

Self-review of that change surfaced a corpus-level gap the diff
faithfully rendered rather than introduced: the source discipline
(PROCEDURE.md Layer 4 "Durability classes", "record provenance in
OBSERVATIONS.md at minting") presupposes an OBSERVATIONS.md exists,
while Layer 4 elsewhere sanctions skills without one (user's choice
at creation). Checklist-level routing clause added ("a patch-bearing
skill without OBSERVATIONS.md fails Evolution first, not here"); the
source discipline still carries the bare presupposition — reconcile
at the next consolidation pass.

*Observed: 2026-07-13, self-review finding N1 on the v1.0.67
change.*

## Voice terminology gap: evidence-voice vs directive-voice unnamed in the corpus

Two steering-text styles kept needing description-by-example in an
operator session (2026-07-26) because no corpus term names them:
**evidence-voice** (an entry states an observed failure shape or fact
and lets judgment weigh it — "live-anchored acceptance criteria have
decayed into false alarms; frozen fixtures stayed re-runnable") vs
**directive-voice** (an entry commands — "always freeze fixtures").
The distinction already EXISTS structurally in multiple homes without
a shared name: an operator maintenance doc's render test ("if an
entry can be obeyed, it is mis-rendered — re-render as the evidence
that justified it"), PROCEDURE.md Layer 2's workflow-vs-judgment
split (gates for sequence, evidence-backed principles for judgment),
writing-by-skill-type's judgment-procedure structure, and the
anti-patterns "adversarial tone" symptom. Each paraphrases the same
axis; none can cite a term. Operator coined the pair mid-session and
asked where it should live — the canonical-term obligation
(Portability discipline (3)) fired with destination (iii) "operator
coins" but no home to persist the coinage into.

Same session, corroborating source: the official "Prompting Claude
Fable 5" doc recommends brief-principle steering over
behavior-enumeration and warns prior-model skills are "often too
prescriptive" — i.e. the style axis is now externally documented and
model-tier-sensitive (stronger models shift the optimum toward
evidence-voice + structural enforcement for the residue; weaker
tiers consuming the same text may still need directive renderings —
the consumer-calibration concern).

Candidate procedure change (next consolidation pass, not
this-session): name the pair once in PROCEDURE.md Layer 2 (likely at
the workflow-vs-judgment split, one sentence each + when-which:
directive-voice for dispatchable sequence and cheap-tier briefs,
evidence-voice for judgment steering of capable tiers), then have
the existing homes cite the term instead of paraphrasing. Also
check: does the Fable-doc's "too prescriptive for newer models"
finding warrant a consumer-calibration line in the durability/
capability-patch discipline (patches written directive may need
re-rendering, not just retirement, as tiers improve)?

*Observed: 2026-07-26, operator session (beat-the-books), coinage
during a corpus-mint discussion; external corroboration
platform.claude.com prompting-claude-fable-5.*

## Deferred (B4, operator GO 2026-07-26): VISION lacks a depreciation/tier dimension

Self-review of the two-registers change found the entire Layer 4
durability branch (capability-patch depreciation, and now the
re-registering axis) architecturally unrooted in VISION.md — the
vision has no model-tier or content-lifetime principle at all
(pre-existing since v1.0.66; tonight's change extends the unrooted
branch). Operator disposition: defer — extend VISION with a
depreciation principle at the next consolidation pass rather than
bundling a second structural change into this diff.

*Observed: 2026-07-26, self-review finding B4 on the two-registers
change.*

## B4 closed (2026-07-26, same day): VISION depreciation principle added

"Content depreciates against a moving reader" added to VISION.md —
roots the Layer 4 durability branch (capability-patch depreciation,
re-registering on tier shifts, binding staleness) that the B4 finding
identified as architecturally unrooted. Derivation now traces:
durable = what enforces (fakeability doesn't shrink with capability);
depreciating = what teaches/compensates; the three durability classes
and the re-registering axis are this principle rendered operational.
Deferred-then-done same day: the defer avoided bundling into the
two-registers diff; VISION is a maintenance file, so no self-review
mandate applied to this edit itself.

*Closes: B4 (self-review of the two-registers change).*

## Proportionality question on the self-review mandate (operator-raised, 2026-07-26)

The alias-deletion change (one line, grep-verified zero operational
consumers) ran the full mandate; the operator asked whether such
changes warrant it. Data point cuts both ways: the review found no
blocking issue (supporting "lighter review would have sufficed") but
its notable — the deletion silently reversed a recorded
keep-as-alias disposition, requiring the supersession stated with new
evidence — is exactly the class a grep cannot catch (it lives in
commit history, not the corpus). Operator lean: no standing
de-minimis rule (misfire risk — "simple" is a fakeable
self-assessment), ad-hoc operator passes instead, per situation; the
14-item checklist skippable for such cases even when the self-review
runs. Watch: if ad-hoc passes recur, mint the observed boundary from
the accumulated cases rather than designing one up front.

*Observed: 2026-07-26, alias-deletion review (0 blocking / 1 notable
/ 1 nit).*

## 2026-07-30 — Cross-home duplication is outside every per-home check

During corpus maintenance (dotfiles operational corpus, governed by
skill-craft as vetting standard): a rule minted into dispatch-discipline
§1 duplicated a sentence already living in §6 — caught only by an
operator-prompted cleanliness pass. The maintenance doc's
neighbor-collision check read the home section's neighbors; the semantic
sibling lived in another section, outside the read radius. skill-craft's
authoring checks (proxy detection, bidirectional trigger) are likewise
per-entry — nothing in the procedure asks "does this statement already
exist elsewhere in the artifact set?". The consumer-side fix landed at
the instance level (maintenance doc: search the governed set for the
concept before minting; hit → amend or source-label). Candidate for the
general procedure: a "search-before-add" step in the drafting checklist
for any multi-file skill/corpus — scope defined per skill as its
governed set. Layer-4 review decides the general form.

During corpus maintenance (2026-07-30, dotfiles operational corpus): a
third sibling for the Skip-rationalization anti-pattern's variant list
— **jurisdiction-appeal**: a verdict cites a REAL, healthy discipline
from the wrong scope, so the rationalization borrows the cited rule's
strength (where corpus-appeal inherits a cited pattern's weakness).
Two same-family instances that day: an extraction (mint-governed)
deferred citing consolidation-timing, which governs compression — one
operator question apart; and, earlier in the corpus's JOURNAL, a
checker's limitation enshrined as doctrine within the hour (rule
justified by what the enforcement could see). The tell is checkable at
disposition time: the cited discipline's own text names a different
act/scope than the one being decided. Consumer-side fixes landed at
the instance level (maintenance doc verdict-jurisdiction bullet; the
operational corpus's costume principle). Candidate for canon: a third
variant under Skip-rationalization beside disposition-echo and
corpus-appeal. Layer-4 review decides the general form.

Self-review of the jurisdiction-appeal mint (2026-07-30) flagged the
third-patch consolidation trigger as arguably met on the
Skip-rationalization family (three structured variants now attached) —
downgraded to watch-item because the cited rule's own text names
checkpoint/caveat additions, not variant entries (the new variant's
Test applied to its own citation). Watch for the next consolidation
pass: restructure as one family intro ("appeal-to-existing without
independent verification") + three compressed moment/mechanism/test
entries; the N1 fix (family framing stated once) is the down payment.

2026-07-30 — Trigger axis independent of register; salience below
ordering. Incident (operational corpus, routing rule): a
judgment-action rule whose firing moment is a recognizable event (an
operator GO over settled work) was rendered pure evidence register
with retrospective tells; a GO-opened implementation burst ran past
it with the rule loaded — the rule's own documented skip-tell,
reproduced with the documentation in context. Diagnosis confirmed by
the operator: (1) register was chosen by action-kind and consumer
tier only — the two-registers rule had no axis for firing shape, so a
moment-anchored trigger inherited the weighable form and the weighing
never happened under momentum; (2) the rule's load-bearing default
sat mid-sentence in a ~90-word enumeration — parsed, not fired:
salience failure below the scope-precedes-default ordering level.
Consumer-side fix landed first (presence-trigger convention at the
GO moment + default split to its own sentence; dotfiles ce79877).
Canon sharpened same day: two-registers gains the trigger axis,
scope-precedes-default gains the salience/flatness case. PROCESS
NOTE for the next Layer-4 pass: these two canon edits shipped
WITHOUT the per-change self-review subagent — operator override,
in-session "anneal in spirit" (checks run in-context, no subagents)
— so the next review cycle re-reviews both edits as unreviewed
deltas.

## 2026-08-05 — Release activation had no mechanical consumer; /reload-skills near-name trap

Incident (coding-clippy releases 0.10.0→0.12.1, beat-the-books
session): `claude plugin update` moved the pin, the operator ran
/reload-skills ("no changes"), and the next Skill invocation served
the session-start version (0.9.97) — caught only because the operator
asked to verify the active version before a run; a first booking
("restart is the only remedy", pinned into a project CLAUDE.md and
relayed from external issue reports about a DIFFERENT failure class)
was falsified the same day by the live test: /reload-plugins
activated 0.12.1 in the same session. §Activation's two-pin model was
correct all along — the knowledge existed, nothing enforced or
announced it, and the operator may not even know a pin moved (another
session can move it).

Minted (v1.1.0): `/release-plugin` command (the §Activation sequence
end-to-end, halting on unbumped versions and unmoved pins);
`hooks/plugin-stale-gate.py` (PreToolUse(Skill) deny when the invoked
skill's own plugin pin moved after the session's last /reload-plugins
marker, else session start — transcript-derived baseline, fail-open,
marker literal split in source so the hook's own text never plants a
phantom reload in transcripts); `hooks/plugin-update-reminder.py`
(PostToolUse(Bash) context line after `claude plugin
update|install`). §Activation gains the /reload-skills-trap paragraph
+ component pointer. Durability: hooks/command are BINDING-class
(valid while the CLI's reload semantics hold, as-of 2026-08-05;
staleness-checked) with enforcement-structure form; the doc paragraph
is canon. Red evidence: fixture red/green suite in each hook
(--test); live red probe planned at release: bump 1.1.1 without
reload → gate must deny, then reload → pass. Firing log starts here.

Firing log, plugin-stale-gate (live, 2026-08-05, releasing session):
RED delivered through the real harness twice — the deliberate 1.1.1
probe (pin 11:44:31 vs baseline 11:43:57, Skill call denied with the
mechanism and fix named) and an unplanned legitimate fire minutes
later (a skill-craft invocation for unrelated corpus work, blocked
until the operator reloaded — the exact incident class, caught on
day one). GREEN after each /reload-plugins (1.1.0 and 1.1.1 probes,
gate silent, base directory correct). plugin-update-reminder fired
live after the 1.1.1 `claude plugin update` (its text landed as
PostToolUse context in the releasing session). §Activation's
"ignore the CLI restart message" claim re-verified twice: hooks and
commands from the new version were live after reload alone.

## 2026-08-05 — Consolidation pass (operator-commissioned backlog clear)

Forward obligations discharged, each against its recorded clause:
- Search-before-add (BACKLOG parked entry): EXIT TRIGGER FIRED — the
  second cross-home incident arrived same-day (repair commits
  violating multi-home discipline dominated both coding-clippy
  render-vet findings tables, 2026-08-05). MINTED into PROCEDURE.md
  Layer 4 multi-file corpora: governed set named + search-before-add
  scan as placement basis + repairs get the same scan. BACKLOG
  entry closed by this commit's ref; file now empty by design.
- Voice/register terminology (:1024): CLOSED-ALREADY-SATISFIED —
  "The two registers" (Layer 2 Authoring discipline, minted
  2026-07-30) names the pair; obligation predates it.
- Durability cut-candidate gap (:970): CLOSED-ALREADY-SATISFIED —
  the durability-classes text carries "a patch with no logged firing
  since the last consolidation pass is a cut candidate".
- OBSERVATIONS presupposition (:998): RECONCILED — capability-patch
  bullet now states the requirement explicitly and points at the
  Evolution check as its enforcer.
- Skip-family restructure (:1151 watch): DONE — family intro minted
  ("appeal-to-existing"), per-variant sibling cross-references
  removed (carried by the intro); variants kept compact rather than
  rewritten (content-preserving Pareto).
- The two unreviewed 2026-07-30 canon deltas (:1160 process note):
  re-review is IN THIS PASS's self-review brief, explicitly.
Remaining journal-resident watch (not a backlog item): self-review
proportionality (:1097) — unchanged, watch-kind unchanged.

Self-review round 2 (2026-08-05, opus, consolidation pass): 4
blocking all fixed pre-commit — B1 OBSERVATIONS-requirement
duplicated across two homes in the commit minting the
anti-duplication rule (parenthetical dropped; checklist owns the
routing); B2 the cited Evolution enforcer lacked the patch-bearing
predicate (widened — this also cures the pre-existing corpus-appeal
in review-checklist:83); B3 the permissive no-journal default kept
its carve-out 120 lines downstream (carve-out now at the default);
B4 the family restructure had shipped only its additive half (three
variants compressed to moment/mechanism/test; net-subtractive now).
Notables applied: governed-set placement half restored
(declaration in the governance doc; skill-craft's own set declared
in repo CLAUDE.md; fallback = whole payload), scan requirement its
own sentence, trigger-axis carve-out carried inline at the Layer-2
lead, salience case gains its own test + the checklist Salience
item gains the flatness half, residual contrast clauses cut with
the compression, coinage related to Terminology (2) inline.
Derivation marking (reviewer n1): the incident evidence
(cross-home propagation-miss, the duplication mirror) squarely
grounds the repairs-clause; the governed-set + placement-basis
clauses are DERIVED from the un-fakeable-artifact principle (the
scan is the artifact), stated here rather than claimed
incident-grounded. Accepted (n2): no new checklist item for
search-before-add — the review-time consumer is self-review check
3's cross-reference enumeration (near-duplicate function; a
parallel item would be the additive reflex). Version: 1.1.2 per
observed canon-mint practice (patch bumps), not 1.2.0.
The two owed 2026-07-30 deltas re-reviewed: findings N3/N4 above,
both fixed — re-review debt cleared.

---

## 2026-08-05 — The stale-pin deny was a wall for the party that cannot reload

Live incident (same day as the gate's own mint, v1.1.0): skill-craft's
pin moved 13:20:08Z mid-day (installed_plugins.json lastUpdated), and a
RUNNING fable subagent then had its Skill(skill-craft) load denied by
the gate. The deny's named remedy — /reload-plugins — is an
operator-only slash command: no subagent can ever satisfy it, and the
subagent has no channel to ask for one mid-flight. The agent worked
around the wall by reading the mirror source by hand, which is the
right outcome arrived at the expensive way.

The gate's predicate was correct; only its RENDERING was wrong for
that audience. A blocking gate whose remedy the blocked party cannot
perform stops being a signal and becomes an obstacle to route around —
and routing around a gate is the behavior that erodes every other gate
in the set. Downgrade decided and operator-ratified 2026-08-05
(v1.1.3): in a subagent context (payload carries a non-empty
`agent_id` — the same detection dispatch-guards uses, replicated as a
one-line predicate rather than imported, for self-containment) the
same predicate emits a non-blocking PreToolUse `additionalContext`
advisory: the load proceeds on the baseline copy, and the advisory
names the pin's CURRENT `installPath` so the agent can read the newer
released source directly — the one remedy that is actually available
to it — and say so in its report. Main sessions still deny; there the
remedy is one keystroke away.

General shape, worth carrying beyond this hook: **a gate's audience
determines whether deny is a legitimate verdict.** Before writing a
block, ask who receives it and whether that party can perform the
remedy named in the text. Where it cannot, the honest rendering is an
advisory that names the remedy the receiver DOES have.

Firing expectation (this is what the log should show next): the
advisory fires on the next mid-day pin move observed in any subagent
context, and the deny keeps firing for main sessions. Red evidence:
main()-level fixture cases in `--test` — subagent + stale pin emits
additionalContext with the installPath and no permissionDecision;
same payload without agent_id denies byte-identically to v1.1.2;
subagent + fresh pin stays silent — plus a live stdin smoke through
the real installed_plugins.json reproducing the 13:20:08 incident
payload.

---

## 2026-08-05 — plugin-stale-gate: the deny retired entirely (v1.2.0)

The v1.1.3 entry above ends on a firing expectation that is now
withdrawn: *"the deny keeps firing for main sessions."* It rested on
an unprobed premise — that only a deny reaches the operator, so a
main-session warn would be silent to them while letting stale rule
text into context unread. The operator challenged the premise
directly ("a stale skill is better than none; it's mainly supposed to
remind me to run /reload-plugins"), and the probe killed it.

**Measurement (live, three variants in one session).** A temporary
patch to the installed cache copy emitted, on the ALLOW path, for
three consecutive `Skill(ref)` calls: (A) bare `systemMessage`, no
`hookSpecificOutput` at all; (B) `systemMessage` +
`additionalContext`; (C) `systemMessage` + `permissionDecision:
"allow"`. All three rendered to the operator, under the identical
`PreToolUse:Skill says:` line the deny had been using, and all three
Skill loads succeeded. Positive control: B's `additionalContext`
reached the model, proving the harness ran the hook and parsed its
JSON rather than discarding it — the absence in the other variants
would otherwise have been an unfalsifiable non-event. Scratchpad log
recorded each emitted payload verbatim; cache copy restored
byte-identical (md5 `6f0e05f3cb44`) after.

So `systemMessage` renders on the allow path unconditionally. **The
deny bought exactly zero operator attention** over a warn, and paid
for it by withholding the skill.

**The lesson, one level up from the v1.1.3 one.** That entry got the
receiver question right (*who receives the block, and can they
perform the remedy?*) and the channel question wrong. Both halves
matter: a deny is a legitimate verdict only when blocking is what
achieves the effect — and where a non-blocking channel reaches the
same receiver with the same words, the block is pure cost. Ask what
the deny BUYS over a warn on the same channel, and probe the channel
before assuming the answer.

Corroborating evidence the block was never doing the work: twice
observed, an unwanted block produced a workaround rather than the
named remedy — a fable subagent read the mirror source by hand, and a
main session opened a design conversation instead of typing
/reload-plugins.

Minted (v1.2.0): one rendering for both contexts, `agent_id` branch
deleted along with `deny()`/`advise()`/`advisory_text()`. Two
channels, two audiences: `systemMessage` → operator (pin moved,
/reload-plugins re-reads it, /reload-skills does not, the load
PROCEEDS); `additionalContext` → model (this load is the baseline
copy, current source at `<installPath>/skills/`, read it if the delta
plausibly matters). Predicate and fail-open semantics untouched.

Red evidence: the new invariant — *no output path may carry
`permissionDecision`* — asserted against the pre-change
implementation, which emitted `permissionDecision: deny` for a main
session (old code, new expectation; the existing battery stayed green
alongside, so old-against-old would have passed vacuously). Bite: the
deny re-injected into `warn()`, `--test` failed at the invariant
assertion, injection removed, green.

Deliberately NOT fixed: the pin moves at PLUGIN granularity while
staleness matters at SKILL granularity, so a hook-only release still
warns about an unrelated skill. Under a deny that cost a blocked
skill; under a warn it costs one line, which does not justify the
SessionStart install-path snapshot a content-level comparison needs.
Reopen only if the warn proves noisy in the firing log.

Firing expectation (what the log should show next): the warn fires on
the next mid-day pin move in ANY context, no Skill call is ever
blocked by this hook again, and the operator's next /reload-plugins
follows the warn rather than a wall.

## 2026-08-06 — Contact transfer: a read skill's format steered behavior without invocation

During the mattpocock/skills comparison session, the assistant read
his `grilling` skill (22 lines) among ~10 others. Roughly a hundred
turns later, presenting design questions for the 2.0.0 plan, it
reproduced that skill's round format unprompted — the ❓/➡️ glyphs,
batched rounds, and the word "frontier" — without deciding to adopt
it, and flagged the leak only when the operator asked. The
recommendation-beside-question SUBSTANCE was already operator-corpus
doctrine; what transferred was the FORM, carried by one
prior-recruiting term ("frontier", from search algorithms).

Two readings, both actionable:
- Corroborates the Tier 2 arm-contamination check (evaluation.md):
  merely reading a skill contaminates behavior; a control arm in a
  session that has read the candidate is not a control.
- Strongest cheap evidence a format can show for adoption value —
  transfer on contact, no enforcement. Feeds PLAN.md Harvest B item
  3 (term selection recruits priors) and the parked grilling-variant
  BACKLOG item.

## 2026-08-06 — 2.0.0 rewrite charter persisted

PLAN.md created (statiker pattern: core settled in dialogue, plan is
the carrier, canon written from scratch next session). Basis
recorded there — architecture + missing economics half, explicitly
NOT staleness: the July annealing (two registers, durability
classes, consumer calibration) is current and harvest-rich. Credit:
Harvest list B adapts from mattpocock/skills (MIT),
github.com/mattpocock/skills — writing-for-agents,
SKILL-MECHANICS, grilling.

## 2026-08-06 — 2.0.0 canon written (from-scratch rewrite per PLAN.md)

- Canon rewritten as a single-body SKILL.md; PROCEDURE.md retired —
  the SKILL→PROCEDURE chain was one extra hop every invocation that
  the disclosure ladder no longer justifies (successor-shape
  latitude in the write brief; PLAN names the files being replaced,
  not a mandated split). References: enforcement.md (new — the
  tier-conditional instrument toolbox), anti-patterns.md,
  evaluation.md, review-checklist.md (de-gated to review
  questions), self-review.md, writing-by-skill-type.md
  (density-calibration and Migration content moved into SKILL.md
  Two parties / era re-grade), plugin-engineering.md (light touch).
  dev-notes/VISION.md deleted (PLAN Q2); surviving content absorbed
  into the birth declaration, Enforcement, and Lifecycle.
- Suspect-at-intake verdicts (PLAN Harvest A): blocking logic as
  default rendering — OUT, re-entered tier-conditional in
  enforcement.md; word-count budgets as stated — OUT, replaced by
  the two-loads ladder ("size each by what it costs where it
  sits"); consolidated load-gate boilerplate — survives once as the
  named "load gate" convention, below-trust-tier only, skill-craft
  itself drops it; five-layer frame — OUT, spine organization
  (parties / economics / registers / enforcement / architecture /
  lifecycle / evaluation); "every sentence must change behavior" —
  survives re-founded as the model-relative no-op test.
- Harvest B landed: pointer economics; invocation choice (with
  measured basis, below); term selection sharpened (criterion: the
  clearest term of its domain from canonical literature;
  verification: cold probe; anti-target: operator echo; coined
  tokens stay for machine-read vocabulary); era re-grade widened
  into durability + no-op test, not duplicated; positive rendering
  (marked hypothesis, registers); completion-criteria demand
  wording + environment-as-source-of-truth (marked hypothesis /
  pruning).
- New Path-1 anti-pattern: Overweight description. Provenance:
  fleet descriptions observed overweight 2026-08-06 —
  integration-shakedown ~180 words; statiker's forcing-point
  summary buying zero triggering on an explicit-invoke skill.
- Tier-1 measurements (dev-notes/eval-skill-craft/2026-08-06/
  result.md): prose invocation 12/12 listed → 0/12 delisted —
  settles PLAN's open question against a description-flip for
  prose-invoked skills; new 2.0.0 description 18/18 should-trigger,
  12/12 near-miss clean, ships unrepaired.
- Fire-born baseline for 2.0.0 self-machinery: carried mechanical
  set only (eval runner, release/stale-pin hooks, pre-commit
  self-review dispatch); no new gates minted at birth. The firing
  log for future capability patches starts at this entry.

Self-review round (fable, fresh context, pre-commit): 1 blocking,
4 notable, 4 nit; PLAN conformance confirmed — no settled decision
missing, contradicted, or silently bridged. Dispositions: B1
(undefined "no-theater" in self-review.md candidate set) fixed —
token dropped; N1 (operator phrase "the clearest term of its
domain" carried verbatim against PLAN's not-this-sentence
instruction — the rule's own anti-target) fixed — criterion
reworded; N2 (environment-as-truth unmarked hypothesis) fixed —
marker added; N3/N4 (stale eval-skill.md example + dangling
citation) fixed — dependent repair, not infrastructure redesign;
n1 (anchor), n2 (description-mood rule aligned to the
Tier-1-proven what-plus-when form, both homes), n4 (Load-when
header) fixed; n3 split — the ×3 "seed, not bound" duplication
reduced to two role-distinct homes, the "inspection is not
measurement" double kept with rationale (evaluation.md has a
standalone consumer via /eval-skill; commit body carries the
Accepted-finding line). Mechanism firing note: the self-review
dispatch caught a real defect class the writer was blind to
(operator-echo in the very rule that forbids it) — counts as a
firing for the mechanism's own retention log. Recursion check
(repo CLAUDE.md): the reviewer did not self-validate — it returned
9 findings; each re-read against the cited line before fixing.

## 2026-08-06 — Guard-lifecycle doctrine minted (operator GO, dotfiles BACKLOG "READY 2026-08-06 — guard-lifecycle adoption")

Path 1; incident provenance: midturn incident 2026-08-05 (synthetic
fixture blindness + frozen corpus scoring a dead detector as
passing), recorded in the dotfiles backlog entry — the binding
decision record.

- Minted: `references/enforcement.md` "Guard lifecycle (shipped
  hooks)" — deny-arm fixtures on recorded real payloads (both traps
  carried verbatim), warn-first with logged fires, deny on measured
  rates, replay audit with re-capture bound to harness versions;
  plus the two-reader report line (prose + schema-validated
  structured tail). Existing instance of the two-reader pattern:
  statiker's tag-first tracker lines. SKILL.md toolbox enumeration
  gains "the guard lifecycle for shipped hooks" — pointer only.
- Placement basis (search-before-add over the governed set):
  `grep -rni "hook|guard|warn|deny|fixture|lifecycle"` over
  SKILL.md + references/*.md — zero doctrinal coverage; all hits
  incidental (packaging mechanics in plugin-engineering, the
  era-regrade's precipitation clause). Gap → minimum novel content.
- Home deviation, named: the backlog entry expected the
  plugin-engineering reference; the follow-up brief set the
  enforcement reference as expected home with placement judgment
  against the canon's ladder. Basis: plugin-engineering is
  packaging bindings; the lifecycle is enforcement-instrument
  doctrine — it sits with the instruments it governs.
- Out of scope, homed elsewhere per the decision record: hookbench
  + warn-runner (dotfiles), schema-tail validator + writer lock
  (dispatch-guards), PermissionRequest seam (stamped re-open
  condition in the backlog; build nothing).
- Self-referential residue (reviewer NIT-8): skill-craft's own
  shipped hooks now sit inside the class convention with no
  recorded-real fixture corpus yet; the fleet measurement is homed
  in hookbench (dotfiles decision record), not here.

Self-review round 2 (fable, fresh context, guard-lifecycle
amendment): 1 blocking, 3 notable, 5 nit. B1 (incident tag inline
in canon) fixed — parenthetical deleted; the trap clause stays
verbatim, the dated provenance lives in this entry (deviation from
a literal reading of the follow-up brief's "carry verbatim",
surfaced to the operator at booking). N2 (home deviation) and N4
(report-pattern line beyond the backlog's canon clause) accepted —
both decided by the operator's follow-up brief, recorded above; N3
(timing "AFTER 2.0.0 lands") accepted — the follow-up brief itself
commissioned the amendment against the committed 2.0.0-dev
rewrite. NIT-6 fixed (one term, "guard", after the title's
equation); NIT-5/7 no action (reviewer's own rule-outs); NIT-8 the
line above; NIT-9 verified in-session (statiker SKILL.md tag-first
entry format read directly this session). Reviewer also caught the
dispatch brief's stale line citation for the backlog entry — a
live co-writer shifted the dotfiles backlog between my read and
the reviewer's; located by title grep, content matched.

## 2026-08-06 — Render-time term-provenance (operator GO'd corpus change; Layer-5 observation)

The canon's portability/abstraction checks anchor at PROPOSAL time
(the rule idea); the observed leak class happens at RENDER time —
the final text's noun phrases import session vocabulary even when
the concept passed its abstraction probe. Motivating incident: the
falsification-escalation mint leaked "intent/mechanical passes",
"clippy", and "money path" into the operator corpus; caught by the
operator post-push (dotfiles JOURNAL 2026-07-31 ADDENDUM), repaired
by re-rendering against existing corpus instruments. Candidate
canon change: a term-provenance step over the FINAL render — every
noun phrase sources from (a) the target corpus's own vocabulary,
(b) domain literature, or (c) session context, and (c) is the leak
signal. The consuming corpus (dotfiles CLAUDE-maintenance.md,
skill-craft-vetting bullet) now states this for itself, 2026-08-06;
this observation proposes the general form for the canon. Operator
decides at the next canon pass.

## 2026-08-06 — Cross-repo experiment booking: opus pre-release review of skill edits (statiker trial)

The statiker repo pre-registered an experiment bearing on this
canon's review posture (statiker CLAUDE.md trial conventions +
dev-notes/OBSERVATIONS.md, 2026-08-06): the next three statiker
SKILL.md releases each get ONE fresh-context opus review before
the pin moves (brief = diff + full skill + question, no author
reasoning; findings dispositioned pre-release). Pre-registered
criterion: SUSTAINS if ≥1 of 3 reviews yields a substantive
change to shipped text (structural/provenance/reach/register, not
wording); else RETIRES to stabilization-only review. Evidence
motivating it (operator-relayed, labeled unverified in the
statiker ledger): opus arm out-bit fable arm in the statiker
attack ladder rounds 1-3 (byte-identical artifacts, n=4, one
domain); an opus vet catching a blocking factual defect in
hours-old top-tier text. CANON RELEVANCE if it sustains: the
mandatory fresh-context pre-commit review dispatch currently binds
only skill-craft's own files, while other skills get a
same-session checklist pass ("Reviewing a skill"); a sustained
result grounds widening the dispatch form (tier-insensitive per
the self-review reference's own doctrine, so a cheaper tier
carries it) to skills under active development generally — a
Path-1 amendment with the three review reports as provenance.
NO canon change now: zero rounds run; unmarked-guess path
otherwise. Consumer: the next canon pass, and the statiker meta
session's grading entry at the third release (statiker
dev-notes) — read both before amending.

- 2026-08-07 — **Proposed widening (operator-raised, statiker meta
  session; incident provenance in statiker dev-notes, reviews
  12/T3 → draft-attack-2/I1): the Architecture rule's
  operational/maintenance split binds at FILE grain only; the
  observed leak is CLAUSE grain.** Incident: a reviewer flagged an
  operational rule resting on an unversioned external fact
  (another plugin's grep patterns); the author repaired it by
  dating the fact IN the skill text ("verified against its source
  as of <date> — re-check on change") — maintenance metadata
  addressed to the maintainer, a no-op for the executing consumer,
  costing context every load. Two existing rules each half-cover
  it (file-level split; no-op test) and neither fired at write
  time, because the trigger moment is specific: a provenance
  demand arriving as a review finding invites answering in the
  wrong home. Proposed one-sentence widening of the Architecture
  "Operational vs maintenance files" rule: the split binds inside
  files too — freshness stamps, verification dates, and re-check
  triggers address the maintainer and go to the journal or a
  mechanized check; operational text keeps only the rationale the
  consumer needs. Canon edit owed via the normal pass
  (self-review gate); this entry is the observation, not the
  patch. Consumer: the next skill-craft canon pass.

- 2026-08-08 — **Observation (operator challenge, statiker meta
  session): skill-craft did not catch prose-held machine semantics
  accreting across repair rounds** (~600 of statiker SKILL.md's
  1032 operational lines; blocker series 5→7→7 concentrated in each
  round's newest text; resolved by the operator accepting an
  executable-spec form change — statiker dev-notes 2026-08-08).
  Triage against skill-craft's own failure classes: NOT a gap — the
  Enforcement section already holds the principle (must-hold rules
  belong in mechanisms, not prose; mitigation preference order).
  LOADED-BUT-INERT: skill-craft was invoked before every SKILL.md
  edit (statiker's hook enforces it), but during attack-repair laps
  it discharges as an edit-gate while the acting frame is the
  attack round's correctness brief — the attackers grade the
  semantics' correctness, never the MEDIUM, and skill-craft's
  structural question is never re-asked under repair momentum. The
  catch that eventually worked was corpus-level (the re-entry-seam
  trend rule + a pre-registered stop criterion, both minted
  2026-08-07 from this same incident) — so the general lesson sits
  at its truth level already. Proposed minimal change (trigger, not
  content, per iterative narrowing): at a repair-lap re-entry on a
  skill's own text — or on a growth burst in one section — the
  review re-asks the Enforcement section's medium question: which
  of the text under repair is must-hold semantics that belongs in a
  mechanism? Computable tripwire candidate: successive repair
  rounds whose findings concentrate in the newest text. Scope
  note: the operator's wider overbuild challenge had three parts;
  only this one is skill-craft's jurisdiction — meta-to-object
  ratio and batch accretion are economy questions (corpus). One
  incident as provenance; operator decides whether it becomes a
  checklist item.**

- 2026-08-08 — **MINT (operator GO, statiker meta session): the
  prose-held machine-semantics observation above lands as a
  widening of review-checklist item 10** — the medium question
  (which of the text is must-hold machine semantics belonging in an
  executable spec + battery, prose keeping principles), asked over
  the body and re-asked at repair-lap re-entry and on a
  section growth burst; tripwire: successive repair rounds whose
  findings concentrate in each round's newest text. Placement
  basis: grep "must-hold|belongs in a mechanism|medium" over the
  governed set — principle homes at SKILL.md:178 (registers) and
  the Enforcement section; the review instrument (checklist item
  10) was the home that failed to fire, so the trigger lands
  there, citing the principle rather than restating it. Fire log
  opens with the founding incident (statiker, 5→7→7). Consumer:
  every checklist-driven review; next consolidation pass grades
  the patch.**

- 2026-08-08 — **Self-review recovery on the item-10 mint (fresh
  opus review, 3B/4N/2n): the mint entry's premise "the review
  instrument was the home that failed to fire" was DISPROVEN (B3:
  review-checklist.md is a disclosed reference the repair-lap
  frame never loads — grep over statiker dev-notes shows zero
  review-checklist mentions, instrument proven live on a known
  positive first). Recovery landed: trigger relocated to SKILL.md
  "Reviewing a skill" (hook-loaded on every edit) as one abstract
  clause — item 10's medium question owed again whenever a section
  has grown since its medium was last decided — and item 10
  compressed to the question + citation form (B1 enumeration →
  abstraction; B2 sub-shapes and motivation dropped; N2 restates →
  cites The two registers; N3a tripwire marked hypothesis,
  validate by use; N3b outward journal pointer dropped — operator
  decision, mid-turn, same session: provenance pointers do not
  belong in operational skill text, which also confirms the
  2026-08-07 clause-grain proposal's direction; n1/n2 resolved by
  the compression and question shape). DEFERRED (N4): "executable
  spec + battery" as a named instrument form in enforcement.md —
  the corpus currently gives a YES answer to the medium question
  no construction recipe; candidate addition at the next
  enforcement.md pass, provenance: statiker's executable-spec form
  change. Planted-test note: the operator withheld the N3b defect
  deliberately to test whether the self-review catches it; it did,
  from three angles (N3b, check-3 refs 5 and 7). Consumer: the
  commit's disposition record; the next enforcement.md pass (N4).**

- 2026-08-08 — **skill-lint landed (the READY item; opus build
  baf064a + desk integration). Red-first proven: planted cases
  fire all four checks, whitelists proven live on would-have-fired
  lines, --fix and --diff-base proven against positive controls.
  The backlog's booked RED TARGET was refuted by measurement (G1:
  0aa1891 carries zero rewrappable over-72 lines — the sha was
  booked from reviewer recollection, not from a measurement at the
  sha; lesson, corpus-grade: a red target booked by sha is worth
  what a measurement at that sha proves). Red run re-pinned to
  40bcc73 (review-8 repairs), measured red independently by arm
  and desk (83/79-col prose at lines 134/310). The GREEN premise
  was refuted too (G2): statiker SKILL.md at aaf2327 carries two
  real 73/75-col lines — the limit stays 72, the defects are
  real, fixed in the statiker working copy by the desk.
  Dispositions: G3 whitelist widening ACCEPTED (frontmatter,
  fenced code, table rows, longest-token predicate — the generic
  predicate replacing enumeration); G4 backticked-only singleton
  ACCEPTED; G5 → desk integration added bold run-in labels as
  cite targets and headings as an unbreakable wrap class, planted
  red re-proven after each; G6 was the desk's own BACKLOG edit,
  no foreign writer. Desk follow-through: 14 genuine wrap lines
  across skill-craft's own files rewrapped; all 8 operational
  files now blocking=0 (61 singleton warns stand, usefulness
  unmeasured — the arm's honest residue). Arm lessons, kept: run
  a new checker over its own wiring commit before it lands; keep
  false-fire classes as the check's regression set; a zero from a
  suppression flag is indistinguishable from a dead flag without
  a positive control. Consumer: /release-plugin executions (the
  new step 3); the next consolidation pass.**

- 2026-08-08 — **Batch review (fresh opus, 1B/4N/3n over the full
  change-set) RECOVERED; change-set closed. Dispositions: B1 fixed
  (tripwire split into its own sentence — the salience rule item 7
  itself enforces; clears n1's scope ambiguity); N1 fixed (cite by
  name, not renumbering-fragile ordinal); N2 fixed (question's
  one-clause form inlined at the SKILL.md trigger — the failing
  frame provably never follows disclosed pointers); N3 fixed (the
  answering measurement named in item 10: the machine-semantics
  line-share count — recorded as DISTINCT from deferred N4, which
  keeps the construction recipe for the next enforcement.md pass;
  two halves, not one deferral); N4 fixed (the after-the-pass line
  gains the third exit: a change of medium); n2 fixed (always-true
  qualifier swapped for "since its last review"); n3 stands as a
  booked open question (release-plugin step-3 path resolution is
  prose by dispatcher decision — ${CLAUDE_PLUGIN_ROOT} support in
  command files unverified, outside the governed set). Mechanical
  layers verified by the reviewer with positive controls: rewraps
  content-neutral by word-diff, planted red byte-identical under
  committed and refined checkers, refinements suppress exactly the
  two known false-fire classes. Consumer: this change-set's
  commit; the next enforcement.md pass (N4-deferred).**

- 2026-08-08 (dispatch-guards 0.7.1 release, skill-lint step): the
  dead-cite check false-fires on a TOOL-NAME parenthetical —
  forms.md:29 "(SendMessage)" is the harness tool, not a section
  cite, yet it blocks (exit 1). Over-firing-check class: the
  heuristic reads any parenthesized CamelCase token as a cite.
  Dispositioned ACCEPTED at that release (bytes identical to the
  already-released 0.7.0). Candidate repair: a declared-exemption
  list of known tool names, or requiring a §/heading-like shape
  before a parenthetical counts as a cite. Consumer: the next
  skill-lint pass over its heuristics.

## 2026-08-09 — the no-op test's sentence unit rewards packing

Observed in the operator's rule corpus (measured before its
modularization): median sentence 33 words, p90 64, max 148 — every
sentence individually defensible under the no-op test because
deleting any changes behavior, while single clauses inside them
would fail individually. The sentence-unit test is the mechanism:
an author optimizing against it merges rule + qualifier +
rationale + cross-reference into one unit that always passes
whole. Change landed same-session (operator GO): the test's unit
is now the CLAUSE (SKILL.md, The no-op test), checklist item 6
grades clause-by-clause with a packed-sentence unpacking step,
anti-patterns' fix line follows. Firing log starts here.

## 2026-08-09 — era-re-grade cites Tier 2 as the no-op instrument; evaluation.md never carries the test

Surfaced by the clause-unit self-review (disposition:
defer-to-observations, operator GO). SKILL.md's era re-grade names
"Tier 2 of references/evaluation.md" as the instrument for
re-running the no-op test, but evaluation.md contains no reference
to the no-op test (grep: zero hits) and Tier 2 measures a
with/without behavioural delta, not per-unit deletion. Either the
citation should name what Tier 2 actually provides (a
behaviour-delta floor under re-graded content) or evaluation.md
owes a no-op protocol. Reconcile at the next consolidation.

Reconciled (2.2.0 canon pass, 2026-08-20): the ablation arm landed
in evaluation.md Tier 2 (the no-op test at document scale), and the
era re-grade's citation now names it as the instrument.

## 2026-08-10 — the trigger-anchor clause is missing two tests: an observable referent, and visible absence

Provenance: a corpus rule in the operator's dotfiles (the
learning-question's second firing moment, calibration module) was
measured inert on a day its trigger condition was met seven times —
zero unprompted firings — and the derivation (dotfiles JOURNAL
2026-08-10; brief docs/directives/post-incident-self-firing-brief-
2026-08-10.md) located the failure UPSTREAM of register. The rule
was nominally anchored at a named moment ("whenever the correction
list grows"), satisfying the trigger-axis clause as written
(SKILL.md, The two registers: "Anchor the trigger at its named
moment (a convention or a gate)"), and still could not fire. Two
mechanisms the clause does not name:

1. REFERENT: the named moment must be an event something
   observably PRODUCES — an act performed, an artifact written.
   "When the list grows" anchored to a list nothing keeps carries
   an anchor's syntax without an anchor.
2. VISIBLE ABSENCE: a convention fixes the under-binding only when
   compliance leaves an artifact whose omission is visible in the
   output (the corpus's route/gauge/closing lines all work this
   way — presence lines). An anchored trigger whose compliance is
   a purely mental act decays silently: nothing distinguishes
   fired from skipped.

Proposed change (operator decides): extend the clause's fix
sentence with both tests. The repair that fixed the motivating
rule was exactly their application: bind the obligation to an act
that provably already happens (the correction's record being
written) and make the answers slots in that record, so a skipped
firing is visible in the artifact itself.

Minted (2.2.0 canon pass, 2026-08-20): both tests appended to the
trigger-anchor clause (SKILL.md, The two registers).

## 2026-08-10 — lever application sweep: where "needs a named moment" applies to this canon itself

Follow-up to the trigger-anchor observation above (same provenance
chain), operator-prompted: sweep this canon for rules that name a
firing moment whose referent nothing produces, or whose compliance
leaves no artifact. Instrument: full read of SKILL.md plus a
moment-language grep over references
(`whenever|owed|re-grade|re-measure|re-review|before ...`), hits
graded individually. Most obligations pass — mechanically enforced
(pre-commit self-review dispatch, eval runner, release and
stale-pin hooks) or artifact-producing by form (placement scans
recorded, findings per checklist item, firing logs, hypothesis
markers, observation writes). Three findings:

1. **The medium re-ask** (Reviewing a skill): "owed again whenever
   a section has grown since its last review" — growth-since has
   no referent (reviews leave no durable mark to measure against)
   and the re-ask leaves no artifact; the clause even self-labels
   hypothesis. Lever: reviews record their mark (a commit ref in
   the journal or the checklist output), and the review record
   carries the medium verdict for each section grown since the
   previous mark — the owed re-ask becomes readable from the
   record instead of remembered.
2. **The era re-grade trigger** (Lifecycle; checklist item 13):
   "when the consuming model moves a tier or a generation" and "a
   consumer-tier move since minting" have no recorded baseline —
   the consumer declaration names a tier or range but not the era
   it was graded against. Lever, small: the consumer declaration
   carries an as-of stamp (model/era at last grading), turning the
   re-grade trigger into a diffable staleness check — the stamp
   discipline this canon already prescribes for bindings, applied
   to its own declaration.
3. Minor: "Re-measure before flipping any prose-invoked skill"
   (Invocation choice) demands a measurement whose absence is
   invisible; if kept prose, the flip commit names its
   measurement.

Correctly un-anchorable, no change proposed: the noticing-class
moments (Reflexivity's "a gap noticed") — noticing has no
observable producer, and their design already defines the output
once noticing occurs, which is the right shape; anchoring noticing
itself would reproduce the defect the lever repairs.

Minted (2.2.0 canon pass, 2026-08-20): review mark (Reviewing a
skill + checklist close), era stamp (The two parties; era re-grade
and item 13 diff against it; own declaration stamped), flip-commit
measurement line (Invocation choice).

## 2026-08-10 — third lever entry: the unbound definite reference (object-side sibling of the named-moment gap)

Same provenance chain, operator-prompted full-corpus review. The
named-moment gap was a TRIGGER with no referent — the rule never
fires. This class is its object-side sibling: the rule fires, but
its object is "the X" where the consumer's environment offers
several Xs and the wording is satisfied by any of them — the act
lands on a sibling object and reads as compliance. Incident today:
"the check is against the record" was satisfied by an incident
record while the work item evaporated (caught by the operator, not
the rule). The reviewed corpus shows this is a RECURRING class
with an established fix pattern — several of its most load-bearing
rules exist precisely because a wrong referent once satisfied
their older wording: "the verifier's output is what the check
itself wrote, never an intermediary's exit status"; "a document
about the artifact is not its definition"; "the provenance note
hangs on the claim, not the section" (same-day peer fix). The fix
each time: bind to the invariant object, never to a container,
section, or label that usually coincides with it.

Proposed change (operator decides; work item in BACKLOG.md): an
UNBOUND-REFERENCE TEST beside the no-op test — every load-bearing
definite reference ("the record", "the list", "the test", "the
source") either has a unique in-scope referent or names its
selector; the tell is a definite article over a noun with siblings
in the consumer's environment; the fix binds to the invariant
object. Plus one review-checklist item carrying the same test.
Instrument note from the review: a hot-noun grep (the
record|list|test|check|source|baseline|output|log|file) surfaces
candidates cheaply; grading stays judgment.

Minted (2.2.0 canon pass, 2026-08-20): the unbound-reference test
beside the no-op test with the three-site fold (trigger, object,
scope); checklist item 18 with the hot-noun grep.

## 2026-08-10 — a plugin released MID-WAVE is invisible to every running session, including the dispatcher's own

Measured in a dotfiles drain wave. A dispatcher released
dispatch-guards 0.10.14 (`f80fd4f`) while its own wave was still
running, then dispatched further agents. One executor loaded the
executor skill at **0.10.13** while the pin on disk already read
0.10.14, and flagged the mismatch in its `(h)` slot instead of
reporting a clean read. Nothing else would have surfaced it: a
skill carries no version in its own prose, so the old copy and the
new one read as the same file.

The gap is a REACH gap in an existing mechanism, not a missing one.
The stale-pin gate fires on the operator's next Skill call in a
session that has not reloaded — it says nothing about a SUBAGENT
spawned from such a session, and the subagent inherits the
dispatcher's already-resolved path. So the one party who cannot see
the staleness is the one who caused it.

The computable half does not exist: "is this session serving the
current pin?" is not answerable from inside the session, which is
the whole defect. What is left is a procedure step, and it belongs
where the release happens rather than where the dispatch happens —
the release is the act that opens the window.

Minted (v2.1.3): `/release-plugin` step 8, a DISPATCH FREEZE between
"pin moved" (step 7) and the operator's `/reload-plugins` handoff
(now step 9). Until the reload, no further dispatches — or the brief
states the served version explicitly, so the executor can report the
mismatch from its own `(h)` slot, which is exactly how this incident
was caught. Renumbering checked against dependents: the only
step-number citation anywhere in the three repos is to step 3
(OBSERVATIONS.md:1744), which does not move.

## 2026-08-11 — gap: plugin BIRTH is uncovered between creation guidance and /release-plugin

Observed at the birth of `begehung` (operator requirement stated in
the incident: "after a skill build or change, everything should be
converged so that /reload-plugins is my only remaining act").
Skill-craft covers creation (design/review/eval) and RELEASE
(/release-plugin: bump, push, marketplace update, reload handoff) —
but the FIRST activation of a newborn plugin is named nowhere:
marketplace add, plugin install, and the environment's
plugin-management convergence (on this fleet: dotfiles mirror pins +
repo adoption + doctor roster check) were each discovered by hand,
and the operator had to ask for the convergence afterward. Proposal
(operator decides; reflexivity rule): plugin-engineering.md or
/release-plugin gains a birth path — "first release of a new plugin:
marketplace add + install, then converge the environment's plugin
management (pins/doctor where the environment has them), then the
reload handoff" — generic wording, environment-specific execution.
Deployment-side half booked concretely in dotfiles BACKLOG
(plugin-birth lane, 2026-08-11).

Minted (2.2.0 canon pass, 2026-08-20): /release-plugin step 1 gains
the birth branch (marketplace add + install + environment
convergence, rejoining at step 7 — no step renumbered);
plugin-engineering.md activation section carries the pointer;
description gains the first-release trigger.

## 2026-08-11 — eval-method deltas from the begehung eval series (three candidates for evaluation.md)

Observed while running the canon's own eval protocol end-to-end on a
newborn skill (begehung: Tier-1 via /eval-skill 12/12; name
cold-probe per SKILL.md term-selection — both fired as designed, a
use-log line for that machinery). Three method gaps surfaced, each
with the incident that grounds it:

1. ABLATION ARM. Tier 2 is two-arm (with/without). The operator's
   counter-question — "would a single sentence perform the same?" —
   has no arm in the protocol, yet it is the no-op test at document
   scale: the strongest cheap competitor is one sentence exploiting
   the skill-name's priors (here justified by the cold-probe result:
   the bare word recruited most of the method). A three-arm run
   (with / without / sentence) separates what the TERM buys from
   what the corpus buys. Evidence pending its own completion: the
   2026-08-11 three-arm run on statiker (record in begehung
   dev-notes/eval-begehung/) — mint only after that run is graded.
2. STAGED PROBES for response-shaped signature elements. A signature
   element of the form "a follow-up X is answered by Y" (begehung's
   rotation element) is unmeasurable in a single saved output — it
   needs a second act against the LIVE arm. Named background agents
   make this cheap (SendMessage follow-up after the first report);
   the protocol currently compares one-shot outputs only.
3. SERIES LIMITATION, stated. A one-shot Tier-2 measures round
   discipline; a skill whose value compounds across sessions (a
   persistent ledger, a rotation schedule) has its core claim
   outside any single run — the honest instrument there is trial-
   series grading, and evaluation.md should say so rather than let
   a flat one-shot delta read as "skill is inert".

Proposal (operator decides; reflexivity rule): the three land as
amendments to references/evaluation.md Tier 2 in a skill-craft canon
session with the Layer-4 self-review; BACKLOG entry parked on the
named trigger.

Minted (2.2.0 canon pass, 2026-08-20): all three landed in
evaluation.md Tier 2 (ablation arm, staged probes, series
limitation) plus the fourth candidate from the graded run
(control-arm definition stated in the record).

## 2026-08-16 — Invariance de-binds: a rule inside identical-per-brief boilerplate reads as plumbing (measured, n=3)

Incident (beat-the-books desk "Session 11", booked with its concrete
fix in dispatch-guards dev-notes/dispatch-OBSERVATIONS.md, same
date — that entry owns the forms.md repair; this one carries the
canon-level class): three same-model discovery dispatches in one
run, each brief carrying the READ-ONLY tail verbatim, which states
the no-report-file rule TWICE. Dispatches 1–2 violated it (wrote a
report file, messaged a pointer); for dispatch 3 the desk moved the
rule — wording unchanged — to the brief's HEAD and named the
consequence ("a file is not a report and will not be read as one"):
complied. Same run, same brief form, same model, same task class —
position the only changed variable.

Diagnosis, and why it is NOT the existing salience case: canon's
"scope precedes default; the default owns its sentence" covers a
default buried mid-sentence in a packed enumeration — parsed, not
fired. Here the rule was neither buried nor under-worded: it held
its own words, twice. What de-bound it is INVARIANCE — a block
identical across every brief is classified by the reader as
transport plumbing and skimmed as a unit, so rules inside it lose
binding force regardless of their local salience. The property that
makes boilerplate a guarantee (byte-identical, never drifts) is the
property that makes it invisible. Measured cure: position at the
container's head + named consequence.

Pre-formulated canon widening (next consolidation pass; Layer-4
self-review applies): the "Scope precedes default" clause gains the
container case — after "Give it its own sentence at the seam it
governs; added rationale only grows what it competes with," append:
"Salience is also container-relative: an invariant block (a pasted
tail, a fixed template) is skimmed as plumbing precisely because it
never varies, and a load-bearing rule inside one de-binds whatever
its wording — position it at the container's head with its
consequence named (measured: 2 violations at tail position, full
compliance after the move, wording unchanged)."

Consumer + drain: next skill-craft consolidation/canon pass (the
entry above proposes evaluation.md amendments the same way); the
concrete forms.md fix drains separately via dispatch-guards'
maintenance quota — one meaning, two grains, each in its owner.

Minted (2.2.0 canon pass, 2026-08-20): the pre-formulated widening
landed in SKILL.md, Scope precedes default.

## 2026-08-20 — Three candidates from a high-volume corpus-editing day (~15 edits, one fresh-context harmony review over the whole governed set)

1. **Amendment search needs the inverse direction.** Amendment
discipline's search finds restatements of the content being ADDED.
The day's review surfaced the inverse class: a mint that changes an
operating premise re-scopes every rule RESTING on the old premise —
two existing rules would have actively forbidden the new
arrangement, and a delta-only review structurally cannot see them.
Candidate: widen Amendment discipline — before landing, ask which
existing rules would forbid, mis-fire, or fall silent under the new
content, and land those sharpens in the same edit set. (Minted
same-day at the operating site's governance layer; this candidate
is the layer-2 generalization — it holds for any governed corpus.)

2. **Register drift is invisible per-edit; the working detector is a
closed-taxonomy sweep with stated instrument reach.** A corpus
written under the two-registers rule had accumulated ten
directive-voice sentences inside evidence-register files, each
individually defensible at its edit. What made them findable: a
fresh-context review using a closed finding taxonomy whose
instrument declared its own REACH — the sentence-initial-imperative
grep was wrap-blind on hard-wrapped text, so its count was reported
as a lower bound, with a live positive control. Candidate:
review-checklist gains a register-consistency item prescribing
exactly that instrument-honesty form (closed classes, reach stated,
counts as bounds where the instrument is blind).

3. **Protocol-shaped skills owe a delivery walk.** A multi-party
delegation protocol designed the same day shipped three steps that
ASSUMED delivery with no mechanism carrying them: a line a human
must paste (never handed to them), state that must survive the
authoring session (never persisted), an acknowledgment (never
awaited). All three were found by the operator, none by review.
Candidate: for any skill prescribing a multi-party or multi-session
protocol, the review walks the lifecycle end-to-end asking per step
WHO DELIVERS it — inline text, gate, artifact, or human memory,
where human memory is the finding.

Minted (2.2.0 canon pass, 2026-08-20): (1) inverse-direction search
in Amendment discipline; (2) register-drift sweep form in checklist
item 8; (3) delivery walk in checklist item 14.

## 2026-08-20 — consolidation input: birth branch duplicates plugin-engineering's install sequence

From the 2.2.0 self-review (finding N7, operator disposition
defer-to-observations). release-plugin.md's birth branch and
plugin-engineering.md:189-194 both carry the marketplace-add +
fully-qualified-install sequence. The command file must stay
paste-executable (a release step cannot depend on loading a
reference mid-command), so the consolidation direction is the
other way: plugin-engineering's Path A install step points at
/release-plugin's birth branch instead of restating the commands.
Pre-formulated fix: replace that step's command lines with one
pointer line. Consumer + drain: next skill-craft consolidation
pass (same as the eval-deltas entry's route).

## 2026-08-20 — Triple probe on fresh rules: sequenced single-axis passes out-find one combined review
- **Incident + basis:** one freshly minted corpus rule, three sequential operator review passes, three distinct real findings — carrier (home would die with its arc), shape (overclaim + a parent rule restated badly instead of cross-referenced), abstraction (incident flavor surviving into the wording). Each finding was invisible before the previous repair landed, because each repair changed the text the next pass graded. A single combined review had found only the first.
- **Class:** review-pass architecture — sequenced single-axis passes vs one multi-axis pass, for freshly authored steering text.
- **Pre-formulated change:** review-checklist.md gains a note at its head (or the fresh-rule branch): for text authored in this session, run the checklist as SEQUENCED single-axis passes — carrier/home first, claim-shape second, abstraction/de-particularization third — re-reading the corrected text between passes; the combined walk stays correct for text not just written.
- **Consumer + drain seam:** skill-craft maintainer at the next review-checklist pass; drains via the standing OBSERVATIONS quota.
