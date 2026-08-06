# /eval-skill skill-craft — 2026-08-06 (2.0.0 rewrite session)

Skill path: plugin/skills/skill-craft/SKILL.md (source repo, 2.0.0-dev
working tree; installed pin frozen at 1.2.0)
Tier applicability: (a) description-triggered. Two Tier-1 runs, both
via the runner protocol (3 × sonnet `skill-router` subagents per
condition, per-query fire counts).

## Run 1 — prose invocation vs. delisting (PLAN.md open question, Harvest B item 2)

Question: does prose invocation ("run X", the bare name) still
resolve when a skill's description leaves the model's listing
(`disable-model-invocation`)?

Conditions: statiker LISTED (7-skill list, real descriptions) vs
DELISTED (same list minus statiker). Same 7 queries; 4 carry the
name.

| Query | Listed | Delisted |
|---|---|---|
| "run statiker on \<bug\>" | 3/3 statiker | 0/3 (1× daneel misroute) |
| "statiker: \<task\>" | 3/3 statiker | 0/3 |
| "use statiker to \<task\>" | 3/3 statiker | 0/3 |
| bare "statiker" | 3/3 statiker | 0/3 |
| structured pass, no name (control) | 1× none / 2× daneel | 3/3 daneel |
| "debug why \<symptom\>" (control) | 3/3 daneel | 3/3 daneel |
| trivial rename (control) | 3/3 none | 3/3 none |

Verdict: name-carrying prose resolved 12/12 listed, 0/12 delisted.
Delisted routers read the name as noise ("not an available skill
name"); one misrouted the named request to a content-matching
competitor. Instrument liveness: the listed arm is the known
positive — same queries, same instrument, 12/12.

Limit: the simulation measures the model's selection-against-listing
step. The harness separately accepts explicitly user-typed names as
valid Skill calls — but nothing in the listing tells the model an
unlisted name IS a skill, and the simulation shows the name read as
noise. Doctrine landed in SKILL.md, Invocation choice: delisting is
safe only for slash-invoked skills; no fleet-wide description-flip
for prose-invoked skills.

## Run 2 — Tier 1 on the 2.0.0 description

Candidates: new skill-craft description + 6 competitors (anneal-dev,
coherence-audit, update-config, dispatch, bildhauer,
architecture-audit). 6 should-trigger + 4 near-miss queries, 3
trials.

| Query (abbreviated) | Fire | Verdict |
|---|---|---|
| build a new skill enforcing a checklist | 3/3 skill-craft | clean |
| review my daneel skill — bloated, verify step ignored | 3/3 skill-craft | clean |
| integration-shakedown never fires — fix its description | 3/3 skill-craft | clean |
| blocking gates or principles? runs on sonnet | 3/3 skill-craft | clean |
| package three skills into a plugin, private marketplace | 3/3 skill-craft | clean |
| checklist the model rubber-stamps — make checks un-fakeable | 3/3 skill-craft | clean |
| sharpen grounding rule in global CLAUDE.md (near-miss) | 3/3 anneal-dev | clean |
| audit locked glossary corpus (near-miss) | 3/3 coherence-audit | clean |
| add a hook that runs eslint (near-miss) | 3/3 update-config | clean |
| write a dispatch brief (near-miss) | 3/3 dispatch | clean |

Verdict: 18/18 should-trigger, 12/12 near-miss clean. Description
ships unrepaired.

## Next action

None for Tier 1. Tier 2 (behaviour-delta signature of the 2.0.0
canon) is not run this session — the rewrite brief's done criteria
name Tier 1 only; the real behavioural trial is the
anneal-successor lift (PLAN.md, Mission and succession).
