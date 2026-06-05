# Evaluating a skill

**Load when:** Designing a new skill (build the eval before extensive
procedure text) or validating one before release.

Evaluation measures whether a skill changes behaviour as intended. It
complements review (which inspects the text) with measurement (which
observes the skill in use): a skill can read clean and still
under-trigger or sit inert. Run the minimum tier the skill's type and
stakes require — running more is the Additive-reflex shape
(`anti-patterns.md`).

## Which tiers apply

| Skill type | Tier 1 trigger | Tier 2 signature | Tier 3 grade |
|---|---|---|---|
| Tooling / workflow (deterministic) | yes | yes — assert on output | rarely |
| Judgment | yes | when it forces an observable signature | high-stakes only |
| Domain-general framework | yes | yes | yes |

## Tier 1 — Triggering (mechanical; the description is the oracle)

The `description` alone decides whether a skill fires — an external,
measurable property. Measure it directly. Author it to that test: state
what the skill does AND when to use it, in the specific terms a user
would type, and treat the should-trigger / should-NOT-trigger sets below
as the bidirectional trigger check (`writing-by-skill-type.md`) pointed
at the description — write the minimum description that fires on every
should-trigger query and no near-miss.

- [ ] Triggering measured? (N/A only when the skill is invoked solely
  by explicit slash-command, not description-matching — checkable from
  the manifest.)
  - NO → CANNOT release. Assemble ≥5 realistic should-trigger queries
    and ≥3 tricky should-NOT-trigger near-misses; run each ≥3×; record
    fire/no-fire counts.
  - YES → Evidence: [query set + per-query fire rate]

A should-trigger query that misfires means the description
under-triggers; a near-miss that fires means it over-triggers. Repair the
**description**, never the body, then re-measure — under-trigger: add the
missing trigger terms or a direct "use when …" clause (widen by
principle, not a synonym list, per `writing-by-skill-type.md`);
over-trigger: narrow the clause the near-miss matched, or name the
competitor skill that should own it. The runner is the
`/eval-skill <name>` slash command in this plugin
(`commands/eval-skill.md` + `agents/skill-router.md`); it dispatches
three `skill-router` subagents in parallel against a candidate +
competitor list, aggregates fire rates, and surfaces diagnoses.

## Tier 2 — Behaviour-delta signature (un-fakeable artifact, applied to evaluation)

The correctness of a judgment cannot be asserted directly. Name
instead the skill's **signature** — the observable artifacts it exists
to force that the bare model omits — and confirm the signature appears
only with the skill loaded.

1. Name the signature: the artifacts the skill must produce (a
   judgment skill's findings carrying location + impact +
   classification; a workflow skill's gate evidence).
2. Run one representative task **with** and **without** the skill.
3. Signature present with, absent without → the skill is doing its
   work. Present in both → inert on that task. Absent in both → the
   skill failed to fire its own discipline.

The delta is the skill's value; the signature is its un-fakeable
artifact, present only when the work was done (`PROCEDURE.md` Layer 2).
`/eval-skill <name>` scaffolds this protocol: it dispatches a
with-skill and a without-skill subagent in parallel on one
operator-supplied task, saves both outputs side-by-side, and surfaces
them for the operator's signature comparison (the judgment stays
operator-side; the running of with/without is automated).

**The trajectory is evidence, not just the final artifact.** A signature
can appear in the output while the path that produced it failed — a gate
skipped on a success path that passed anyway, a recovered wrong turn, a
wasteful loop. Read the run's trajectory (what the agent did), not only
its output: a load-bearing step absent from the trajectory is a finding
even when the artifact looks right. The same read surfaces the converse —
a helper the agent re-derives across runs is a chore to freeze into a
bundled script (`writing-by-skill-type.md`, Skills that bundle scripts).

## Tier 3 — Isolated grade (the subjective residue)

The irreducibly-subjective quality — was the analysis insightful, the
cut correct — has no mechanical oracle. Where stakes justify it,
dispatch a fresh-context grader subagent that did not author the skill
or run the eval, to score the with/without outputs blind. Isolation
lowers the floor; it does not remove it (same lever as the Self-review
mandate, `PROCEDURE.md` Layer 4). Reserve for high-stakes or
widely-used skills.

## Relation to evolution

A Tier-1 or Tier-2 failure is a candidate observation, not only a fix
— route it through the Layer 4 cycle (`PROCEDURE.md`).
