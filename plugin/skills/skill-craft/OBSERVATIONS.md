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
