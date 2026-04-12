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
