# Skill-craft 2.0.0 — the rewrite plan (persisted 2026-08-06)

Consumer of this file: the session that writes the 2.0.0 canon, and
the trial sessions after it. Every subtle decision from the design
discussion (2026-08-06 session, mattpocock/skills comparison) is
HERE; the conversation is not the carrier. Companion observations:
dev-notes/OBSERVATIONS.md entries dated 2026-08-06.

## Mission and succession

Rewrite the CANON from scratch — SKILL.md, PROCEDURE.md,
references/*.md — in this repo, same plugin name. The infrastructure
(eval runner, /release-plugin, stale-pin hooks, /eval-skill,
skill-router agent) is not doctrine and carries over untouched.

- The installed 1.2.0 pin IS the freeze (clippy-freeze pattern,
  statiker PLAN.md). Main proceeds as unreleased 2.0.0-dev.
- 2.0.0 releases only after a real trial: producing at least one
  real skill well. Named trial: the anneal-successor lift from
  statiker (operator roadmap).
- No working title — the version boundary does what the statiker
  name did.

**Basis of the rewrite — recorded so the write session harvests
instead of discarding.** NOT staleness: the July-2026 annealing is
current (two registers 07-26, durability classes 07-10, consumer
calibration 07-23, Fable-delta audit 07-23; backlog cleared 08-05).
The basis is two-fold: (1) the ECONOMICS half of the discipline is
entirely absent — months of amendment never produced it (no commit
touches pointer wording, invocation cost, or term selection-for-
priors); (2) the canon's own FORM contradicts its newest doctrine —
it teaches consumer calibration while being written as
blocking-gates-everywhere for a below-trust-tier reader, 634 dense
lines in the inherited five-layer frame. Iterated amendment
converges within an architecture, never out of it (the statiker
lesson). Which model authored earlier strata is anecdote, not a
graded basis — no model-grading in this plan.

## The spine (settled: operator GO on Q1)

Two-party model, replacing "un-fakeable artifacts" as the top-level
thesis:

- The WRITER of a skill is a top-tier model, steered by
  evidence-register doctrine, thin.
- Every produced skill DECLARES its consumer tier; that declaration
  decides the skill's enforcement density. Enforcement is a
  function of the declared consumer, not a default.
- Un-fakeable artifacts remain the spine OF THE ENFORCEMENT
  TOOLBOX — fully alive, tier-conditional, the below-trust-tier
  instrument set.
- The economics doctrine (pointer wording, the two loads,
  invocation choice, term selection, no-op pruning) applies at
  EVERY tier.

Statiker's local declaration ("prescription density is calibrated
to it") is this spine applied once; 2.0.0 makes it the central
teaching.

## Upstream documents (settled: Q2)

VISION.md retires as a standing derivation source at 2.0.0 (file
drops from dev-notes; git history preserves it). What survives of
its content folds into this PLAN and the canon directly. The
VISION→PROCEDURE derivation contract is replaced by the
statiker-style birth declaration inside the new canon. Single
upstream: this file, until the canon exists; then the canon is the
single home.

## The canon's own register (settled: Q3)

Skill-craft is a judgment skill consumed by Fable. The new canon
drops prose gates ON ITSELF: the load-gate boilerplate and the
14-item CANNOT-proceed checklist framing retire. The checklist's 14
QUESTIONS survive as a review reference (content, not gate).
Mechanical checks stay mechanical: eval runner, release/stale-pin
hooks, and the pre-commit fresh-context self-review dispatch
(fresh-context vet is tier-insensitive insurance, not a capability
patch).

Doctrine/machinery line (settled): TEACHING content (doctrine,
evidence-register prose) is harvested rich — birth-thin does not
apply to it. MACHINERY skill-craft applies to itself (gates,
mandates, checklists-as-gates) is born near-zero and fire-earns its
way in, statiker fire-born rules: one incident as provenance,
amendment over addition, firing log in dev-notes/OBSERVATIONS.md,
no-fire-since-review = cut candidate.

## Harvest list A — from the 1.2.0 canon (re-enters with existing
provenance; OBSERVATIONS.md is the grading record)

Admit (content, possibly re-homed/re-registered):
- Un-fakeable-artifact principle + N/A-escape hardening
- The two registers + trigger-axis clause
- Scope-precedes-default + salience rule
- Commitment consistency across phase boundaries; information flow
  in orchestrated workflows
- Durability classes (enforcement/patch/binding) + firing-based
  retirement + re-registering on tier shifts
- Amendment discipline incl. multi-file governed-set +
  search-before-add; iterative narrowing; abstraction check;
  context-independence check; rendering-from-source
- Category 1/2 boundary (write-target vs read dependency)
- Evaluation tiers 1–3 (unique asset; nothing comparable exists in
  the reference corpus)
- plugin-engineering.md mechanics; release/activation flow
- Terminology discipline — SHARPENED, see Harvest B item 3

Suspect at intake (each must re-earn placement; default is out):
- Blocking logic as the default enforcement rendering (becomes
  tier-conditional toolbox content)
- Word-count budgets as stated (re-derive from the two-loads frame)
- Consolidated load-gate boilerplate pattern (mint once as a named
  convention IF it survives at all; below-trust-tier tool)
- The five-layer frame itself as the organizing architecture
- "Every sentence must change behavior" — survives, but re-founded
  on the model-relative no-op test (Harvest B item 4)

## Harvest list B — from mattpocock/skills (MIT; credit line in
dev-notes; adapt in, never cite by pointer — context-independence)

1. **Pointer economics** (writing-for-agents: Context pointers) —
   Path 1; incident: fleet descriptions observed overweight this
   session (integration-shakedown ~180 words; statiker's
   forcing-point summary buys zero triggering on an explicit-invoke
   skill). Wording decides firing; sharpen before inlining;
   front-load the leading word; one trigger per branch; cut
   identity the body carries.
2. **Invocation choice as economics** (SKILL-MECHANICS: model- vs
   user-invoked, disable-model-invocation) — Path 1. Explicit-
   invoke-only skills pay zero context load. OPEN QUESTION for the
   write session, Tier-1-testable: operator invokes by prose ("run
   statiker"), not only by slash — verify prose invocation still
   resolves when the description leaves the model's listing,
   BEFORE recommending the flip fleet-wide.
3. **Term selection recruits priors** (Leading words) — Path 1;
   TWO incidents: (a) operator-recalled: Opus echoed the operator's
   non-expert phrasing when minting rules — the existing
   canonical-term obligation was the mitigation attempt, and it
   under-specifies selection; (b) this session: the "frontier"
   round-format transferred on mere contact (see OBSERVATIONS
   2026-08-06). Sharpening direction (operator: "the clearest term
   of its domain", analogous phrasing to be authored, not this
   sentence): selection criterion = the term the domain's canonical
   literature converged on (defined and re-used across a large
   consistent body of pretrained text); verification = cold-probe a
   fresh context for the behavior the term implies; anti-target =
   echoing operator phrasing. Enum/parser tokens stay coined by
   design; words meant to steer thinking prefer priors.
4. **No-op test is model-relative → era-regrade lifecycle** —
   Path 1 (partially present: Migration section, re-registering
   axis; WIDEN, don't duplicate). Settled by running, not debate;
   on model-era change, re-grade the corpus (Tier 2 is the
   instrument). This is the codified form of the operator's own
   history: clippy-era machinery was compensation for weaker
   models.
5. **Negation/positive phrasing** — Path 2 (marked hypothesis). A
   lens WITHIN the registers section: prefer positive rendering
   where the rule is directive; evidence-register failure-shape
   statements are load-bearing and exempt. Validate by use.
6. **Demand wording on completion criteria** ("every X accounted
   for" forces legwork; complements checkability) and
   **environment-as-source-of-truth** (a doc restating --help/
   config is a cache; cache only expensive lookups) — Path 2.

## Write-session conduct

- Written DIRECT, single home, no spec→render chain.
- The new canon demonstrates its own doctrine: pointer-economical
  description, prior-recruiting terms, decision-per-sentence
  register. The file is its own first exhibit.
- Build the evaluation before the procedure text where it applies
  (existing doctrine, kept).
- Self-review dispatch before commit (kept, see above).

## Out of scope, booked elsewhere

- The grilling/frontier-round form: minted thin as an operator-
  corpus convention (dotfiles f3dfa52, CLAUDE.md Recommending &
  reporting) — never skill-craft content (operator correction
  2026-08-06; skill-craft stays pure craft).
- Fleet description rewrites and description-flip of explicit-
  invoke skills — follows 2.0.0, using its doctrine + Tier 1 evals.
