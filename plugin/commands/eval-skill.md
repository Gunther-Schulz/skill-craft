---
description: Measure a skill's triggering (Tier 1) and behaviour-delta signature (Tier 2). Applies skill-craft's references/evaluation.md to any skill — its own, anneal-dev, clippy, anything.
argument-hint: <skill-name>
---

# /eval-skill $ARGUMENTS

Run skill-craft's evaluation discipline on the skill named `$ARGUMENTS`. Tier 1 measures whether the description triggers correctly; Tier 2 measures whether running the skill produces its un-fakeable signature; Tier 3 (isolated grade) is operator-discretion for the subjective residue and not driven by this command.

## Step 1 — Load the protocol (load-bearing gate), then locate the skill

**FIRST**, load `references/evaluation.md` from skill-craft into context. State the section headers loaded as the un-fakeable load artifact — no subsequent step is valid without this load. Without it, the command runs on memory of the discipline, not the discipline itself (`anti-patterns.md` Soft-load-pointer).

Then find the target skill's `SKILL.md`. Search likely locations and show the operator the file path + the description verbatim:

```
ls ~/.claude/plugins/cache/*/<plugin>/*/skills/$ARGUMENTS/SKILL.md 2>/dev/null
ls ~/.claude/plugins/marketplaces/*/plugin/skills/$ARGUMENTS/SKILL.md 2>/dev/null
```

If multiple paths match, prefer the cache path matching the currently-installed version (read `~/.claude/plugins/installed_plugins.json`).

## Step 2 — Determine which tiers apply

Inspect the SKILL.md frontmatter description (loaded in Step 1) and apply this mechanical rule:

- **(a) Description-triggered** — the description contains natural-language trigger phrases / domain matching the router could route on. Tier 1 + Tier 2 both apply.
- **(b) Name-invoked-only** — invocation is exclusively via explicit slash-command or skill-name reference (e.g. `/skill-name`, "invoke skill-name"), and the description either says so or carries no trigger keywords beyond the skill's own name. Tier 1 is **N/A**; skip with an explicit note. Tier 2 applies.

When ambiguous (skills can be both — e.g. skill-craft is description-triggered AND a framework method), default to (a). Confirm the classification with the operator in one line before dispatching.

Per `references/evaluation.md`: "Run the minimum tier the skill's type and stakes require — running more is the Additive-reflex shape." Do not run Tier 1 on a name-invoked-only skill to pad the report.

## Step 3 — Tier 1 (if applicable): triggering rate

a. **Assemble the test set.** Ask the operator: draft it now, or do they have one? If drafting, propose:
   - **Competitors**: 3-5 other plugins/skills the router would plausibly consider (look at `~/.claude/plugins/installed_plugins.json` + each skill's description for realistic alternatives).
   - **Should-trigger queries (≥5)**: realistic, substantive, varied phrasing — not keyword echoes of the description.
   - **Should-NOT-trigger near-misses (≥3)**: keyword-bait that *shouldn't* fire it (overlapping vocabulary, adjacent domain, the genuine boundary cases the description must reject).
   Show the draft for operator confirmation before dispatch.

b. **Dispatch 3 `skill-router` subagents in parallel.** Each receives the same input: candidate skill + competitor descriptions + the full query set. Each returns per-query routing decisions.

c. **Aggregate.** Per query, count fires (0–3). Report a table: query → fire-count → verdict (clean / under-trigger / over-trigger / boundary). A should-trigger miss across 3/3 trials is a real defect; 1-2/3 is borderline noise.

d. **Diagnose misses.** For each defect: name the likely mechanism (keyword collision with a competitor that owns the literal verb, missing trigger phrase, overclaimed territory that should be delegated, etc.). Per `evaluation.md`: the fix is the description, not the body — and you re-measure after.

## Step 4 — Tier 2 (always applicable): behaviour-delta signature

a. **Get the signature spec from the operator.** Ask: what un-fakeable artifact does `$ARGUMENTS` exist to force that the bare model would not produce? Examples to give if useful: "findings carrying file:line + impact + classification" (judgment skill); "a tracker with locked design decisions + isolated verify ledger" (workflow skill); "14-item review-checklist completion with file:line per item" (review skill). The signature must be *observable in the output*, not "good thinking."

b. **Get one representative task** the skill is designed to handle.

c. **Dispatch two general-purpose subagents in parallel** with these briefs. First derive the qualified Skill-tool name `<plugin>:$ARGUMENTS` from the SKILL.md path located in Step 1 (path shape: `…/cache/<marketplace>/<plugin>/<version>/skills/$ARGUMENTS/SKILL.md` → `<plugin>` is the directory segment after the marketplace). Pass that qualified name into both briefs.
   - **WITH-skill**: "Invoke the `<plugin>:$ARGUMENTS` skill (via `Skill(skill='<plugin>:$ARGUMENTS')`) and follow its guidance to execute this task. Task: [paste task]. Save your full output verbatim."
   - **WITHOUT-skill**: "Execute this task directly. Do NOT invoke `<plugin>:$ARGUMENTS` or any specialized methodology skill (skill-craft, anneal-dev, clippy, etc.) — respond as you would without them loaded. Task: [paste task]. Save your full output verbatim."

d. **Save outputs.** Default target: `./dev-notes/eval-$ARGUMENTS/<YYYY-MM-DD>/` (or `~/.claude/skill-evals/$ARGUMENTS/<YYYY-MM-DD>/` if no `dev-notes/` exists in CWD). Confirm or override with the operator in one question. Write `tier2-with.md` and `tier2-without.md` verbatim.

e. **Surface side-by-side for the operator with cited evidence.** For each signature element the operator named in (a), locate it (or its absence) in both saved files and report with file:line citations — e.g. "element 'finding with location+impact+classification' present in `tier2-with.md:L42-58` (quote: '...'), absent in `tier2-without.md` (grep '<pattern>' returned 0 hits)." **A verdict line without per-element citations is malformed; the citations are the un-fakeable artifact for the verdict** (the verdict itself, otherwise, is a bare-claim shape — `anti-patterns.md`).

   Then name the pattern:
   - **Signature present in WITH, absent in WITHOUT** → skill is doing its work.
   - **Signature present in both** → skill is inert on this task (bare model already does it). Path-1 observation candidate: maybe the trigger is wrong, maybe the skill is over-broad.
   - **Signature absent in WITH** → skill failed to fire its own discipline. Path-1 observation candidate: the skill loaded but the gates didn't bind.
   The operator does the final signature judgment. The command surfaces grounded evidence, not a verdict.

## Step 5 — Write the eval record

Write `./dev-notes/eval-$ARGUMENTS/<YYYY-MM-DD>/result.md`:

```
# /eval-skill $ARGUMENTS — <date>

Skill path: <path to SKILL.md>
Installed version: <version from installed_plugins.json>
Tier applicability: (a) / (b) + 1-line reason

## Tier 1
[fire-rate table, or "N/A — name-invoked-only / framework method"]
[diagnosis of any misses]

## Tier 2
Signature spec: <what the operator named>
Task: <the one representative task>
Verdict: present-with / absent-without (or whichever pattern observed)

## Next action
[description revision / Path-1 observation in <skill>/OBSERVATIONS.md / accept-as-clean / Tier-3 escalation]
```

## Closing the loop

Per `references/evaluation.md` "Relation to evolution": a Tier-1 or Tier-2 failure is a candidate **observation** for the evaluated skill's own `OBSERVATIONS.md` (if it has one), not only a one-shot fix. After the verdict, ask the operator: log this as an observation in the skill's **source-repo** `dev-notes/OBSERVATIONS.md` (the source repo, not the installed cache — per skill-craft's boundary rule, maintenance files live at source-repo level; ask the operator for the path if not known)?
