# Evaluating a skill

**Load when:** designing a new skill (build the eval before the
procedure text) or validating one before release.

Evaluation measures whether a skill changes behaviour as intended.
It complements review (which inspects the text) with measurement
(which observes the skill in use): a skill can read clean and still
under-trigger or sit inert. Run the minimum tier the skill's type
and stakes require — running more is the Additive-reflex shape
(`anti-patterns.md`).

## Which tiers apply

| Skill type | Tier 1 trigger | Tier 2 signature | Tier 3 grade |
|---|---|---|---|
| Tooling / workflow (deterministic) | yes | yes — assert on output | rarely |
| Judgment | yes | when it forces an observable signature | high-stakes only |
| Domain-general framework | yes | yes | yes |

## Tier 1 — Triggering (mechanical; the description is the oracle)

The `description` alone decides whether a skill fires — an
external, measurable property. Measure it directly, and author the
description to the test: what the skill does AND when to use it, in
the terms a user would type — the minimum description that fires on
every should-trigger query and no near-miss (the bidirectional
trigger check of `writing-by-skill-type.md`, pointed at the
description).

Triggering is measured before release for any description-triggered
skill. The exemption is mechanical: invocation exclusively by slash
command, checkable from the manifest — and delisting a description
carries a measured cost to prose invocation (SKILL.md, Invocation
choice: listed 12/12, delisted 0/12), so the exemption is claimed,
not assumed. The measurement: ≥5 realistic should-trigger queries
and ≥3 tricky should-NOT-trigger near-misses, each run ≥3×;
evidence is the query set plus per-query fire rates.

A should-trigger miss means the description under-triggers; a
near-miss fire means it over-triggers. Repair the **description**,
never the body, then re-measure — under-trigger: add the missing
trigger term or a direct "use when …" clause (widen by principle,
not a synonym list, per `writing-by-skill-type.md`); over-trigger:
narrow the clause the near-miss matched, or name the competitor
skill that should own it. The runner is `/eval-skill <name>`
(`commands/eval-skill.md` + `agents/skill-router.md`): three
`skill-router` subagents in parallel against a candidate +
competitor list, fire rates aggregated, diagnoses surfaced.

## Tier 2 — Behaviour-delta signature (un-fakeable artifact, applied to evaluation)

The correctness of a judgment cannot be asserted directly. Name
instead the skill's **signature** — the observable artifacts it
exists to force that the bare model omits — and confirm the
signature appears only with the skill loaded.

1. Name the signature: the artifacts the skill must produce (a
   judgment skill's findings carrying location + impact +
   classification; a workflow skill's gate evidence).
2. Run one representative task **with** and **without** the skill.
   The arms must differ in the skill alone: an always-on injector
   (a plugin hook, a global instruction file) can carry the skill's
   text into the without-arm and collapse the delta — and merely
   READING the candidate contaminates: a skill's format has
   transferred on contact alone, without invocation, surfacing a
   hundred turns later. A control arm in a session that has read
   the candidate is not a control.
3. Signature present with, absent without → the skill is doing its
   work. Present in both → before reading it as inert, grep the
   without-arm's output for the skill's coined terms — vocabulary
   the skill's own files introduce that the task statement does not
   contain; the signature elements of step 1 seed the list. A hit
   means the arm was contaminated — trace the matched phrase to its
   source and rerun with that injector disabled; the run is
   invalid. A clean grep does not prove a clean arm (an injector
   can carry the discipline in its own words) — with no hit and no
   known injector in the surface, read the skill as inert on that
   task. Absent in both → the skill failed to fire its own
   discipline.

The delta is the skill's value; the signature is its un-fakeable
artifact, present only when the work was done (SKILL.md,
Enforcement). `/eval-skill <name>` scaffolds the protocol: a
with-skill and a without-skill subagent in parallel on one
operator-supplied task, outputs saved side-by-side, the signature
comparison staying operator-side.

**The trajectory is evidence, not just the final artifact.** A
signature can appear in the output while the path that produced it
failed — a gate skipped on a success path, a recovered wrong turn,
a wasteful loop. Read what the agent did, not only what it
produced: a load-bearing step absent from the trajectory is a
finding even when the artifact looks right. The same read surfaces
the converse — a helper re-derived across runs is a chore to freeze
into a bundled script (`writing-by-skill-type.md`, Skills that
bundle scripts).

## Tier 3 — Isolated grade (the subjective residue)

The irreducibly-subjective quality — was the analysis insightful,
the cut correct — has no mechanical oracle. Where stakes justify
it, dispatch a fresh-context grader subagent that neither authored
the skill nor ran the eval, scoring the with/without outputs blind.
Isolation lowers the floor; it does not remove it (the same lever
as the self-review dispatch, `references/self-review.md`). Reserve
for high-stakes or widely-used skills.

## Relation to evolution

A Tier-1 or Tier-2 failure is a candidate observation, not only a
fix — route it through the evolution cycle (SKILL.md, Lifecycle).
